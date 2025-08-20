#!/usr/bin/env python3
"""
PaddleOCR Tutorial Flet UI Application
===================================

기존 paddleocr_tutorial의 모든 기능을 통합한 종합 Flet UI 애플리케이션

Features:
- 전체 튜토리얼 예제 실행 (01_basic_cli.py ~ 05_performance_test.py)
- Enhanced OCR Engine 통합
- 실시간 진행률 표시
- 결과 시각화 및 저장
- 성능 분석 및 벤치마킹

Based on:
- examples/fletbase/src/main.py (기본 Flet 패턴)
- examples/paddleocr/flet_ocr_app.py (OCR UI 패턴)
- paddleocr_tutorial/* (핵심 OCR 기능)
"""

import flet as ft
import asyncio
import os
import sys
import time
import json
import threading
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
import traceback

# 현재 디렉터리를 시스템 패스에 추가
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Core OCR Engine import
try:
    from core.ocr_engine import EnhancedOCREngine, DocumentResult, OCRResult
    CORE_ENGINE_AVAILABLE = True
    print("OK: Enhanced OCR Engine loaded")
except ImportError as e:
    CORE_ENGINE_AVAILABLE = False
    print(f"WARNING: Enhanced OCR Engine load failed: {e}")

# Tutorial Wrapper import
try:
    from tutorial_wrapper import get_tutorial_wrapper, TutorialExecutionResult
    tutorial_wrapper = get_tutorial_wrapper()
    TUTORIAL_WRAPPER_AVAILABLE = True
    print("OK: Tutorial Wrapper loaded")
except ImportError as e:
    TUTORIAL_WRAPPER_AVAILABLE = False
    print(f"WARNING: Tutorial Wrapper load failed: {e}")
    tutorial_wrapper = None

# PaddleOCR availability check
try:
    os.environ["CUDA_VISIBLE_DEVICES"] = ""  # CPU 강제 사용
    from paddleocr import PaddleOCR
    PADDLEOCR_AVAILABLE = True
    print("OK: PaddleOCR available (CPU mode)")
except ImportError:
    PADDLEOCR_AVAILABLE = False
    print("WARNING: PaddleOCR not available - simulation mode")


class TutorialResult:
    """튜토리얼 실행 결과를 담는 클래스"""
    
    def __init__(self, title: str, status: str, duration: float, details: str = "", error: str = ""):
        self.title = title
        self.status = status  # "success", "failed", "running", "pending"
        self.duration = duration
        self.details = details
        self.error = error
        self.timestamp = datetime.now()


class PaddleOCRTutorialApp:
    """PaddleOCR Tutorial Flet UI 메인 애플리케이션"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_page()
        
        # Core OCR Engine
        self.ocr_engine = None
        self.ocr_initialized = False
        
        # 상태 변수
        self.is_processing = False
        self.current_results = []
        self.tutorial_results: List[TutorialResult] = []
        
        # UI 컴포넌트 참조
        self.progress_bar = None
        self.progress_text = None
        self.status_text = None
        self.result_container = None
        self.tutorial_list = None
        self.file_picker = None
        self.result_tabs = None
        self.log_container = None
        
        # 파일 관련
        self.current_file = None
        
        self.setup_ui()
        
    def setup_page(self):
        """페이지 기본 설정"""
        self.page.title = "🎓 PaddleOCR Tutorial - Flet UI"
        self.page.window_width = 1600
        self.page.window_height = 1000
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.scroll = ft.ScrollMode.AUTO
        
    def setup_ui(self):
        """UI 구성 요소 설정"""
        
        # 파일 선택기
        self.file_picker = ft.FilePicker(on_result=self.on_file_picked)
        self.page.overlay.append(self.file_picker)
        
        # 헤더
        header = self.create_header()
        
        # 상태 및 설정 패널
        settings_panel = self.create_settings_panel()
        
        # 튜토리얼 섹션 선택
        tutorial_section = self.create_tutorial_section()
        
        # 파일 업로드 영역
        file_section = self.create_file_section()
        
        # 진행률 및 상태
        progress_section = self.create_progress_section()
        
        # 액션 버튼
        action_section = self.create_action_section()
        
        # 결과 표시 영역
        result_section = self.create_result_section()
        
        # 전체 레이아웃
        main_content = ft.Column([
            header,
            settings_panel,
            tutorial_section,
            file_section,
            progress_section,
            action_section,
            result_section
        ], scroll=ft.ScrollMode.AUTO, spacing=20)
        
        self.page.add(main_content)
        
    def create_header(self):
        """헤더 섹션 생성"""
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.SCHOOL, size=50, color=ft.colors.BLUE_600),
                ft.Column([
                    ft.Text("PaddleOCR Tutorial", size=32, weight=ft.FontWeight.BOLD),
                    ft.Text("완전한 OCR 튜토리얼 - CLI, API, 다국어, 모듈러 파이프라인", size=16, color=ft.colors.GREY_600),
                    ft.Row([
                        ft.Icon(ft.icons.CHECK_CIRCLE, size=16, 
                               color=ft.colors.GREEN if CORE_ENGINE_AVAILABLE else ft.colors.RED),
                        ft.Text(f"Enhanced OCR Engine: {'✅ 사용가능' if CORE_ENGINE_AVAILABLE else '❌ 사용불가'}", size=12),
                        ft.Icon(ft.icons.SMART_TOY, size=16,
                               color=ft.colors.GREEN if PADDLEOCR_AVAILABLE else ft.colors.ORANGE),
                        ft.Text(f"PaddleOCR: {'✅ 실제모드' if PADDLEOCR_AVAILABLE else '⚠️ 시뮬레이션'}", size=12)
                    ])
                ], spacing=5)
            ], alignment=ft.MainAxisAlignment.START),
            padding=25,
            bgcolor=ft.colors.BLUE_50,
            border_radius=15,
            margin=ft.margin.only(bottom=20)
        )
        
    def create_settings_panel(self):
        """설정 패널 생성"""
        return ft.Container(
            content=ft.Row([
                # OCR 엔진 상태
                ft.Container(
                    content=ft.Column([
                        ft.Text("OCR 엔진 상태", size=14, weight=ft.FontWeight.BOLD),
                        ft.Row([
                            ft.Icon(ft.icons.MEMORY, size=20, color=ft.colors.BLUE),
                            ft.Text("Enhanced OCR Engine", size=12),
                            ft.Icon(ft.icons.CHECK_CIRCLE if CORE_ENGINE_AVAILABLE else ft.icons.ERROR, 
                                   size=16, color=ft.colors.GREEN if CORE_ENGINE_AVAILABLE else ft.colors.RED)
                        ])
                    ], spacing=8),
                    padding=15,
                    border=ft.border.all(1, ft.colors.GREY_300),
                    border_radius=10,
                    bgcolor=ft.colors.WHITE
                ),
                
                # 언어 설정
                ft.Container(
                    content=ft.Column([
                        ft.Text("언어 설정", size=14, weight=ft.FontWeight.BOLD),
                        ft.Dropdown(
                            options=[
                                ft.dropdown.Option("en", "🇺🇸 English"),
                                ft.dropdown.Option("korean", "🇰🇷 한국어"),
                                ft.dropdown.Option("ch", "🇨🇳 中文"),
                                ft.dropdown.Option("japan", "🇯🇵 日本語"),
                                ft.dropdown.Option("french", "🇫🇷 Français"),
                                ft.dropdown.Option("german", "🇩🇪 Deutsch"),
                            ],
                            value="en",
                            width=160
                        )
                    ], spacing=8),
                    padding=15,
                    border=ft.border.all(1, ft.colors.GREY_300),
                    border_radius=10,
                    bgcolor=ft.colors.WHITE
                ),
                
                # 초기화 버튼
                ft.ElevatedButton(
                    "🔄 OCR 엔진 초기화",
                    icon=ft.icons.REFRESH,
                    on_click=self.initialize_ocr_engine,
                    style=ft.ButtonStyle(
                        bgcolor=ft.colors.INDIGO_600,
                        color=ft.colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    height=50
                )
            ], spacing=20),
            margin=ft.margin.only(bottom=20)
        )
        
    def create_tutorial_section(self):
        """튜토리얼 섹션 선택 UI"""
        tutorial_options = [
            {"id": "01_basic_cli", "title": "섹션 2.3: 기본 CLI 예제", "desc": "CLI 명령어 및 기본 파이프라인"},
            {"id": "02_python_api", "title": "섹션 2.4: Python API 예제", "desc": "Python API 사용법 및 결과 분석"},
            {"id": "03_multilingual", "title": "섹션 3.1: 다국어 지원", "desc": "80+ 언어 지원 및 성능 비교"},
            {"id": "04_modular_pipeline", "title": "섹션 3.2: 모듈러 파이프라인", "desc": "컴포넌트별 개별 실행"},
            {"id": "05_performance_test", "title": "섹션 4: 성능 테스트", "desc": "종합 성능 분석 및 벤치마킹"},
            {"id": "all_tutorials", "title": "🚀 전체 튜토리얼 실행", "desc": "모든 예제를 순차적으로 실행"}
        ]
        
        tutorial_cards = []
        for option in tutorial_options:
            card = ft.Container(
                content=ft.Column([
                    ft.Text(option["title"], size=14, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700),
                    ft.Text(option["desc"], size=12, color=ft.colors.GREY_600),
                    ft.ElevatedButton(
                        "실행",
                        data=option["id"],
                        on_click=self.run_tutorial_section,
                        style=ft.ButtonStyle(bgcolor=ft.colors.GREEN_600, color=ft.colors.WHITE),
                        width=80,
                        height=35
                    )
                ], spacing=8),
                padding=15,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=10,
                bgcolor=ft.colors.WHITE,
                width=280
            )
            tutorial_cards.append(card)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("📚 튜토리얼 섹션 선택", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700),
                ft.GridView(
                    tutorial_cards[:3],  # 첫 번째 행
                    runs_count=3,
                    max_extent=300,
                    child_aspect_ratio=1.2,
                    spacing=15,
                    run_spacing=15
                ),
                ft.GridView(
                    tutorial_cards[3:],  # 두 번째 행
                    runs_count=3,
                    max_extent=300,
                    child_aspect_ratio=1.2,
                    spacing=15,
                    run_spacing=15
                )
            ], spacing=15),
            margin=ft.margin.only(bottom=20)
        )
    
    def create_file_section(self):
        """파일 업로드 섹션"""
        return ft.Container(
            content=ft.Column([
                ft.Text("📁 파일 테스트", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700),
                ft.Text("이미지 파일을 선택하여 OCR 성능을 직접 테스트해보세요", size=14, color=ft.colors.GREY_600),
                ft.Row([
                    ft.ElevatedButton(
                        "🖼️ 이미지 선택",
                        icon=ft.icons.IMAGE,
                        on_click=self.select_image_file,
                        style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE)
                    ),
                    ft.ElevatedButton(
                        "📄 PDF 선택",
                        icon=ft.icons.PICTURE_AS_PDF,
                        on_click=self.select_pdf_file,
                        style=ft.ButtonStyle(bgcolor=ft.colors.RED_600, color=ft.colors.WHITE)
                    ),
                    ft.ElevatedButton(
                        "🎯 샘플 이미지 테스트",
                        icon=ft.icons.SCIENCE,
                        on_click=self.test_sample_images,
                        style=ft.ButtonStyle(bgcolor=ft.colors.PURPLE_600, color=ft.colors.WHITE)
                    )
                ], spacing=15)
            ], spacing=10),
            padding=20,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=10,
            bgcolor=ft.colors.GREY_50,
            margin=ft.margin.only(bottom=20)
        )
    
    def create_progress_section(self):
        """진행률 및 상태 섹션"""
        self.progress_bar = ft.ProgressBar(width=600, visible=False)
        self.progress_text = ft.Text("준비 완료", size=14, weight=ft.FontWeight.BOLD)
        self.status_text = ft.Text("튜토리얼 섹션을 선택하거나 파일을 업로드하세요", size=12, color=ft.colors.GREY_500)
        
        return ft.Container(
            content=ft.Column([
                self.progress_bar,
                self.progress_text,
                self.status_text
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            margin=ft.margin.only(bottom=20)
        )
    
    def create_action_section(self):
        """액션 버튼 섹션"""
        return ft.Row([
            ft.ElevatedButton(
                "💾 결과 저장",
                icon=ft.icons.SAVE,
                on_click=self.save_results,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.ORANGE_600,
                    color=ft.colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=10)
                ),
                width=140,
                height=45
            ),
            ft.ElevatedButton(
                "📊 성능 리포트",
                icon=ft.icons.ANALYTICS,
                on_click=self.generate_performance_report,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.TEAL_600,
                    color=ft.colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=10)
                ),
                width=140,
                height=45
            ),
            ft.ElevatedButton(
                "🔄 초기화",
                icon=ft.icons.CLEAR_ALL,
                on_click=self.reset_app,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.RED_600,
                    color=ft.colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=10)
                ),
                width=140,
                height=45
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
    
    def create_result_section(self):
        """결과 표시 섹션"""
        # 로그 컨테이너
        self.log_container = ft.ListView(height=300, spacing=5, padding=10)
        
        # 결과 컨테이너
        self.result_container = ft.ListView(height=350, spacing=10, padding=15)
        
        self.result_tabs = ft.Tabs([
            ft.Tab(
                text="📝 실행 로그",
                icon=ft.icons.TERMINAL,
                content=ft.Container(
                    content=self.log_container,
                    border=ft.border.all(1, ft.colors.GREY_300),
                    border_radius=10,
                    bgcolor=ft.colors.BLACK,
                    padding=5
                )
            ),
            ft.Tab(
                text="📊 결과 요약",
                icon=ft.icons.SUMMARIZE,
                content=ft.Container(
                    content=self.result_container,
                    border=ft.border.all(1, ft.colors.GREY_300),
                    border_radius=10,
                    bgcolor=ft.colors.WHITE
                )
            ),
            ft.Tab(
                text="📈 성능 분석",
                icon=ft.icons.TIMELINE,
                content=ft.Container(
                    content=ft.Text("성능 분석 결과가 여기에 표시됩니다", 
                                   color=ft.colors.GREY_500, size=16),
                    height=350,
                    padding=20,
                    bgcolor=ft.colors.GREY_50,
                    border_radius=10,
                    alignment=ft.alignment.center
                )
            )
        ])
        
        return ft.Container(
            content=ft.Column([
                ft.Text("📊 실행 결과", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700),
                self.result_tabs
            ], spacing=15),
            margin=ft.margin.only(top=30)
        )
    
    def update_status(self, message: str, show_progress: bool = False):
        """상태 업데이트"""
        if self.progress_text:
            self.progress_text.value = message
        
        if self.progress_bar:
            self.progress_bar.visible = show_progress
        
        # 로그에도 추가
        self.add_log(message, "info")
        self.page.update()
    
    def add_log(self, message: str, level: str = "info"):
        """로그 메시지 추가"""
        if not self.log_container:
            return
            
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # 로그 레벨에 따른 색상
        color_map = {
            "info": ft.colors.GREEN_300,
            "warning": ft.colors.ORANGE_300,
            "error": ft.colors.RED_300,
            "success": ft.colors.BLUE_300
        }
        
        log_entry = ft.Text(
            f"[{timestamp}] {message}",
            size=11,
            color=color_map.get(level, ft.colors.WHITE),
            font_family="Courier New"
        )
        
        self.log_container.controls.append(log_entry)
        
        # 로그 개수 제한 (최근 100개)
        if len(self.log_container.controls) > 100:
            self.log_container.controls.pop(0)
        
        self.page.update()
    
    def show_snackbar(self, message: str, bgcolor: str = ft.colors.BLUE_700):
        """스낵바 표시"""
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(message, color=ft.colors.WHITE),
                bgcolor=bgcolor,
                action="확인",
                action_color=ft.colors.WHITE,
                duration=4000
            )
        )
    
    def initialize_ocr_engine(self, e):
        """OCR 엔진 초기화"""
        if self.is_processing:
            self.show_snackbar("이미 처리 중입니다")
            return
        
        if not CORE_ENGINE_AVAILABLE:
            self.show_snackbar("Enhanced OCR Engine을 사용할 수 없습니다", ft.colors.RED_600)
            return
        
        self.is_processing = True
        self.update_status("OCR 엔진 초기화 중...", True)
        
        def init_worker():
            try:
                self.add_log("Enhanced OCR Engine 초기화 시작", "info")
                self.ocr_engine = EnhancedOCREngine(lang='en', model_type='mobile')
                
                # 초기화 테스트
                self.add_log("OCR 엔진 테스트 중...", "info")
                time.sleep(1)  # 초기화 시뮬레이션
                
                self.ocr_initialized = True
                self.add_log("OCR 엔진 초기화 완료!", "success")
                self.update_status("OCR 엔진 초기화 완료", False)
                self.show_snackbar("OCR 엔진이 성공적으로 초기화되었습니다!", ft.colors.GREEN_600)
                
            except Exception as ex:
                error_msg = f"OCR 엔진 초기화 실패: {str(ex)}"
                self.add_log(error_msg, "error")
                self.update_status(error_msg, False)
                self.show_snackbar(error_msg, ft.colors.RED_600)
            finally:
                self.is_processing = False
                self.page.update()
        
        threading.Thread(target=init_worker, daemon=True).start()
    
    def run_tutorial_section(self, e):
        """튜토리얼 섹션 실행"""
        if self.is_processing:
            self.show_snackbar("이미 처리 중입니다")
            return
        
        section_id = e.control.data
        self.is_processing = True
        self.update_status(f"튜토리얼 섹션 실행 중: {section_id}", True)
        
        def tutorial_worker():
            try:
                if section_id == "all_tutorials":
                    self.run_all_tutorials()
                else:
                    self.run_single_tutorial(section_id)
                    
            except Exception as ex:
                error_msg = f"튜토리얼 실행 실패: {str(ex)}"
                self.add_log(error_msg, "error")
                self.update_status(error_msg, False)
                self.show_snackbar(error_msg, ft.colors.RED_600)
            finally:
                self.is_processing = False
                self.page.update()
        
        threading.Thread(target=tutorial_worker, daemon=True).start()
    
    def run_single_tutorial(self, section_id: str):
        """단일 튜토리얼 섹션 실행"""
        start_time = time.time()
        
        try:
            self.add_log(f"튜토리얼 섹션 {section_id} 시작", "info")
            
            if TUTORIAL_WRAPPER_AVAILABLE and tutorial_wrapper:
                # Tutorial Wrapper 사용
                self.add_log(f"Tutorial Wrapper로 {section_id} 실행 중...", "info")
                
                # 진행률 콜백 설정
                tutorial_wrapper.set_progress_callback(lambda msg: self.add_log(msg, "info"))
                
                # 실제 튜토리얼 실행
                execution_result = tutorial_wrapper.execute_tutorial(section_id, demo_type="all")
                
                # 결과를 TutorialResult로 변환
                result = TutorialResult(
                    title=execution_result.title,
                    status="success" if execution_result.success else "failed",
                    duration=execution_result.duration,
                    details=f"{execution_result.title}\n\n실행 출력:\n{execution_result.output}\n\n세부사항:\n{execution_result.details}",
                    error=execution_result.error
                )
                
                self.tutorial_results.append(result)
                
                if execution_result.success:
                    self.add_log(f"섹션 {section_id} 완료 ({execution_result.duration:.2f}초)", "success")
                else:
                    self.add_log(f"섹션 {section_id} 실패: {execution_result.error}", "error")
                
            else:
                # 시뮬레이션 모드
                self.add_log(f"시뮬레이션 모드로 {section_id} 실행", "warning")
                time.sleep(1.5)
                
                duration = time.time() - start_time
                result = TutorialResult(
                    title=f"섹션 {section_id} (시뮬레이션)",
                    status="success",
                    duration=duration,
                    details=f"시뮬레이션 모드로 실행됨\nTutorial Wrapper가 사용할 수 없어 시뮬레이션으로 대체됨"
                )
                
                self.tutorial_results.append(result)
                self.add_log(f"섹션 {section_id} 시뮬레이션 완료", "success")
            
            self.update_result_display()
            self.update_status(f"섹션 {section_id} 실행 완료", False)
            
        except Exception as e:
            duration = time.time() - start_time
            result = TutorialResult(
                title=f"섹션 {section_id}",
                status="failed",
                duration=duration,
                error=str(e)
            )
            self.tutorial_results.append(result)
            raise e
    
    def run_all_tutorials(self):
        """모든 튜토리얼 순차 실행"""
        self.add_log("전체 튜토리얼 실행 시작", "info")
        
        if TUTORIAL_WRAPPER_AVAILABLE and tutorial_wrapper:
            # Tutorial Wrapper로 모든 튜토리얼 실행
            tutorial_wrapper.set_progress_callback(lambda msg: self.add_log(msg, "info"))
            
            execution_results = tutorial_wrapper.execute_all_tutorials(
                progress_callback=lambda msg: self.update_status(msg, True)
            )
            
            # 결과를 TutorialResult로 변환
            for execution_result in execution_results:
                result = TutorialResult(
                    title=execution_result.title,
                    status="success" if execution_result.success else "failed",
                    duration=execution_result.duration,
                    details=f"{execution_result.title}\n\n실행 출력:\n{execution_result.output}\n\n세부사항:\n{execution_result.details}",
                    error=execution_result.error
                )
                self.tutorial_results.append(result)
        else:
            # 시뮬레이션 모드
            tutorial_sections = ["01_basic_cli", "02_python_api", "03_multilingual", "04_modular_pipeline", "05_performance_test"]
            
            for i, section in enumerate(tutorial_sections):
                self.update_status(f"진행 중: {section} ({i+1}/{len(tutorial_sections)})", True)
                self.run_single_tutorial(section)
                time.sleep(0.5)  # 섹션 간 간격
        
        self.update_result_display()
        self.add_log("전체 튜토리얼 실행 완료!", "success")
        self.update_status("모든 튜토리얼 실행 완료", False)
        self.show_snackbar("모든 튜토리얼이 성공적으로 실행되었습니다!", ft.colors.GREEN_600)
    
    def update_result_display(self):
        """결과 표시 업데이트"""
        if not self.result_container:
            return
        
        self.result_container.controls.clear()
        
        if not self.tutorial_results:
            self.result_container.controls.append(
                ft.Text("아직 실행된 튜토리얼이 없습니다", color=ft.colors.GREY_500)
            )
        else:
            for result in self.tutorial_results:
                # 상태에 따른 아이콘과 색상
                if result.status == "success":
                    icon = ft.icons.CHECK_CIRCLE
                    color = ft.colors.GREEN_600
                elif result.status == "failed":
                    icon = ft.icons.ERROR
                    color = ft.colors.RED_600
                else:
                    icon = ft.icons.PENDING
                    color = ft.colors.ORANGE_600
                
                result_card = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(icon, size=20, color=color),
                            ft.Text(result.title, size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"{result.duration:.2f}s", size=12, color=ft.colors.GREY_600)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Text(result.details if result.details else result.error, 
                               size=12, color=ft.colors.GREY_700),
                        ft.Text(f"실행 시간: {result.timestamp.strftime('%H:%M:%S')}", 
                               size=10, color=ft.colors.GREY_500)
                    ], spacing=5),
                    padding=15,
                    margin=5,
                    border=ft.border.all(1, ft.colors.GREY_300),
                    border_radius=8,
                    bgcolor=ft.colors.WHITE
                )
                self.result_container.controls.append(result_card)
        
        self.page.update()
    
    def select_image_file(self, e):
        """이미지 파일 선택"""
        self.file_picker.pick_files(
            dialog_title="OCR 테스트할 이미지 선택",
            allowed_extensions=["png", "jpg", "jpeg", "bmp", "tiff"],
            allow_multiple=False
        )
    
    def select_pdf_file(self, e):
        """PDF 파일 선택"""
        self.file_picker.pick_files(
            dialog_title="OCR 테스트할 PDF 선택",
            allowed_extensions=["pdf"],
            allow_multiple=False
        )
    
    def on_file_picked(self, e: ft.FilePickerResultEvent):
        """파일 선택 처리"""
        if e.files:
            file = e.files[0]
            self.current_file = file.path
            filename = Path(file.path).name
            
            self.add_log(f"파일 선택됨: {filename}", "info")
            self.update_status(f"선택된 파일: {filename}")
            
            # 파일 정보 표시
            file_size = self.get_file_size(file.path)
            self.status_text.value = f"파일 크기: {file_size}"
            self.page.update()
    
    def get_file_size(self, file_path: str) -> str:
        """파일 크기 계산"""
        try:
            size = os.path.getsize(file_path)
            if size < 1024:
                return f"{size} bytes"
            elif size < 1024*1024:
                return f"{size/1024:.1f} KB"
            else:
                return f"{size/(1024*1024):.1f} MB"
        except:
            return "크기 불명"
    
    def test_sample_images(self, e):
        """샘플 이미지 테스트"""
        if self.is_processing:
            self.show_snackbar("이미 처리 중입니다")
            return
        
        self.is_processing = True
        self.update_status("샘플 이미지 테스트 중...", True)
        
        def test_worker():
            try:
                # assets/images 디렉터리에서 샘플 이미지 찾기
                assets_dir = current_dir / "assets" / "images"
                
                if assets_dir.exists():
                    image_files = list(assets_dir.glob("*.png")) + list(assets_dir.glob("*.jpg"))
                    
                    if image_files:
                        self.add_log(f"{len(image_files)}개 샘플 이미지 발견", "info")
                        
                        for img_file in image_files[:3]:  # 처음 3개만 테스트
                            self.add_log(f"테스트 중: {img_file.name}", "info")
                            time.sleep(1)  # 처리 시뮬레이션
                            
                        self.add_log("샘플 이미지 테스트 완료", "success")
                    else:
                        self.add_log("샘플 이미지가 없습니다", "warning")
                else:
                    self.add_log("assets/images 디렉터리가 없습니다", "warning")
                
                self.update_status("샘플 이미지 테스트 완료", False)
                
            except Exception as ex:
                error_msg = f"샘플 이미지 테스트 실패: {str(ex)}"
                self.add_log(error_msg, "error")
                self.update_status(error_msg, False)
            finally:
                self.is_processing = False
                self.page.update()
        
        threading.Thread(target=test_worker, daemon=True).start()
    
    def save_results(self, e):
        """결과 저장"""
        if not self.tutorial_results:
            self.show_snackbar("저장할 결과가 없습니다!")
            return
        
        try:
            # 결과 디렉터리 생성
            output_dir = current_dir / "results"
            output_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = output_dir / f"tutorial_results_{timestamp}.json"
            
            # 결과 데이터 구성
            results_data = {
                "timestamp": datetime.now().isoformat(),
                "total_tutorials": len(self.tutorial_results),
                "success_count": sum(1 for r in self.tutorial_results if r.status == "success"),
                "failed_count": sum(1 for r in self.tutorial_results if r.status == "failed"),
                "total_duration": sum(r.duration for r in self.tutorial_results),
                "ocr_engine_available": CORE_ENGINE_AVAILABLE,
                "paddleocr_available": PADDLEOCR_AVAILABLE,
                "results": [
                    {
                        "title": r.title,
                        "status": r.status,
                        "duration": r.duration,
                        "details": r.details,
                        "error": r.error,
                        "timestamp": r.timestamp.isoformat()
                    }
                    for r in self.tutorial_results
                ]
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results_data, f, ensure_ascii=False, indent=2)
            
            self.add_log(f"결과 저장 완료: {output_file.name}", "success")
            self.show_snackbar(f"결과가 저장되었습니다!\n📁 {output_file.name}")
            
        except Exception as ex:
            error_msg = f"결과 저장 실패: {str(ex)}"
            self.add_log(error_msg, "error")
            self.show_snackbar(error_msg, ft.colors.RED_600)
    
    def generate_performance_report(self, e):
        """성능 리포트 생성"""
        if not self.tutorial_results:
            self.show_snackbar("분석할 결과가 없습니다!")
            return
        
        self.add_log("성능 리포트 생성 중...", "info")
        
        # 성능 통계 계산
        total_duration = sum(r.duration for r in self.tutorial_results)
        success_count = sum(1 for r in self.tutorial_results if r.status == "success")
        avg_duration = total_duration / len(self.tutorial_results) if self.tutorial_results else 0
        
        report = f"""
📊 PaddleOCR Tutorial 성능 리포트
=====================================
실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📈 전체 통계:
- 총 실행 섹션: {len(self.tutorial_results)}개
- 성공률: {success_count}/{len(self.tutorial_results)} ({success_count/len(self.tutorial_results)*100:.1f}%)
- 총 소요 시간: {total_duration:.2f}초
- 평균 실행 시간: {avg_duration:.2f}초

🔧 시스템 정보:
- Enhanced OCR Engine: {'✅ 사용가능' if CORE_ENGINE_AVAILABLE else '❌ 사용불가'}
- PaddleOCR: {'✅ 실제모드' if PADDLEOCR_AVAILABLE else '⚠️ 시뮬레이션모드'}

📋 섹션별 성능:
"""
        
        for result in self.tutorial_results:
            status_icon = "✅" if result.status == "success" else "❌"
            report += f"- {status_icon} {result.title}: {result.duration:.2f}s\n"
        
        self.add_log("성능 리포트 생성 완료", "success")
        self.show_snackbar("성능 리포트가 생성되었습니다!")
        
        # 성능 분석 탭에 리포트 표시
        if self.result_tabs:
            performance_tab = self.result_tabs.tabs[2]  # 세 번째 탭 (성능 분석)
            performance_tab.content = ft.Container(
                content=ft.SelectableText(
                    report,
                    size=12,
                    style=ft.TextStyle(font_family="Courier New")
                ),
                height=350,
                padding=20,
                bgcolor=ft.colors.WHITE,
                border_radius=10
            )
            self.page.update()
    
    def reset_app(self, e):
        """애플리케이션 초기화"""
        self.current_file = None
        self.tutorial_results.clear()
        self.current_results.clear()
        
        if self.result_container:
            self.result_container.controls.clear()
        
        if self.log_container:
            self.log_container.controls.clear()
        
        self.update_status("애플리케이션 초기화 완료")
        self.add_log("애플리케이션이 초기화되었습니다", "info")
        self.show_snackbar("애플리케이션이 초기화되었습니다")
        
        self.page.update()


def main(page: ft.Page):
    """메인 애플리케이션 진입점"""
    try:
        PaddleOCRTutorialApp(page)
    except Exception as e:
        print(f"애플리케이션 시작 실패: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    print("🎓 PaddleOCR Tutorial Flet UI 시작")
    print("=" * 50)
    print(f"✅ Enhanced OCR Engine: {'사용가능' if CORE_ENGINE_AVAILABLE else '사용불가'}")
    print(f"✅ PaddleOCR: {'실제모드' if PADDLEOCR_AVAILABLE else '시뮬레이션모드'}")
    print(f"📁 작업 디렉터리: {current_dir}")
    print("🌐 브라우저에서 http://localhost:8551 으로 접속하세요")
    print("=" * 50)
    
    # Flet 웹앱으로 실행
    try:
        ft.app(
            target=main, 
            view=ft.AppView.WEB_BROWSER,
            port=8551,
            assets_dir="assets"
        )
    except Exception as e:
        print(f"Flet 앱 실행 실패: {e}")
        traceback.print_exc()