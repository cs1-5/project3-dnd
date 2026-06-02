"""
UI utility functions for the Monster Battle app.
"""

import flet as ft


def get_probability_color(probability: float) -> str:
    """
    Get color based on probability value.
    
    Args:
        probability: Probability value between 0.0 and 1.0
    
    Returns:
        Flet color string
    """
    if probability >= 0.70:
        return ft.Colors.GREEN_400
    elif probability >= 0.30:
        return ft.Colors.YELLOW_600
    else:
        return ft.Colors.RED_400


def format_percentage(value: float) -> str:
    """
    Format a decimal value as a percentage string.
    
    Args:
        value: Decimal value between 0.0 and 1.0
    
    Returns:
        Formatted percentage string (e.g., "65%")
    """
    return f"{value * 100:.0f}%"


def format_percentage_precise(value: float) -> str:
    """
    Format a decimal value as a precise percentage string.
    
    Args:
        value: Decimal value between 0.0 and 1.0
    
    Returns:
        Formatted percentage string with one decimal (e.g., "65.3%")
    """
    return f"{value * 100:.1f}%"

