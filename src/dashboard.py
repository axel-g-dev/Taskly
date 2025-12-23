"""
Interface principale du dashboard Taskly.
"""
import flet as ft
import time
import threading
from datetime import datetime

from config import AppleTheme
from constants import DEFAULT_LANGUAGE, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from utils import debug_log, verbose_log, with_opacity
from data_manager import SystemDataManager
from data_exporter import DataExporter
from i18n import TranslationManager
from components import (
    MetricCard, CPULineChart, RAMLineChart, NetworkLineChart,
    ProcessList, SystemInfoPanel, AlertManager, AlertPanel
)


class DashboardUI:
    """Interface principale de l'application."""
    
    def __init__(self, page: ft.Page):
        debug_log("=" * 60)
        debug_log("TASKLY - SYSTEM MONITOR STARTING")
        debug_log("=" * 60)
        self.page = page
        self.data_manager = SystemDataManager()
        self.running = True
        self.current_sort = 'cpu'
        self.show_details = False
        self.show_alerts = False
        self.alert_manager = AlertManager()
        self.data_exporter = DataExporter()
        
        # Translation manager
        self.i18n = TranslationManager(default_language=DEFAULT_LANGUAGE)
        self.t = self.i18n.t  # Shortcut for translations
        
        debug_log("Setting up page...")
        self.setup_page()
        debug_log("Building UI...")
        self.build_ui()
        debug_log("Starting monitoring thread...")
        self.start_monitoring()
        debug_log("Taskly initialization complete!")

    def setup_page(self):
        """Configure les paramètres de la page."""
        debug_log("Configuring page settings")
        self.page.title = self.t("app_title")
        self.page.bgcolor = AppleTheme.BG_COLOR
        self.page.padding = 30
        self.page.theme_mode = ft.ThemeMode.DARK
        
        self.page.fonts = {
            "SF Pro": "https://raw.githubusercontent.com/google/fonts/main/ofl/sfpro/SFPro-Regular.ttf"
        }
        self.page.theme = ft.Theme(font_family="SF Pro")
        
        self.page.window.width = WINDOW_WIDTH
        self.page.window.height = WINDOW_HEIGHT
        self.page.window.min_width = WINDOW_MIN_WIDTH
        self.page.window.min_height = WINDOW_MIN_HEIGHT
        debug_log(f"Window size: {self.page.window.width}x{self.page.window.height}")

    def toggle_details(self, e):
        """Affiche/cache le panneau d'informations détaillées."""
        debug_log(f"Toggling details panel (currently: {self.show_details})")
        self.show_details = not self.show_details
        if self.show_details:
            self.layout.controls.insert(3, self.info_panel)
            debug_log("Details panel shown")
        else:
            if self.info_panel in self.layout.controls:
                self.layout.controls.remove(self.info_panel)
            debug_log("Details panel hidden")
        self.layout.update()
    
    def toggle_alerts(self, e):
        """Affiche/cache le panneau d'alertes."""
        debug_log(f"Toggling alerts panel (currently: {self.show_alerts})")
        self.show_alerts = not self.show_alerts
        if self.show_alerts:
            # Insert after header and spacing
            insert_pos = 4 if self.show_details else 3
            self.layout.controls.insert(insert_pos, self.alert_panel)
            debug_log("Alerts panel shown")
        else:
            if self.alert_panel in self.layout.controls:
                self.layout.controls.remove(self.alert_panel)
            debug_log("Alerts panel hidden")
        self.layout.update()
    
    def change_language(self, e):
        """Bascule entre français et anglais."""
        debug_log(f"Changing language from {self.i18n.get_current_language()}")
        new_lang = self.i18n.toggle_language()
        debug_log(f"Language changed to: {new_lang}")
        
        # Update page title
        self.page.title = self.t("app_title")
        
        # Update all UI components with new translations
        self.update_ui_translations()
        self.page.update()
    
    def update_ui_translations(self):
        """Met à jour toutes les traductions de l'interface."""
        debug_log("Updating UI translations")
        
        # Update metric cards
        self.cpu_card.update_title(self.t("cpu_usage"))
        self.ram_card.update_title(self.t("memory"))
        self.net_card.update_title(self.t("network"))
        
        # Update charts
        self.cpu_chart.update_title(self.t("cpu_history"))
        self.ram_chart.update_title(self.t("ram_history"))
        self.net_chart.update_title(self.t("network_history"))
        
        # Update process list
        self.process_component.update_labels(self.t)
        
        # Update system info panel if visible
        if self.show_details:
            self.info_panel.update_labels(self.t)
        
        # Update header live badge
        self.live_text.value = self.t("live")
        self.live_text.update()
        
        debug_log("UI translations updated")
    
    def export_data(self, e):
        """Exporte les données actuelles."""
        debug_log("Exporting data...")
        try:
            metrics = self.data_manager.get_metrics()
            json_file = self.data_exporter.export_to_json(metrics)
            csv_file = self.data_exporter.export_to_csv(metrics)
            debug_log(f"Data exported: JSON={json_file}, CSV={csv_file}")
            # TODO: Show success notification to user
        except Exception as e:
            debug_log(f"Export failed: {e}", "ERROR")

    def build_ui(self):
        """Construit l'interface utilisateur."""
        debug_log("Building UI components...")
        # Header avec horloge
        self.clock_text = ft.Text(
            datetime.now().strftime("%H:%M:%S"),
            size=12,
            color=AppleTheme.TEXT_GREY
        )
        
        self.live_text = ft.Text(self.t("live"), color=AppleTheme.GREEN, size=12, weight="bold")
        
        header = ft.Row(
            controls=[
                ft.Row([
                    ft.Text("Taskly", size=28, weight="bold", color=AppleTheme.TEXT_WHITE),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CIRCLE, color=AppleTheme.GREEN, size=8),
                            self.live_text
                        ], spacing=5),
                        bgcolor=with_opacity(0.2, AppleTheme.GREEN),
                        padding=ft.padding.symmetric(horizontal=10, vertical=5),
                        border_radius=20
                    )
                ], spacing=15),
                ft.Row([
                    self.clock_text,
                    ft.IconButton(
                        icon=ft.Icons.LANGUAGE,
                        icon_color=AppleTheme.CYAN,
                        on_click=self.change_language,
                        tooltip=self.t("tooltip_language")
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DOWNLOAD,
                        icon_color=AppleTheme.GREEN,
                        on_click=self.export_data,
                        tooltip=self.t("tooltip_export")
                    ),
                    ft.IconButton(
                        icon=ft.Icons.NOTIFICATIONS_OUTLINED,
                        icon_color=AppleTheme.ORANGE,
                        on_click=self.toggle_alerts,
                        tooltip=self.t("tooltip_alerts")
                    ),
                    ft.IconButton(
                        icon=ft.Icons.INFO_OUTLINE,
                        icon_color=AppleTheme.BLUE,
                        on_click=self.toggle_details,
                        tooltip=self.t("tooltip_info")
                    )
                ], spacing=5)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        debug_log("Header created")

        # Metric Cards
        debug_log("Creating metric cards...")
        self.cpu_card = MetricCard(self.t("cpu_usage"), ft.Icons.MEMORY, AppleTheme.BLUE, "%")
        self.ram_card = MetricCard(self.t("memory"), ft.Icons.SD_STORAGE, AppleTheme.PURPLE, "%")
        self.net_card = MetricCard(self.t("network"), ft.Icons.WIFI, AppleTheme.GREEN, " KB/s")
        
        
        metric_cards = [self.cpu_card, self.ram_card, self.net_card]

        top_row = ft.Row(
            controls=metric_cards,
            spacing=20,
        )
        debug_log("Metric cards created")

        # System Info Panel (caché par défaut)
        debug_log("Creating system info panel and alert panel...")
        self.info_panel = SystemInfoPanel()
        self.alert_panel = AlertPanel()

        # Charts Row
        debug_log("Creating charts...")
        self.cpu_chart = CPULineChart()
        self.ram_chart = RAMLineChart()
        self.net_chart = NetworkLineChart()
        
        charts_row = ft.Row(
            controls=[self.cpu_chart, self.ram_chart, self.net_chart],
            spacing=20,
            expand=True
        )
        
        # Process List
        debug_log("Creating process list...")
        self.process_component = ProcessList(on_sort_change=self._handle_sort_change)

        debug_log("All components created")

        self.layout = ft.Column(
            controls=[
                header,
                ft.Container(height=20),
                top_row,
                ft.Container(height=10),
                charts_row,
                ft.Container(height=10),
                self.process_component
            ],
            expand=True
        )
        
        debug_log("Adding layout to page...")
        self.page.add(self.layout)
        debug_log("UI build complete!")

    def _handle_sort_change(self, sort_type):
        """Gère le changement de tri des processus."""
        debug_log(f"Process sort changed to: {sort_type}")
        self.current_sort = sort_type

    def start_monitoring(self):
        """Démarre le thread de monitoring."""
        debug_log("Starting monitoring thread...")
        monitor_thread = threading.Thread(target=self._update_loop, daemon=True)
        monitor_thread.start()
        debug_log("Monitoring thread started")

    def _update_loop(self):
        """Boucle principale de mise à jour."""
        debug_log("Update loop started")
        iteration = 0
        while self.running:
            try:
                iteration += 1
                verbose_log(f"--- Update iteration {iteration} ---")
                
                metrics = self.data_manager.get_metrics()
                top_procs = self.data_manager.get_top_processes(sort_by=self.current_sort)

                # Mise à jour horloge
                self.clock_text.value = datetime.now().strftime("%H:%M:%S")
                self.clock_text.update()

                # Mise à jour des cartes
                verbose_log("Updating metric cards...")
                self.cpu_card.update_data(
                    f"{metrics['cpu_percent']:.1f}",
                    f"{metrics['cpu_count']} cores",
                    metrics['cpu_percent'] / 100
                )
                
                self.ram_card.update_data(
                    f"{metrics['ram_percent']:.1f}",
                    f"{metrics['ram_used_gb']:.1f} / {metrics['ram_total_gb']:.1f} GB",
                    metrics['ram_percent'] / 100
                )
                
                
                total_speed = metrics['net_down'] + metrics['net_up']
                max_ref_speed = 5000
                self.net_card.update_data(
                    f"{metrics['net_down']:.0f}",
                    f"↑ {metrics['net_up']:.0f} KB/s",
                    min(total_speed / max_ref_speed, 1.0)
                )

                # Mise à jour des graphiques
                verbose_log("Updating charts...")
                self.cpu_chart.update_chart(metrics['cpu_history'])
                self.ram_chart.update_chart(metrics['ram_history'])
                self.net_chart.update_chart(metrics['net_down_history'], metrics['net_up_history'])
                
                # Mise à jour de la liste de processus
                self.process_component.update_processes(top_procs)
                
                # Mise à jour info panel si visible
                if self.show_details:
                    verbose_log("Updating info panel...")
                    self.info_panel.update_info(metrics)
                
                # Vérifier les alertes
                new_alerts = self.alert_manager.check_metrics(metrics)
                if new_alerts and self.show_alerts:
                    self.alert_panel.update_alerts(self.alert_manager.get_recent_alerts())

                verbose_log(f"Update iteration {iteration} complete")
                time.sleep(1)
                
            except Exception as e:
                debug_log(f"ERROR in update loop (iteration {iteration}): {e}", "ERROR")
                import traceback
                traceback.print_exc()
                time.sleep(1)
