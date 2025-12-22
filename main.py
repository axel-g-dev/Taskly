"""
Taskly - System Monitor
Point d'entrée principal de l'application.
"""
import flet as ft
from dashboard import DashboardUI


def main(page: ft.Page):
    """Fonction principale de l'application."""
    app = DashboardUI(page)


if __name__ == "__main__":
    ft.app(target=main)
