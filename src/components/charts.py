"""
Composants de graphiques pour Taskly.
"""
import flet as ft
from config import AppleTheme, HISTORY_SIZE
from utils import with_opacity


class BaseLineChart(ft.Container):
    """Classe de base pour les graphiques de ligne."""
    
    def __init__(self, title, subtitle, color, max_points=30):
        super().__init__()
        self.max_points = max_points
        self.data_points = [ft.LineChartDataPoint(i, 0) for i in range(max_points)]
        
        self.title_text = ft.Text(title, size=16, weight="w600", color=AppleTheme.TEXT_WHITE)
        self.subtitle_text = ft.Text(subtitle, size=12, color=AppleTheme.TEXT_GREY)
        
        self.chart = ft.LineChart(
            data_series=[
                ft.LineChartData(
                    data_points=self.data_points,
                    stroke_width=3,
                    color=color,
                    curved=True,
                    stroke_cap_round=True,
                    below_line_bgcolor=with_opacity(0.1, color),
                )
            ],
            min_y=0,
            max_y=100,
            min_x=0,
            max_x=max_points,
            expand=True,
            left_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(value=0, label=ft.Text("0%", size=10, color=AppleTheme.TEXT_GREY)),
                    ft.ChartAxisLabel(value=50, label=ft.Text("50%", size=10, color=AppleTheme.TEXT_GREY)),
                    ft.ChartAxisLabel(value=100, label=ft.Text("100%", size=10, color=AppleTheme.TEXT_GREY)),
                ],
                show_labels=True
            ),
            bottom_axis=ft.ChartAxis(labels=[], show_labels=False),
            tooltip_bgcolor=AppleTheme.CARD_COLOR,
            horizontal_grid_lines=ft.ChartGridLines(interval=25, color=with_opacity(0.1, "#FFFFFF"), width=1),
            vertical_grid_lines=ft.ChartGridLines(interval=10, color=with_opacity(0.1, "#FFFFFF"), width=1),
            border=ft.border.all(0, AppleTheme.TRANSPARENT)
        )

        self.content = ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        self.title_text,
                        self.subtitle_text
                    ]
                ),
                ft.Container(content=self.chart, expand=True, padding=ft.padding.only(top=10))
            ]
        )
        self.bgcolor = AppleTheme.CARD_COLOR
        self.border_radius = AppleTheme.BORDER_RADIUS
        self.padding = AppleTheme.PADDING
        self.expand = 1

    def update_title(self, new_title):
        """Met à jour le titre du graphique."""
        self.title_text.value = new_title
        self.title_text.update()

    def update_chart(self, history_list):
        """Met à jour le graphique avec les nouvelles données."""
        for i, val in enumerate(history_list):
            if i < len(self.data_points):
                self.data_points[i].y = val if val is not None else 0
        self.chart.update()


class CPULineChart(BaseLineChart):
    """Graphique d'historique CPU."""
    
    def __init__(self):
        super().__init__(
            title="CPU History",
            subtitle=f"Last {HISTORY_SIZE}s",
            color=AppleTheme.BLUE,
            max_points=HISTORY_SIZE
        )


class RAMLineChart(BaseLineChart):
    """Graphique d'historique RAM."""
    
    def __init__(self):
        super().__init__(
            title="Memory History",
            subtitle=f"Last {HISTORY_SIZE}s",
            color=AppleTheme.PURPLE,
            max_points=HISTORY_SIZE
        )


class NetworkLineChart(ft.Container):
    """Graphique d'historique réseau (upload + download)."""
    
    def __init__(self):
        super().__init__()
        max_points = HISTORY_SIZE
        self.download_points = [ft.LineChartDataPoint(i, 0) for i in range(max_points)]
        self.upload_points = [ft.LineChartDataPoint(i, 0) for i in range(max_points)]
        
        self.title_text = ft.Text("Network History", size=16, weight="w600", color=AppleTheme.TEXT_WHITE)
        self.download_label = ft.Text("Download", size=10, color=AppleTheme.TEXT_GREY)
        self.upload_label = ft.Text("Upload", size=10, color=AppleTheme.TEXT_GREY)
        
        self.chart = ft.LineChart(
            data_series=[
                ft.LineChartData(
                    data_points=self.download_points,
                    stroke_width=3,
                    color=AppleTheme.GREEN,
                    curved=True,
                    stroke_cap_round=True,
                    below_line_bgcolor=with_opacity(0.1, AppleTheme.GREEN),
                ),
                ft.LineChartData(
                    data_points=self.upload_points,
                    stroke_width=2,
                    color=AppleTheme.CYAN,
                    curved=True,
                    stroke_cap_round=True,
                    below_line_bgcolor=with_opacity(0.05, AppleTheme.CYAN),
                )
            ],
            min_y=0,
            max_y=100,
            min_x=0,
            max_x=max_points,
            expand=True,
            left_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(value=0, label=ft.Text("0", size=10, color=AppleTheme.TEXT_GREY)),
                    ft.ChartAxisLabel(value=50, label=ft.Text("50", size=10, color=AppleTheme.TEXT_GREY)),
                    ft.ChartAxisLabel(value=100, label=ft.Text("100", size=10, color=AppleTheme.TEXT_GREY)),
                ],
                show_labels=True
            ),
            bottom_axis=ft.ChartAxis(labels=[], show_labels=False),
            tooltip_bgcolor=AppleTheme.CARD_COLOR,
            horizontal_grid_lines=ft.ChartGridLines(interval=25, color=with_opacity(0.1, "#FFFFFF"), width=1),
            vertical_grid_lines=ft.ChartGridLines(interval=10, color=with_opacity(0.1, "#FFFFFF"), width=1),
            border=ft.border.all(0, AppleTheme.TRANSPARENT)
        )

        self.content = ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        self.title_text,
                        ft.Row([
                            ft.Container(
                                content=ft.Row([
                                    ft.Container(width=12, height=3, bgcolor=AppleTheme.GREEN, border_radius=2),
                                    self.download_label
                                ], spacing=5)
                            ),
                            ft.Container(
                                content=ft.Row([
                                    ft.Container(width=12, height=3, bgcolor=AppleTheme.CYAN, border_radius=2),
                                    self.upload_label
                                ], spacing=5)
                            )
                        ], spacing=10)
                    ]
                ),
                ft.Container(content=self.chart, expand=True, padding=ft.padding.only(top=10))
            ]
        )
        self.bgcolor = AppleTheme.CARD_COLOR
        self.border_radius = AppleTheme.BORDER_RADIUS
        self.padding = AppleTheme.PADDING
        self.expand = 1

    def update_title(self, new_title):
        """Met à jour le titre du graphique."""
        self.title_text.value = new_title
        self.title_text.update()

    def update_chart(self, download_history, upload_history):
        """Met à jour le graphique avec les données réseau."""
        # Normalize to 0-100 scale (assuming max 1000 KB/s)
        max_speed = 1000
        
        for i, val in enumerate(download_history):
            if i < len(self.download_points):
                normalized = min((val / max_speed) * 100, 100) if val else 0
                self.download_points[i].y = normalized
        
        for i, val in enumerate(upload_history):
            if i < len(self.upload_points):
                normalized = min((val / max_speed) * 100, 100) if val else 0
                self.upload_points[i].y = normalized
        
        self.chart.update()
