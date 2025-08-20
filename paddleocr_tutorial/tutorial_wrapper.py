#!/usr/bin/env python3
"""
Tutorial Wrapper Module
=======================

기존 튜토리얼 예제들(01_basic_cli.py ~ 05_performance_test.py)을 
Flet UI에서 호출할 수 있도록 래핑하는 모듈

이 모듈은 각 튜토리얼 예제의 main 함수를 호출하고 
결과를 UI에 표시할 수 있는 형태로 변환합니다.
"""

import sys
import os
import time
import io
import contextlib
import traceback
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import importlib.util

# 현재 디렉터리 설정
current_dir = Path(__file__).parent
examples_dir = current_dir / "examples"

@dataclass
class TutorialExecutionResult:
    """튜토리얼 실행 결과"""
    section_id: str
    title: str
    success: bool
    duration: float
    output: str
    error: str
    details: Dict[str, Any]
    timestamp: datetime

class OutputCapture:
    """표준 출력/에러 캡처 클래스"""
    
    def __init__(self):
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()
        self.output = ""
        self.error = ""
    
    def __enter__(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._stdout
        sys.stderr = self._stderr
        self.output = self.stdout.getvalue()
        self.error = self.stderr.getvalue()

class TutorialWrapper:
    """튜토리얼 예제 래퍼 클래스"""
    
    def __init__(self):
        self.examples_dir = examples_dir
        self.available_tutorials = self._discover_tutorials()
        self.progress_callback: Optional[Callable] = None
    
    def set_progress_callback(self, callback: Callable):
        """진행률 콜백 설정"""
        self.progress_callback = callback
    
    def _discover_tutorials(self) -> Dict[str, Dict[str, str]]:
        """사용 가능한 튜토리얼 발견"""
        tutorials = {
            "01_basic_cli": {
                "title": "섹션 2.3: 기본 CLI 예제",
                "description": "PaddleOCR CLI 명령어 및 기본 파이프라인 테스트",
                "file": "01_basic_cli.py"
            },
            "02_python_api": {
                "title": "섹션 2.4: Python API 예제", 
                "description": "Python API 사용법 및 결과 구조 분석",
                "file": "02_python_api.py"
            },
            "03_multilingual": {
                "title": "섹션 3.1: 다국어 지원",
                "description": "80+ 언어 지원 및 다국어 성능 비교",
                "file": "03_multilingual.py"
            },
            "04_modular_pipeline": {
                "title": "섹션 3.2: 모듈러 파이프라인",
                "description": "검출/인식 컴포넌트별 개별 실행",
                "file": "04_modular_pipeline.py"
            },
            "05_performance_test": {
                "title": "섹션 4: 성능 테스트",
                "description": "종합 성능 분석 및 벤치마킹",
                "file": "05_performance_test.py"
            }
        }
        
        # 실제 파일 존재 여부 확인
        available = {}
        for tid, info in tutorials.items():
            file_path = self.examples_dir / info["file"]
            if file_path.exists():
                available[tid] = info
                available[tid]["path"] = str(file_path)
            else:
                print(f"⚠️ 튜토리얼 파일 없음: {file_path}")
        
        return available
    
    def get_available_tutorials(self) -> Dict[str, Dict[str, str]]:
        """사용 가능한 튜토리얼 목록 반환"""
        return self.available_tutorials
    
    def execute_tutorial(self, section_id: str, demo_type: str = "all", **kwargs) -> TutorialExecutionResult:
        """튜토리얼 실행"""
        start_time = time.time()
        
        if self.progress_callback:
            self.progress_callback(f"튜토리얼 {section_id} 실행 시작...")
        
        if section_id not in self.available_tutorials:
            return TutorialExecutionResult(
                section_id=section_id,
                title=f"알 수 없는 섹션: {section_id}",
                success=False,
                duration=0,
                output="",
                error=f"튜토리얼 {section_id}을(를) 찾을 수 없습니다",
                details={},
                timestamp=datetime.now()
            )
        
        tutorial_info = self.available_tutorials[section_id]
        
        try:
            # 튜토리얼 모듈 동적 로딩
            spec = importlib.util.spec_from_file_location(
                f"tutorial_{section_id}", 
                tutorial_info["path"]
            )
            
            if spec is None or spec.loader is None:
                raise ImportError(f"모듈 로딩 실패: {tutorial_info['path']}")
            
            module = importlib.util.module_from_spec(spec)
            
            # 출력 캡처와 함께 모듈 실행
            with OutputCapture() as capture:
                if self.progress_callback:
                    self.progress_callback(f"모듈 {section_id} 로딩 중...")
                
                spec.loader.exec_module(module)
                
                # 데모 실행
                result = self._run_tutorial_demo(module, section_id, demo_type, **kwargs)
            
            duration = time.time() - start_time
            
            if self.progress_callback:
                self.progress_callback(f"튜토리얼 {section_id} 완료 ({duration:.2f}초)")
            
            return TutorialExecutionResult(
                section_id=section_id,
                title=tutorial_info["title"],
                success=True,
                duration=duration,
                output=capture.output,
                error=capture.error,
                details=result,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            duration = time.time() - start_time
            error_msg = f"튜토리얼 실행 오류: {str(e)}\n{traceback.format_exc()}"
            
            if self.progress_callback:
                self.progress_callback(f"튜토리얼 {section_id} 실패: {str(e)}")
            
            return TutorialExecutionResult(
                section_id=section_id,
                title=tutorial_info.get("title", section_id),
                success=False,
                duration=duration,
                output="",
                error=error_msg,
                details={},
                timestamp=datetime.now()
            )
    
    def _run_tutorial_demo(self, module, section_id: str, demo_type: str, **kwargs) -> Dict[str, Any]:
        """실제 튜토리얼 데모 실행"""
        result = {"demo_type": demo_type, "parameters": kwargs}
        
        try:
            if section_id == "01_basic_cli":
                result.update(self._run_basic_cli_demo(module, demo_type))
            elif section_id == "02_python_api":
                result.update(self._run_python_api_demo(module, demo_type))
            elif section_id == "03_multilingual":
                result.update(self._run_multilingual_demo(module, demo_type))
            elif section_id == "04_modular_pipeline":
                result.update(self._run_modular_pipeline_demo(module, demo_type))
            elif section_id == "05_performance_test":
                result.update(self._run_performance_test_demo(module, demo_type))
            else:
                # 일반적인 main 함수 실행
                if hasattr(module, 'main'):
                    result["output"] = str(module.main())
                else:
                    result["output"] = "main 함수가 없습니다"
        
        except Exception as e:
            result["error"] = f"데모 실행 오류: {str(e)}"
            result["traceback"] = traceback.format_exc()
        
        return result
    
    def _run_basic_cli_demo(self, module, demo_type: str) -> Dict[str, Any]:
        """기본 CLI 데모 실행"""
        if self.progress_callback:
            self.progress_callback("CLI 예제 실행 중...")
        
        try:
            if hasattr(module, 'demonstrate_cli_usage'):
                # CLI 사용법 시연
                return {"cli_demo": module.demonstrate_cli_usage()}
            elif hasattr(module, 'main'):
                return {"main_output": module.main()}
            else:
                # 시뮬레이션
                time.sleep(1)
                return {
                    "simulation": True,
                    "features": [
                        "Full pipeline inference",
                        "Component-specific inference", 
                        "Model version selection",
                        "Multilingual CLI processing"
                    ]
                }
        except Exception as e:
            return {"error": str(e)}
    
    def _run_python_api_demo(self, module, demo_type: str) -> Dict[str, Any]:
        """Python API 데모 실행"""
        if self.progress_callback:
            self.progress_callback("Python API 예제 실행 중...")
        
        try:
            if hasattr(module, 'demonstrate_python_api'):
                return {"api_demo": module.demonstrate_python_api()}
            elif hasattr(module, 'main'):
                return {"main_output": module.main()}
            else:
                time.sleep(1.5)
                return {
                    "simulation": True,
                    "features": [
                        "Basic initialization patterns",
                        "OCR processing with structured output",
                        "Output structure analysis",
                        "Advanced visualization"
                    ]
                }
        except Exception as e:
            return {"error": str(e)}
    
    def _run_multilingual_demo(self, module, demo_type: str) -> Dict[str, Any]:
        """다국어 데모 실행"""
        if self.progress_callback:
            self.progress_callback("다국어 지원 테스트 중...")
        
        try:
            if hasattr(module, 'demonstrate_multilingual'):
                return {"multilingual_demo": module.demonstrate_multilingual()}
            elif hasattr(module, 'main'):
                return {"main_output": module.main()}
            else:
                time.sleep(2)
                return {
                    "simulation": True,
                    "supported_languages": 80,
                    "script_families": [
                        "Latin", "Chinese", "Japanese", "Korean", 
                        "Arabic", "Cyrillic", "Indic", "Other"
                    ],
                    "features": [
                        "Language support overview",
                        "Model zoo navigation", 
                        "Language-specific testing",
                        "Performance comparison"
                    ]
                }
        except Exception as e:
            return {"error": str(e)}
    
    def _run_modular_pipeline_demo(self, module, demo_type: str) -> Dict[str, Any]:
        """모듈러 파이프라인 데모 실행"""
        if self.progress_callback:
            self.progress_callback("모듈러 파이프라인 테스트 중...")
        
        try:
            if hasattr(module, 'demonstrate_modular_pipeline'):
                return {"pipeline_demo": module.demonstrate_modular_pipeline()}
            elif hasattr(module, 'main'):
                return {"main_output": module.main()}
            else:
                time.sleep(1.8)
                return {
                    "simulation": True,
                    "components": [
                        "Detection-only pipeline",
                        "Recognition-only pipeline", 
                        "Angle classification",
                        "Custom pipeline configuration"
                    ],
                    "configurations": [
                        "High accuracy server",
                        "Fast mobile",
                        "Detection focused"
                    ]
                }
        except Exception as e:
            return {"error": str(e)}
    
    def _run_performance_test_demo(self, module, demo_type: str) -> Dict[str, Any]:
        """성능 테스트 데모 실행"""
        if self.progress_callback:
            self.progress_callback("성능 테스트 실행 중...")
        
        try:
            if hasattr(module, 'run_performance_tests'):
                return {"performance_results": module.run_performance_tests()}
            elif hasattr(module, 'main'):
                return {"main_output": module.main()}
            else:
                time.sleep(3)  # 성능 테스트는 시간이 더 걸림
                return {
                    "simulation": True,
                    "test_categories": [
                        "Basic functionality validation",
                        "Performance benchmarking",
                        "Stress testing",
                        "Error recovery validation"
                    ],
                    "metrics": {
                        "processing_time": "측정됨",
                        "memory_usage": "모니터링됨", 
                        "accuracy": "평가됨",
                        "throughput": "벤치마킹됨"
                    }
                }
        except Exception as e:
            return {"error": str(e)}
    
    def execute_all_tutorials(self, progress_callback: Optional[Callable] = None) -> List[TutorialExecutionResult]:
        """모든 튜토리얼 순차 실행"""
        if progress_callback:
            self.set_progress_callback(progress_callback)
        
        results = []
        tutorial_ids = list(self.available_tutorials.keys())
        
        for i, tutorial_id in enumerate(tutorial_ids):
            if self.progress_callback:
                self.progress_callback(f"진행 중: {tutorial_id} ({i+1}/{len(tutorial_ids)})")
            
            result = self.execute_tutorial(tutorial_id)
            results.append(result)
            
            # 튜토리얼 간 짧은 간격
            time.sleep(0.5)
        
        if self.progress_callback:
            self.progress_callback(f"모든 튜토리얼 완료! ({len(results)}개)")
        
        return results

# 전역 래퍼 인스턴스
tutorial_wrapper = TutorialWrapper()

def get_tutorial_wrapper() -> TutorialWrapper:
    """튜토리얼 래퍼 인스턴스 반환"""
    return tutorial_wrapper