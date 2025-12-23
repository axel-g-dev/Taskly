"""
Gestionnaire d'alertes pour surveiller les seuils critiques.
"""
import flet as ft
from config import AppleTheme, ALERT_THRESHOLDS
from utils import debug_log
from datetime import datetime


class AlertManager:
    """Gère les alertes système pour les seuils critiques."""
    
    def __init__(self):
        debug_log("Initializing AlertManager")
        self.alerts = []
        self.max_alerts = 10
        self.last_cpu_alert = 0
        self.last_ram_alert = 0
        self.last_temp_alert = 0
        self.alert_cooldown = 30  # seconds between same type of alerts
    
    def check_metrics(self, metrics):
        """Vérifie les métriques et génère des alertes si nécessaire."""
        current_time = datetime.now().timestamp()
        new_alerts = []
        
        # Check CPU
        if metrics['cpu_percent'] > ALERT_THRESHOLDS['cpu']:
            if current_time - self.last_cpu_alert > self.alert_cooldown:
                new_alerts.append({
                    'type': 'cpu',
                    'level': 'warning' if metrics['cpu_percent'] < 95 else 'critical',
                    'message': f"CPU usage high: {metrics['cpu_percent']:.1f}%",
                    'timestamp': datetime.now(),
                    'value': metrics['cpu_percent']
                })
                self.last_cpu_alert = current_time
        
        # Check RAM
        if metrics['ram_percent'] > ALERT_THRESHOLDS['ram']:
            if current_time - self.last_ram_alert > self.alert_cooldown:
                new_alerts.append({
                    'type': 'ram',
                    'level': 'warning' if metrics['ram_percent'] < 95 else 'critical',
                    'message': f"Memory usage high: {metrics['ram_percent']:.1f}%",
                    'timestamp': datetime.now(),
                    'value': metrics['ram_percent']
                })
                self.last_ram_alert = current_time
        
        # Add new alerts
        for alert in new_alerts:
            self.alerts.insert(0, alert)
            debug_log(f"ALERT: {alert['message']}", "WARNING")
        
        # Keep only recent alerts
        self.alerts = self.alerts[:self.max_alerts]
        
        return new_alerts
    
    def get_recent_alerts(self, limit=5):
        """Retourne les alertes récentes."""
        return self.alerts[:limit]
    
    def clear_alerts(self):
        """Efface toutes les alertes."""
        self.alerts = []
        debug_log("All alerts cleared")


class AlertPanel(ft.Container):
    """Panneau d'affichage des alertes."""
    
    def __init__(self):
        super().__init__()
        
        self.alert_list = ft.Column(spacing=8)
        
        self.content = ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Alerts", size=16, weight="w600", color=AppleTheme.TEXT_WHITE),
                        ft.IconButton(
                            icon=ft.Icons.CLEAR_ALL,
                            icon_color=AppleTheme.TEXT_GREY,
                            icon_size=16,
                            tooltip="Clear all alerts"
                        )
                    ]
                ),
                ft.Divider(color="#3A3A3C", height=1),
                self.alert_list
            ],
            spacing=12
        )
        
        self.bgcolor = AppleTheme.CARD_COLOR
        self.border_radius = AppleTheme.BORDER_RADIUS
        self.padding = AppleTheme.PADDING
        self.visible = False
    
    def update_alerts(self, alerts):
        """Met à jour l'affichage des alertes."""
        self.alert_list.controls.clear()
        
        if not alerts:
            self.visible = False
            return
        
        self.visible = True
        
        for alert in alerts:
            # Choose color based on level
            if alert['level'] == 'critical':
                color = AppleTheme.RED
                icon = ft.Icons.ERROR
            else:
                color = AppleTheme.ORANGE
                icon = ft.Icons.WARNING
            
            # Choose icon based on type
            if alert['type'] == 'cpu':
                type_icon = ft.Icons.MEMORY
            elif alert['type'] == 'ram':
                type_icon = ft.Icons.SD_STORAGE
            else:
                type_icon = ft.Icons.THERMOSTAT
            
            alert_row = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(icon, color=color, size=16),
                        ft.Icon(type_icon, color=AppleTheme.TEXT_GREY, size=14),
                        ft.Column(
                            controls=[
                                ft.Text(alert['message'], size=12, color=AppleTheme.TEXT_WHITE),
                                ft.Text(
                                    alert['timestamp'].strftime("%H:%M:%S"),
                                    size=10,
                                    color=AppleTheme.TEXT_GREY
                                )
                            ],
                            spacing=2,
                            expand=True
                        )
                    ],
                    spacing=10
                ),
                bgcolor="#3A3A3C",
                border_radius=8,
                padding=10
            )
            self.alert_list.controls.append(alert_row)
        
        self.update()
