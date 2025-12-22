"""
Composant ProcessList pour afficher les processus système.
"""
import flet as ft
from config import AppleTheme


class ProcessList(ft.Container):
    """Tableau des processus avec tri."""
    
    def __init__(self, on_sort_change):
        super().__init__()
        self.on_sort_change = on_sort_change
        self.current_sort = 'cpu'
        
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Process", color=AppleTheme.TEXT_GREY, size=12)),
                ft.DataColumn(ft.Text("PID", color=AppleTheme.TEXT_GREY, size=12), numeric=True),
                ft.DataColumn(ft.Text("CPU%", color=AppleTheme.TEXT_GREY, size=12), numeric=True),
                ft.DataColumn(ft.Text("RAM%", color=AppleTheme.TEXT_GREY, size=12), numeric=True),
            ],
            rows=[],
            column_spacing=10,
            heading_row_height=30,
            data_row_min_height=40,
        )

        # Boutons de tri
        self.cpu_sort_btn = ft.ElevatedButton(
            "Sort by CPU",
            icon=ft.Icons.SORT,
            bgcolor=AppleTheme.BLUE,
            color=AppleTheme.TEXT_WHITE,
            on_click=lambda _: self._change_sort('cpu')
        )
        
        self.mem_sort_btn = ft.ElevatedButton(
            "Sort by RAM",
            icon=ft.Icons.SORT,
            bgcolor=AppleTheme.CARD_COLOR,
            color=AppleTheme.TEXT_GREY,
            on_click=lambda _: self._change_sort('memory')
        )

        self.content = ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Top Processes", size=16, weight="w600", color=AppleTheme.TEXT_WHITE),
                        ft.Row([self.cpu_sort_btn, self.mem_sort_btn], spacing=5)
                    ]
                ),
                ft.Container(
                    content=ft.Column([self.data_table], scroll=ft.ScrollMode.AUTO),
                    expand=True
                )
            ]
        )
        self.bgcolor = AppleTheme.CARD_COLOR
        self.border_radius = AppleTheme.BORDER_RADIUS
        self.padding = AppleTheme.PADDING
        self.expand = 1

    def _change_sort(self, sort_type):
        self.current_sort = sort_type
        if sort_type == 'cpu':
            self.cpu_sort_btn.bgcolor = AppleTheme.BLUE
            self.cpu_sort_btn.color = AppleTheme.TEXT_WHITE
            self.mem_sort_btn.bgcolor = AppleTheme.CARD_COLOR
            self.mem_sort_btn.color = AppleTheme.TEXT_GREY
        else:
            self.mem_sort_btn.bgcolor = AppleTheme.PURPLE
            self.mem_sort_btn.color = AppleTheme.TEXT_WHITE
            self.cpu_sort_btn.bgcolor = AppleTheme.CARD_COLOR
            self.cpu_sort_btn.color = AppleTheme.TEXT_GREY
        
        self.cpu_sort_btn.update()
        self.mem_sort_btn.update()
        self.on_sort_change(sort_type)

    def update_processes(self, procs):
        new_rows = []
        for p in procs:
            name = p.get('name', 'Unknown')
            pid = p.get('pid', 0)
            cpu = p.get('cpu_percent', 0.0)
            mem = p.get('memory_percent', 0.0)
            if cpu is None:
                cpu = 0.0
            if mem is None:
                mem = 0.0

            new_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(name)[:15], color=AppleTheme.TEXT_WHITE, size=13, weight="w500")),
                        ft.DataCell(ft.Text(str(pid), color=AppleTheme.TEXT_GREY, size=12)),
                        ft.DataCell(ft.Text(f"{cpu:.1f}%", color=AppleTheme.ORANGE, size=13, weight="bold")),
                        ft.DataCell(ft.Text(f"{mem:.1f}%", color=AppleTheme.PURPLE, size=13, weight="bold")),
                    ]
                )
            )
        self.data_table.rows = new_rows
        self.data_table.update()
