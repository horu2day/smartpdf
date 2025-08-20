#!/usr/bin/env python3
"""
의존성 테스트 스크립트
==================

PaddleOCR Tutorial Flet UI에 필요한 의존성을 확인하는 스크립트
"""

import sys
import os
from pathlib import Path

def test_dependencies():
    """의존성 테스트"""
    print("="*50)
    print("PaddleOCR Tutorial Flet UI - 의존성 테스트")
    print("="*50)
    
    print(f"Python 버전: {sys.version}")
    print(f"현재 디렉터리: {Path.cwd()}")
    print()
    
    # 필수 의존성 확인
    required_deps = [
        ('flet', 'Flet UI 프레임워크'),
        ('numpy', 'NumPy'),
        ('cv2', 'OpenCV'),
        ('PIL', 'Pillow')
    ]
    
    print("필수 의존성 확인:")
    required_available = True
    
    for module, name in required_deps:
        try:
            __import__(module)
            print(f"  ✓ {name}: 사용 가능")
        except ImportError as e:
            print(f"  ✗ {name}: 사용 불가")
            print(f"    오류: {e}")
            required_available = False
    
    print()
    
    # 선택적 의존성
    optional_deps = [
        ('paddleocr', 'PaddleOCR'),
        ('matplotlib', 'Matplotlib'),
        ('PyPDF2', 'PyPDF2')
    ]
    
    print("선택적 의존성 확인:")
    for module, name in optional_deps:
        try:
            __import__(module)
            print(f"  ✓ {name}: 사용 가능")
        except ImportError:
            print(f"  - {name}: 사용 불가 (시뮬레이션 모드)")
    
    print()
    
    # 프로젝트 구조 확인
    print("프로젝트 구조 확인:")
    files_to_check = [
        'flet_ui_app.py',
        'tutorial_wrapper.py', 
        'performance_visualizer.py',
        'run_flet_ui.py',
        'core/ocr_engine.py',
        'examples/01_basic_cli.py'
    ]
    
    for file_path in files_to_check:
        full_path = Path(file_path)
        if full_path.exists():
            print(f"  ✓ {file_path}: 존재")
        else:
            print(f"  ✗ {file_path}: 없음")
    
    print()
    
    # 설치 가이드
    if not required_available:
        print("❌ 필수 의존성이 누락되었습니다!")
        print()
        print("설치 명령:")
        print("  pip install flet opencv-python pillow numpy")
        print("  또는")
        print("  pip install -r requirements_flet.txt")
        print()
        return False
    else:
        print("✅ 모든 필수 의존성이 준비되었습니다!")
        print()
        print("실행 명령:")
        print("  python run_flet_ui.py")
        print("  python run_flet_ui.py --desktop")
        print()
        return True

if __name__ == "__main__":
    success = test_dependencies()
    
    if success:
        print("🎉 Flet UI 애플리케이션을 실행할 준비가 완료되었습니다!")
    else:
        print("⚠️ 의존성을 먼저 설치해주세요.")
        
    print("="*50)