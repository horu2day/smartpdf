#!/usr/bin/env python3
"""
Simple PaddleOCR Tutorial Flet UI
=================================

기본적인 Flet UI로 PaddleOCR 튜토리얼 기능을 제공하는 간단한 버전
호환성을 위해 최소한의 Flet 기능만 사용
"""

import flet as ft
import asyncio
import os
import sys
import time
import threading
from pathlib import Path
from datetime import datetime

# 현재 디렉터리를 시스템 패스에 추가
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# 간단한 결과 클래스
class SimpleResult:
    def __init__(self, title, status, duration, details=""):
        self.title = title
        self.status = status
        self.duration = duration
        self.details = details
        self.timestamp = datetime.now()

class SimplePaddleOCRApp:
    """간단한 PaddleOCR Tutorial UI"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "PaddleOCR Tutorial - Simple UI"
        self.page.window_width = 1200
        self.page.window_height = 800
        
        # 상태 변수
        self.is_processing = False
        self.results = []
        
        # UI 컴포넌트
        self.status_text = None
        self.log_container = None
        self.result_container = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """UI 설정"""
        
        # 헤더
        header = ft.Container(
            content=ft.Column([
                ft.Text("PaddleOCR Tutorial", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("완전한 OCR 튜토리얼 학습 도구", size=16),
                ft.Text(f"작업 디렉터리: {current_dir}", size=12)
            ]),
            padding=20,
            bgcolor="#E3F2FD",
            border_radius=10,
            margin=ft.margin.only(bottom=20)
        )
        
        # 상태 표시
        self.status_text = ft.Text("준비 완료", size=14, weight=ft.FontWeight.BOLD)
        
        # 튜토리얼 버튼들
        tutorial_buttons = ft.Row([
            ft.ElevatedButton(
                "섹션 2.3: CLI 예제",
                on_click=lambda e: self.run_tutorial("01_basic_cli"),
                bgcolor="#4CAF50",
                color="white"
            ),
            ft.ElevatedButton(
                "섹션 2.4: Python API",
                on_click=lambda e: self.run_tutorial("02_python_api"),
                bgcolor="#2196F3",
                color="white"
            ),
            ft.ElevatedButton(
                "섹션 3.1: 다국어",
                on_click=lambda e: self.run_tutorial("03_multilingual"),
                bgcolor="#FF9800",
                color="white"
            ),
            ft.ElevatedButton(
                "섹션 3.2: 모듈러",
                on_click=lambda e: self.run_tutorial("04_modular_pipeline"),
                bgcolor="#9C27B0",
                color="white"
            ),
            ft.ElevatedButton(
                "성능 테스트",
                on_click=lambda e: self.run_tutorial("05_performance_test"),
                bgcolor="#F44336",
                color="white"
            )
        ], wrap=True, spacing=10)
        
        # 전체 실행 버튼
        action_buttons = ft.Row([
            ft.ElevatedButton(
                "🚀 전체 튜토리얼 실행",
                on_click=self.run_all_tutorials,
                bgcolor="#673AB7",
                color="white",
                width=200,
                height=50
            ),
            ft.ElevatedButton(
                "📊 결과 요약",
                on_click=self.show_summary,
                bgcolor="#607D8B",
                color="white",
                width=150,
                height=50
            ),
            ft.ElevatedButton(
                "🔄 초기화",
                on_click=self.reset_app,
                bgcolor="#795548",
                color="white",
                width=150,
                height=50
            )
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        
        # 로그 영역
        self.log_container = ft.ListView(height=200, spacing=5, padding=10)
        log_section = ft.Container(
            content=ft.Column([
                ft.Text("실행 로그", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=self.log_container,
                    border=ft.border.all(1, "#CCCCCC"),
                    border_radius=5,
                    bgcolor="#000000",
                    padding=5
                )
            ]),
            margin=ft.margin.only(top=20, bottom=10)
        )
        
        # 결과 영역
        self.result_container = ft.ListView(height=250, spacing=10, padding=15)
        result_section = ft.Container(
            content=ft.Column([
                ft.Text("실행 결과", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=self.result_container,
                    border=ft.border.all(1, "#CCCCCC"),
                    border_radius=5,
                    bgcolor="#FAFAFA"
                )
            ]),
            margin=ft.margin.only(top=10)
        )
        
        # 전체 레이아웃
        main_content = ft.Column([
            header,
            self.status_text,
            ft.Text("📚 튜토리얼 섹션", size=18, weight=ft.FontWeight.BOLD),
            tutorial_buttons,
            action_buttons,
            log_section,
            result_section
        ], scroll=ft.ScrollMode.AUTO, spacing=15)
        
        self.page.add(main_content)
        
        # 초기 로그
        self.add_log("PaddleOCR Tutorial UI 시작됨", "info")
        self.add_log("시뮬레이션 모드로 실행 중", "warning")
    
    def add_log(self, message: str, level: str = "info"):
        """로그 추가"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        color_map = {
            "info": "#00FF00",
            "warning": "#FFA500", 
            "error": "#FF0000",
            "success": "#00BFFF"
        }
        
        log_entry = ft.Text(
            f"[{timestamp}] {message}",
            size=11,
            color=color_map.get(level, "#FFFFFF")
        )
        
        self.log_container.controls.append(log_entry)
        
        # 로그 개수 제한
        if len(self.log_container.controls) > 50:
            self.log_container.controls.pop(0)
        
        self.page.update()
    
    def update_status(self, message: str):
        """상태 업데이트"""
        self.status_text.value = f"상태: {message}"
        self.page.update()
    
    def run_tutorial(self, section_id: str):
        """단일 튜토리얼 실행"""
        if self.is_processing:
            self.add_log("이미 처리 중입니다", "warning")
            return
        
        self.is_processing = True
        self.update_status(f"실행 중: {section_id}")
        
        def tutorial_worker():
            try:
                start_time = time.time()
                self.add_log(f"튜토리얼 {section_id} 시작", "info")
                
                # 시뮬레이션 실행
                section_names = {
                    "01_basic_cli": "기본 CLI 예제",
                    "02_python_api": "Python API 사용법",
                    "03_multilingual": "다국어 지원",
                    "04_modular_pipeline": "모듈러 파이프라인",
                    "05_performance_test": "성능 테스트"
                }
                
                section_name = section_names.get(section_id, section_id)
                
                # 실행 시뮬레이션
                for i in range(3):
                    time.sleep(0.5)
                    self.add_log(f"{section_name} 처리 중... ({i+1}/3)", "info")
                
                duration = time.time() - start_time
                
                # 결과 생성
                result = SimpleResult(
                    title=f"섹션: {section_name}",
                    status="성공",
                    duration=duration,
                    details=f"시뮬레이션 모드로 실행 완료\n처리 시간: {duration:.2f}초"
                )
                
                self.results.append(result)
                self.add_log(f"{section_name} 완료! ({duration:.2f}초)", "success")
                self.update_result_display()
                
            except Exception as e:
                self.add_log(f"오류 발생: {str(e)}", "error")
            finally:
                self.is_processing = False
                self.update_status("대기 중")
        
        threading.Thread(target=tutorial_worker, daemon=True).start()
    
    def run_all_tutorials(self, e):
        """전체 튜토리얼 실행"""
        if self.is_processing:
            self.add_log("이미 처리 중입니다", "warning")
            return
        
        self.is_processing = True
        self.update_status("전체 튜토리얼 실행 중")
        
        def all_tutorial_worker():
            try:
                tutorials = ["01_basic_cli", "02_python_api", "03_multilingual", "04_modular_pipeline", "05_performance_test"]
                
                self.add_log("전체 튜토리얼 실행 시작", "info")
                
                for i, tutorial in enumerate(tutorials):
                    self.add_log(f"진행 중: {tutorial} ({i+1}/{len(tutorials)})", "info")
                    
                    start_time = time.time()
                    time.sleep(1.5)  # 시뮬레이션
                    duration = time.time() - start_time
                    
                    result = SimpleResult(
                        title=f"섹션: {tutorial}",
                        status="성공",
                        duration=duration,
                        details="전체 실행 모드에서 처리됨"
                    )
                    
                    self.results.append(result)
                    self.add_log(f"{tutorial} 완료", "success")
                
                self.add_log("전체 튜토리얼 실행 완료!", "success")
                self.update_result_display()
                
            except Exception as e:
                self.add_log(f"오류 발생: {str(e)}", "error")
            finally:
                self.is_processing = False
                self.update_status("대기 중")
        
        threading.Thread(target=all_tutorial_worker, daemon=True).start()
    
    def update_result_display(self):
        """결과 표시 업데이트"""
        self.result_container.controls.clear()
        
        if not self.results:
            self.result_container.controls.append(
                ft.Text("아직 실행된 튜토리얼이 없습니다", color="#666666")
            )
        else:
            for result in self.results:
                status_color = "#4CAF50" if result.status == "성공" else "#F44336"
                
                result_card = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(result.title, size=14, weight=ft.FontWeight.BOLD),
                            ft.Text(f"{result.duration:.2f}s", size=12, color="#666666")
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Text(result.details, size=12, color="#333333"),
                        ft.Text(f"실행 시간: {result.timestamp.strftime('%H:%M:%S')}", 
                               size=10, color="#999999")
                    ], spacing=5),
                    padding=10,
                    margin=5,
                    border=ft.border.all(1, status_color),
                    border_radius=5,
                    bgcolor="#FFFFFF"
                )
                self.result_container.controls.append(result_card)
        
        self.page.update()
    
    def show_summary(self, e):
        """결과 요약 표시"""
        if not self.results:
            self.add_log("표시할 결과가 없습니다", "warning")
            return
        
        total_duration = sum(r.duration for r in self.results)
        success_count = sum(1 for r in self.results if r.status == "성공")
        
        summary = f"""
📊 실행 요약:
- 총 실행 섹션: {len(self.results)}개
- 성공: {success_count}개
- 총 소요 시간: {total_duration:.2f}초
- 평균 시간: {total_duration/len(self.results):.2f}초
"""
        self.add_log("=== 요약 리포트 ===", "info")
        for line in summary.strip().split('\n'):
            if line.strip():
                self.add_log(line.strip(), "info")
    
    def reset_app(self, e):
        """애플리케이션 초기화"""
        self.results.clear()
        self.result_container.controls.clear()
        self.log_container.controls.clear()
        
        self.add_log("애플리케이션이 초기화되었습니다", "info")
        self.update_status("초기화 완료")
        self.page.update()

def main(page: ft.Page):
    """메인 애플리케이션 진입점"""
    SimplePaddleOCRApp(page)

if __name__ == "__main__":
    print("Starting Simple PaddleOCR Tutorial UI...")
    print("URL: http://localhost:8552")
    print("=" * 50)
    
    try:
        ft.app(
            target=main, 
            view=ft.AppView.WEB_BROWSER,
            port=8552
        )
    except Exception as e:
        print(f"Error running app: {e}")
        import traceback
        traceback.print_exc()