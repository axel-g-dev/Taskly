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
        
        # Cache for optimization
        self.cached_main_val = None
        self.cached_sub_val = None
        self.cached_progress = None
        
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
        """Met à jour les données avec cache pour éviter les updates inutiles."""
        # Check if values have changed significantly
        main_str = f"{main_val}{self.value_suffix}"
        
        needs_update = False
        if self.cached_main_val != main_str:
            self.value_text.value = main_str
            self.cached_main_val = main_str
            needs_update = True
        
        if self.cached_sub_val != sub_val:
            self.sub_text.value = sub_val
            self.cached_sub_val = sub_val
            needs_update = True
        
        safe_progress = 0.0
        try:
            safe_progress = float(progress_val)
        except Exception as e:
            debug_log(f"Error converting progress value: {e}", "ERROR")
            safe_progress = 0.0
        
        safe_progress = min(max(safe_progress, 0), 1)
        
        # Only update if progress changed by more than 0.5%
        if self.cached_progress is None or abs(safe_progress - self.cached_progress) > 0.005:
            self.progress_bar.value = safe_progress
            self.cached_progress = safe_progress
            needs_update = True
        
        if needs_update:
            verbose_log(f"Updating card: {main_str}, {sub_val}, progress={safe_progress:.2f}")
            self.update()
