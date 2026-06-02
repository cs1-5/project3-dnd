import flet as ft
from ui_constants import (
    SPACING_SM, SPACING_LG, SPACING_XL,
    BUTTON_HEIGHT_LG, BUTTON_WIDTH_LG,
    TEXT_SIZE_SM, TEXT_SIZE_LG, TEXT_SIZE_XL
)


def home_screen(page: ft.Page, on_start_battle):
    """Render the home screen.
    
    Args:
        page: The Flet page object
        on_start_battle: Callback function to navigate to monster selection
    """
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(height=SPACING_XL * 2),  # Spacer
                ft.Icon(
                    name=ft.Icons.CASTLE,
                    size=120,
                    color=ft.Colors.RED_400,
                ),
                ft.Container(height=SPACING_LG),
                ft.Text(
                    "MONSTER BATTLE",
                    size=48,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.RED_400,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=SPACING_SM),
                ft.Text(
                    "D&D Combat Simulator",
                    size=TEXT_SIZE_LG,
                    color=ft.Colors.RED_300,
                    text_align=ft.TextAlign.CENTER,
                    italic=True,
                ),
                ft.Container(height=SPACING_XL),
                ft.Container(
                    content=ft.Text(
                        "Choose your champion and face your foe\n"
                        "Experience tactical combat with real-time probabilities",
                        size=TEXT_SIZE_XL,
                        color=ft.Colors.GREY_400,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    width=600,
                ),
                ft.Container(height=SPACING_XL * 2),
                ft.ElevatedButton(
                    "⚔️ START BATTLE",
                    width=BUTTON_WIDTH_LG,
                    height=BUTTON_HEIGHT_LG,
                    on_click=on_start_battle,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_700,
                        color=ft.Colors.WHITE,
                    ),
                ),
                ft.Container(height=SPACING_LG),
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Icon(ft.Icons.PSYCHOLOGY, size=30, color=ft.Colors.CYAN_400),
                                    ft.Text("Probability", size=TEXT_SIZE_SM, color=ft.Colors.CYAN_400),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=5,
                            ),
                            padding=10,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Icon(ft.Icons.TRENDING_UP, size=30, color=ft.Colors.GREEN_400),
                                    ft.Text("Live Stats", size=TEXT_SIZE_SM, color=ft.Colors.GREEN_400),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=5,
                            ),
                            padding=10,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Icon(ft.Icons.CASINO, size=30, color=ft.Colors.PURPLE_400),
                                    ft.Text("Monte Carlo", size=TEXT_SIZE_SM, color=ft.Colors.PURPLE_400),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=5,
                            ),
                            padding=10,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=SPACING_XL,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
    )

