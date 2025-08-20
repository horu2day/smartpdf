#!/usr/bin/env python3
"""
PaddleOCR Tutorial Flet UI 실행 스크립트
====================================

이 스크립트는 PaddleOCR Tutorial Flet UI 애플리케이션을 실행합니다.

Usage:
    python run_flet_ui.py [options]

Options:
    --port PORT     웹 서버 포트 (기본값: 8551)
    --desktop       데스크톱 앱으로 실행
    --web           웹 브라우저로 실행 (기본값)
    --dev           개발 모드 (핫 리로드)
    --assets DIR    에셋 디렉터리 경로

Examples:
    python run_flet_ui.py                    # 웹 브라우저로 실행
    python run_flet_ui.py --desktop          # 데스크톱 앱으로 실행
    python run_flet_ui.py --port 8080        # 포트 8080으로 실행
    python run_flet_ui.py --dev              # 개발 모드로 실행
"""

import sys
import os
import argparse
from pathlib import Path

# 현재 디렉터리를 파이썬 패스에 추가
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def check_dependencies():
    """필수 의존성 확인"""
    missing_deps = []
    
    try:
        import flet
        print("OK: Flet UI framework available")
    except ImportError:
        missing_deps.append("flet")
    
    try:
        import cv2
        print("OK: OpenCV available")
    except ImportError:
        missing_deps.append("opencv-python")
    
    try:
        import numpy
        print("OK: NumPy available")
    except ImportError:
        missing_deps.append("numpy")
    
    try:
        from PIL import Image
        print("OK: Pillow available")
    except ImportError:
        missing_deps.append("Pillow")
    
    # PaddleOCR는 선택사항
    try:
        from paddleocr import PaddleOCR
        print("OK: PaddleOCR available (real OCR mode)")
    except ImportError:
        print("WARNING: PaddleOCR not available (simulation mode)")
    
    # Core OCR Engine 확인
    try:
        from core.ocr_engine import EnhancedOCREngine
        print("OK: Enhanced OCR Engine available")
    except ImportError:
        print("WARNING: Enhanced OCR Engine not available")
    
    if missing_deps:
        print("\nERROR: Missing required dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\nInstall command:")
        print(f"   pip install -r {current_dir}/requirements_flet.txt")
        print("   or")
        print(f"   pip install {' '.join(missing_deps)}")
        return False
    
    return True

def setup_environment():
    """환경 설정"""
    # CPU 모드 강제 설정 (GPU 관련 오류 방지)
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    
    # Assets 디렉터리 확인 및 생성
    assets_dir = current_dir / "assets"
    if not assets_dir.exists():
        assets_dir.mkdir(exist_ok=True)
        print(f"Created assets directory: {assets_dir}")
    
    # Results 디렉터리 확인 및 생성
    results_dir = current_dir / "results"
    if not results_dir.exists():
        results_dir.mkdir(exist_ok=True)
        print(f"Created results directory: {results_dir}")

def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(
        description="PaddleOCR Tutorial Flet UI 실행",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=8551,
        help="웹 서버 포트 (기본값: 8551)"
    )
    
    parser.add_argument(
        "--desktop",
        action="store_true",
        help="데스크톱 앱으로 실행"
    )
    
    parser.add_argument(
        "--web",
        action="store_true", 
        help="웹 브라우저로 실행 (기본값)"
    )
    
    parser.add_argument(
        "--dev",
        action="store_true",
        help="개발 모드 (핫 리로드)"
    )
    
    parser.add_argument(
        "--assets",
        type=str,
        default="assets",
        help="에셋 디렉터리 경로"
    )
    
    args = parser.parse_args()
    
    print("PaddleOCR Tutorial Flet UI")
    print("=" * 50)
    
    # 의존성 확인
    if not check_dependencies():
        print("\nERROR: Dependency check failed. Please install required packages.")
        sys.exit(1)
    
    # 환경 설정
    setup_environment()
    
    # Flet 앱 실행
    try:
        import flet as ft
        from flet_ui_app import main as app_main
        
        print(f"\nStarting application...")
        print(f"Working directory: {current_dir}")
        
        # 실행 모드 결정
        if args.desktop:
            view = ft.AppView.FLET_APP
            print(f"Running in desktop app mode")
        else:
            view = ft.AppView.WEB_BROWSER
            print(f"Running in web browser mode")
            print(f"URL: http://localhost:{args.port}")
        
        print("=" * 50)
        
        # Flet 앱 실행
        ft.app(
            target=app_main,
            view=view,
            port=args.port,
            assets_dir=args.assets,
            route_url_strategy="hash",
            web_renderer="html"  # 호환성을 위해 HTML 렌더러 사용
        )
        
    except ImportError as e:
        print(f"\nERROR: Failed to run Flet app: {e}")
        print("Check Flet installation: pip install flet")
        sys.exit(1)
    
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(0)
    
    except Exception as e:
        print(f"\nERROR: Application runtime error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()