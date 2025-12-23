"""
Composant SystemInfoPanel pour afficher les informations système détaillées.
"""
import flet as ft
from config import AppleTheme
from utils import with_opacity, format_uptime


class SystemInfoPanel(ft.Container):
    """Panel d'informations système détaillées."""
    
    def __init__(self):
        super().__init__()
        
        self.title_text = ft.Text("System Info", size=16, weight="w600", color=AppleTheme.TEXT_WHITE)
        self.cpu_info = ft.Text("", size=12, color=AppleTheme.TEXT_GREY)
        self.disk_info = ft.Text("", size=12, color=AppleTheme.TEXT_GREY)
        self.uptime_info = ft.Text("", size=12, color=AppleTheme.TEXT_GREY)
        self.battery_info = ft.Text("", size=12, color=AppleTheme.TEXT_GREY)
        
        self.content = ft.Column(
            controls=[
                self.title_text,
                ft.Divider(color=with_opacity(0.2, "#FFFFFF"), height=1),
                ft.Row([
                    ft.Icon(ft.Icons.COMPUTER, color=AppleTheme.CYAN, size=16),
                    self.cpu_info
                ], spacing=10),
                ft.Row([
                    ft.Icon(ft.Icons.STORAGE, color=AppleTheme.ORANGE, size=16),
                    self.disk_info
                ], spacing=10),
                ft.Row([
                    ft.Icon(ft.Icons.ACCESS_TIME, color=AppleTheme.GREEN, size=16),
                    self.uptime_info
                ], spacing=10),
                ft.Row([
                    ft.Icon(ft.Icons.BATTERY_CHARGING_FULL, color=AppleTheme.YELLOW, size=16),
                    self.battery_info
                ], spacing=10),
            ],
            spacing=12
        )
        self.bgcolor = AppleTheme.CARD_COLOR
        self.border_radius = AppleTheme.BORDER_RADIUS
        self.padding = AppleTheme.PADDING

    def update_labels(self, t):
        """Met à jour les labels avec les traductions."""
        self.title_text.value = t("system_info")
        self.title_text.update()

    def update_info(self, metrics):
        # CPU Info
        cpu_text = f"{metrics['cpu_count']} cores ({metrics['cpu_count_logical']} threads)"
        if metrics['cpu_freq'] > 0:
            cpu_text += f" @ {metrics['cpu_freq']/1000:.2f} GHz"
        if metrics.get('cpu_temp'):
            cpu_text += f" • {metrics['cpu_temp']:.0f}°C"
        self.cpu_info.value = cpu_text
        
        # Disk Info
        self.disk_info.value = f"{metrics['disk_used_gb']:.0f} GB used / {metrics['disk_total_gb']:.0f} GB total ({metrics['disk_percent']:.1f}%)"
        
        # Uptime
        self.uptime_info.value = f"Uptime: {format_uptime(metrics['uptime'])}"
        
        # Battery
        if metrics['battery_plugged']:
            batt_text = f"{metrics['battery_percent']:.0f}% • Charging"
        else:
            batt_text = f"{metrics['battery_percent']:.0f}%"
            if metrics.get('battery_time_left'):
                batt_text += f" • {format_uptime(metrics['battery_time_left'])} left"
        self.battery_info.value = batt_text
        
        self.update()
