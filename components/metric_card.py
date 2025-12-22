"""
Composant MetricCard pour afficher les métriques système.
"""
import flet as ft
from config import AppleTheme
from utils import debug_log, verbose_log


class MetricCard(ft.Container):
    """Carte pour les métriques (CPU, RAM, Net)."""
    
    def __init__(self, title, icon, accent_color, value_suffix="", on_click=None):
        debug_log(f"Creating MetricCard: {title}")
        super().__init__()
        self.accent_color = accent_color
        self.value_suffix = value_suffix
        self.is_hovered = False
        
        # Controls
        self.value_text = ft.Text("0", size=24, weight="bold", color=AppleTheme.TEXT_WHITE)
        self.sub_text = ft.Text("", size=12, color=AppleTheme.TEXT_GREY)
        self.progress_bar = ft.ProgressBar(
            value=0,
            color=accent_color,
            bgcolor="#3A3A3C",
            height=6,
            border_radius=ft.border_radius.all(3)
        )
        
        self.content = ft.Column(
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(controls=[
                            ft.Icon(icon, color=accent_color, size=18),
                            ft.Text(title, size=14, weight="w500", color=AppleTheme.TEXT_GREY),
                        ]),
                    ]
                ),
                ft.Column(
                    spacing=5,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[self.value_text, self.sub_text]
                        ),
                        self.progress_bar
                    ]
                )
            ]
        )
        
        self.bgcolor = AppleTheme.CARD_COLOR
        self.border_radius = AppleTheme.BORDER_RADIUS
        self.padding = AppleTheme.PADDING
        self.expand = 1
        self.on_click = on_click
        self.on_hover = self._handle_hover
        # FIX: Animation simplifiée compatible avec toutes versions de Flet
        try:
            self.animate_scale = ft.animation.Animation(150, ft.AnimationCurve.EASE_OUT)
            verbose_log(f"Animation enabled for {title}")
        except AttributeError:
            # Si l'animation n'est pas disponible, on continue sans
            debug_log(f"Animation not available for {title}, continuing without", "WARNING")
            pass

    def _handle_hover(self, e):
        self.is_hovered = e.data == "true"
        self.scale = 1.02 if self.is_hovered else 1.0
        self.update()

    def update_data(self, main_val, sub_val, progress_val):
        verbose_log(f"Updating card: {main_val}{self.value_suffix}, {sub_val}, progress={progress_val}")
        self.value_text.value = f"{main_val}{self.value_suffix}"
        self.sub_text.value = sub_val
        safe_progress = 0.0
        try:
            safe_progress = float(progress_val)
        except Exception as e:
            debug_log(f"Error converting progress value: {e}", "ERROR")
            safe_progress = 0.0
        self.progress_bar.value = min(max(safe_progress, 0), 1)
        self.update()
