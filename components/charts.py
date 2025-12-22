"""
Composants de graphiques pour Taskly.
"""
import flet as ft
from config import AppleTheme
from utils import with_opacity


class MiniChart(ft.Container):
    """Mini graphique sparkline pour les cartes."""
    
    def __init__(self, color):
        super().__init__()
        self.data_points = [ft.LineChartDataPoint(i, 0) for i in range(30)]
        
        self.chart = ft.LineChart(
            data_series=[
                ft.LineChartData(
                    data_points=self.data_points,
                    stroke_width=2,
                    color=color,
                    curved=True,
                    stroke_cap_round=True,
                    below_line_bgcolor=with_opacity(0.15, color),
                )
            ],
            min_y=0,
            max_y=100,
            min_x=0,
            max_x=30,
            left_axis=ft.ChartAxis(labels=[], show_labels=False),
            bottom_axis=ft.ChartAxis(labels=[], show_labels=False),
            tooltip_bgcolor=AppleTheme.TRANSPARENT,
            border=ft.border.all(0, AppleTheme.TRANSPARENT),
            interactive=False,
        )
        
        self.content = self.chart
        self.height = 60
        self.expand = True

    def update_chart(self, history_list):
        # Prend les 30 dernières valeurs
        recent = history_list[-30:] if len(history_list) >= 30 else history_list
        for i, val in enumerate(recent):
            if i < len(self.data_points):
                self.data_points[i].y = val if val is not None else 0
        self.chart.update()


class CPULineChart(ft.Container):
    """Le graphique principal avec historique."""
    
    def __init__(self):
        super().__init__()
        self.data_points = [ft.LineChartDataPoint(i, 0) for i in range(60)]
        
        self.chart = ft.LineChart(
            data_series=[
                ft.LineChartData(
                    data_points=self.data_points,
                    stroke_width=3,
                    color=AppleTheme.BLUE,
                    curved=True,
                    stroke_cap_round=True,
                    below_line_bgcolor=with_opacity(0.1, AppleTheme.BLUE),
                )
            ],
            min_y=0,
            max_y=100,
            min_x=0,
            max_x=60,
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
                        ft.Text("CPU History", size=16, weight="w600", color=AppleTheme.TEXT_WHITE),
                        ft.Text("Last 60s", size=12, color=AppleTheme.TEXT_GREY)
                    ]
                ),
                ft.Container(content=self.chart, expand=True, padding=ft.padding.only(top=10))
            ]
        )
        self.bgcolor = AppleTheme.CARD_COLOR
        self.border_radius = AppleTheme.BORDER_RADIUS
        self.padding = AppleTheme.PADDING
        self.expand = 2

    def update_chart(self, history_list):
        for i, val in enumerate(history_list):
            if i < len(self.data_points):
                self.data_points[i].y = val if val is not None else 0
        self.chart.update()
