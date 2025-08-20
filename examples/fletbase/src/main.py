"""
기본 Flet 애플리케이션
버전: 1.0.0
날짜: 2025-05-17
"""

import flet as ft

def main(page: ft.Page):
    # 페이지 설정
    page.title = "Flet 기본 애플리케이션"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # 인사말 텍스트
    greeting_text = ft.Text(
        value="",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE,
        text_align=ft.TextAlign.CENTER,
    )
    
    # 버튼 클릭 이벤트 핸들러
    def button_clicked(e):
        greeting_text.value = "Hello World!"
        page.update()
    
    # 버튼 생성
    hello_button = ft.ElevatedButton(
        text="인사하기",
        icon=ft.Icons.FAVORITE,
        on_click=button_clicked,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE,
            padding=15,
        ),
        height=50,
        width=150,
    )
    
    # 페이지에 컴포넌트 추가
    page.add(
        ft.Column(
            [
                ft.Text(
                    "Flet 기본 애플리케이션", 
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                ),
                ft.Text(
                    "아래 버튼을 클릭하세요",
                    size=18,
                    italic=True,
                    color=ft.Colors.GREY_700,
                ),
                ft.Container(height=20),  # 간격 추가
                hello_button,
                ft.Container(height=30),  # 간격 추가
                greeting_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
