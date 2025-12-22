"""
Composant TemperatureCard pour afficher la température du système.
"""
import flet as ft
from config import AppleTheme
from utils import debug_log, verbose_log


class TemperatureCard(ft.Container):
    """Carte pour afficher la température CPU/GPU."""
    
    def __init__(self, title="Temperature", icon=ft.Icons.THERMOSTAT, on_click=None):
        debug_log(f"Creating TemperatureCard: {title}")
        super().__init__()
        self.is_hovered = False
        self.current_temp = 0
        
        # Controls
        self.value_text = ft.Text("--", size=24, weight="bold", color=AppleTheme.TEXT_WHITE)
        self.sub_text = ft.Text("CPU Temperature", size=12, color=AppleTheme.TEXT_GREY)
        self.progress_bar = ft.ProgressBar(
            value=0,
            color=AppleTheme.GREEN,
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
                            ft.Icon(icon, color=AppleTheme.ORANGE, size=18),
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
        
        # Animation
        try:
            self.animate_scale = ft.animation.Animation(150, ft.AnimationCurve.EASE_OUT)
            verbose_log(f"Animation enabled for {title}")
        except AttributeError:
            debug_log(f"Animation not available for {title}, continuing without", "WARNING")
            pass

    def _handle_hover(self, e):
        self.is_hovered = e.data == "true"
        self.scale = 1.02 if self.is_hovered else 1.0
        self.update()

    def _get_temp_color(self, temp):
        """Retourne la couleur en fonction de la température."""
        if temp is None or temp == 0:
            return AppleTheme.TEXT_GREY
        elif temp < 60:
            return AppleTheme.GREEN
        elif temp < 80:
            return AppleTheme.ORANGE
        else:
            return AppleTheme.RED

    def update_data(self, temp_value):
        """Met à jour la température affichée."""
        verbose_log(f"Updating temperature card: {temp_value}°C")
        
        if temp_value is None or temp_value == 0:
            self.value_text.value = "--"
            self.sub_text.value = "Not available"
            self.progress_bar.value = 0
            self.progress_bar.color = AppleTheme.TEXT_GREY
        else:
            self.current_temp = temp_value
            self.value_text.value = f"{temp_value:.0f}°C"
            
            # Mise à jour du texte de statut
            if temp_value < 60:
                self.sub_text.value = "Normal"
            elif temp_value < 80:
                self.sub_text.value = "Warm"
            else:
                self.sub_text.value = "Hot!"
            
            # Mise à jour de la couleur et de la barre de progression
            # Normalisation: 0°C = 0%, 100°C = 100%
            self.progress_bar.value = min(max(temp_value / 100, 0), 1)
            self.progress_bar.color = self._get_temp_color(temp_value)
        
        self.update()
