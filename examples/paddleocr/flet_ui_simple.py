#!/usr/bin/env python3
"""
Simple Flet UI OCR Application (Unicode-safe)
PaddleOCR 의존성 문제에 대비한 시뮬레이션 모드 포함
"""

import flet as ft
import os
import time
from pathlib import Path
import json
import threading
import cv2
import numpy as np

# 안전한 출력을 위한 설정
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# PyPDF2 for PDF processing
try:
    import PyPDF2
    PDF_AVAILABLE = True
    print("PyPDF2 available")
except ImportError:
    PDF_AVAILABLE = False
    print("PyPDF2 not available")

# PaddleOCR with fallback
try:
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    from paddleocr import PaddleOCR
    PADDLEOCR_AVAILABLE = True
    print("PaddleOCR CPU mode available")
except Exception as e:
    PADDLEOCR_AVAILABLE = False
    print("PaddleOCR not available - using simulation mode")


class SimpleOCRApp:
    """간단한 Flet OCR 애플리케이션"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "PaddleOCR Flet UI"
        self.page.window_width = 1200
        self.page.window_height = 800
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
        # 상태 변수
        self.current_file = None
        self.ocr_results = []
        self.is_processing = False
        
        # UI 컴포넌트
        self.file_picker = None
        self.progress_bar = None
        self.status_text = None
        self.result_area = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """UI 구성"""
        # 파일 선택기
        self.file_picker = ft.FilePicker(on_result=self.on_file_selected)
        self.page.overlay.append(self.file_picker)
        
        # 제목
        title = ft.Text(
            "PaddleOCR Flet UI Application",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE_700
        )
        
        subtitle = ft.Text(
            "PDF/Image OCR Processing",
            size=14,
            color=ft.colors.GREY_600
        )
        
        # 엔진 상태
        engine_status = ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.icons.CHECK_CIRCLE if PADDLEOCR_AVAILABLE else ft.icons.WARNING,
                    color=ft.colors.GREEN if PADDLEOCR_AVAILABLE else ft.colors.ORANGE
                ),
                ft.Text(
                    "PaddleOCR Ready" if PADDLEOCR_AVAILABLE else "Simulation Mode",
                    size=12
                )
            ]),
            padding=10,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=5
        )
        
        # 파일 선택 버튼들
        file_buttons = ft.Row([
            ft.ElevatedButton(
                "Select Image File",
                icon=ft.icons.IMAGE,
                on_click=self.select_image_file,
                style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE)
            ),
            ft.ElevatedButton(
                "Select PDF File",
                icon=ft.icons.PICTURE_AS_PDF,
                on_click=self.select_pdf_file,
                style=ft.ButtonStyle(bgcolor=ft.colors.RED_600, color=ft.colors.WHITE)
            )
        ], alignment=ft.MainAxisAlignment.CENTER)
        
        # 처리 버튼
        process_button = ft.ElevatedButton(
            "Start OCR Processing",
            icon=ft.icons.PLAY_ARROW,
            on_click=self.start_processing,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.GREEN_600,
                color=ft.colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=8)
            ),
            width=200,
            height=50
        )
        
        # 진행률 표시
        self.progress_bar = ft.ProgressBar(width=400, visible=False)
        self.status_text = ft.Text("Ready", size=12, color=ft.colors.GREY_600)
        
        # 결과 표시 영역
        self.result_area = ft.ListView(
            height=300,
            spacing=10,
            padding=20
        )
        
        result_container = ft.Container(
            content=ft.Column([
                ft.Text("Processing Results", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=self.result_area,
                    border=ft.border.all(1, ft.colors.GREY_300),
                    border_radius=8,
                    bgcolor=ft.colors.GREY_50
                )
            ]),
            margin=ft.margin.only(top=20)
        )
        
        # 메인 레이아웃
        main_layout = ft.Column([
            ft.Container(
                content=ft.Column([title, subtitle], spacing=5),
                padding=20,
                bgcolor=ft.colors.BLUE_50,
                border_radius=10
            ),
            engine_status,
            ft.Container(height=20),  # 간격
            file_buttons,
            ft.Container(height=20),  # 간격
            process_button,
            ft.Container(height=20),  # 간격
            ft.Column([
                self.progress_bar,
                self.status_text
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            result_container
        ], spacing=15, scroll=ft.ScrollMode.AUTO)
        
        self.page.add(main_layout)
    
    def select_image_file(self, e):
        """이미지 파일 선택"""
        self.file_picker.pick_files(
            dialog_title="Select Image for OCR",
            allowed_extensions=["png", "jpg", "jpeg"],
            allow_multiple=False
        )
    
    def select_pdf_file(self, e):
        """PDF 파일 선택"""
        self.file_picker.pick_files(
            dialog_title="Select PDF for OCR",
            allowed_extensions=["pdf"],
            allow_multiple=False
        )
    
    def on_file_selected(self, e: ft.FilePickerResultEvent):
        """파일 선택됨"""
        if e.files:
            file = e.files[0]
            self.current_file = file.path
            filename = Path(file.path).name
            
            self.status_text.value = f"Selected: {filename}"
            self.page.update()
    
    def start_processing(self, e):
        """OCR 처리 시작"""
        if not self.current_file:
            self.show_dialog("Please select a file first!")
            return
        
        if self.is_processing:
            self.show_dialog("Processing in progress. Please wait.")
            return
        
        self.is_processing = True
        self.progress_bar.visible = True
        self.status_text.value = "Processing..."
        self.page.update()
        
        # 백그라운드 처리
        threading.Thread(target=self.process_file, daemon=True).start()
    
    def process_file(self):
        """파일 처리 (백그라운드)"""
        try:
            file_ext = Path(self.current_file).suffix.lower()
            
            if file_ext == '.pdf':
                self.process_pdf()
            elif file_ext in ['.png', '.jpg', '.jpeg']:
                self.process_image()
            else:
                self.update_status("Unsupported file format")
                
        except Exception as ex:
            self.update_status(f"Error: {str(ex)}")
        finally:
            self.is_processing = False
            self.progress_bar.visible = False
            self.page.update()
    
    def process_pdf(self):
        """PDF 처리"""
        try:
            if PDF_AVAILABLE:
                with open(self.current_file, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    total_pages = len(pdf_reader.pages)
                    
                    for i, page in enumerate(pdf_reader.pages):
                        self.update_status(f"Processing page {i+1}/{total_pages}")
                        text += f"\n--- Page {i+1} ---\n"
                        text += page.extract_text() + "\n"
                
                self.display_text_result(f"PDF Text Extraction ({total_pages} pages)", text)
                self.update_status("PDF processing completed")
            else:
                self.update_status("PyPDF2 not available for PDF processing")
                
        except Exception as e:
            self.update_status(f"PDF processing error: {str(e)}")
    
    def process_image(self):
        """이미지 OCR 처리"""
        try:
            if PADDLEOCR_AVAILABLE:
                # 실제 PaddleOCR 사용
                ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False, show_log=False)
                result = ocr.ocr(self.current_file, cls=True)
                
                if result and result[0]:
                    texts = []
                    for line in result[0]:
                        if line[1]:
                            text = line[1][0]
                            confidence = line[1][1] if len(line[1]) > 1 else 0.0
                            texts.append({
                                'text': text,
                                'confidence': confidence
                            })
                    
                    self.display_ocr_results(texts)
                    self.update_status(f"OCR completed: {len(texts)} texts found")
                else:
                    self.update_status("No text found in image")
            else:
                # 시뮬레이션 모드
                self.simulate_ocr()
                
        except Exception as e:
            self.update_status(f"OCR processing error: {str(e)}")
    
    def simulate_ocr(self):
        """OCR 시뮬레이션"""
        try:
            # 이미지 확인
            img = cv2.imread(self.current_file)
            if img is None:
                self.update_status("Cannot read image file")
                return
            
            height, width = img.shape[:2]
            
            # 시뮬레이션 결과 생성
            simulated_texts = [
                {'text': f'Image size: {width}x{height}', 'confidence': 0.90},
                {'text': 'PaddleOCR Simulation Mode', 'confidence': 0.85},
                {'text': 'Text recognition simulation', 'confidence': 0.88},
                {'text': 'Actual OCR needs PaddleOCR installation', 'confidence': 0.92}
            ]
            
            time.sleep(1)  # 처리 시뮬레이션
            
            self.display_ocr_results(simulated_texts)
            self.update_status("Simulation completed")
            
        except Exception as e:
            self.update_status(f"Simulation error: {str(e)}")
    
    def display_ocr_results(self, texts):
        """OCR 결과 표시"""
        self.result_area.controls.clear()
        
        for i, result in enumerate(texts):
            # 신뢰도에 따른 색상
            color = ft.colors.GREEN if result['confidence'] > 0.8 else \
                   ft.colors.ORANGE if result['confidence'] > 0.6 else ft.colors.RED
            
            item = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(f"Text {i+1}", weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=ft.Text(f"{result['confidence']:.1%}", 
                                           size=10, color=ft.colors.WHITE),
                            bgcolor=color,
                            padding=5,
                            border_radius=10
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.SelectableText(result['text'], size=14)
                ], spacing=5),
                padding=10,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=5,
                bgcolor=ft.colors.WHITE
            )
            self.result_area.controls.append(item)
        
        self.page.update()
    
    def display_text_result(self, title, text):
        """텍스트 결과 표시"""
        self.result_area.controls.clear()
        
        item = ft.Container(
            content=ft.Column([
                ft.Text(title, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700),
                ft.SelectableText(text, size=12)
            ], spacing=10),
            padding=15,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=5,
            bgcolor=ft.colors.WHITE
        )
        self.result_area.controls.append(item)
        self.page.update()
    
    def update_status(self, message):
        """상태 업데이트"""
        self.status_text.value = message
        self.page.update()
    
    def show_dialog(self, message):
        """알림 대화상자"""
        dialog = ft.AlertDialog(
            title=ft.Text("Notice"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.page.close_dialog())]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()


def main(page: ft.Page):
    """메인 함수"""
    SimpleOCRApp(page)


if __name__ == "__main__":
    print("Starting Flet OCR Application...")
    print("PaddleOCR CPU mode (model download on first run)")
    print("Open browser at http://localhost:8550")
    
    # Flet 웹앱 실행
    try:
        ft.app(
            target=main,
            view=ft.AppView.WEB_BROWSER,
            port=8550
        )
    except Exception as e:
        print(f"Application error: {e}")
        input("Press Enter to exit...")