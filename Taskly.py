import flet as ft
import psutil
import time
import threading
from collections import deque

# ==========================================
# 0. HELPER FUNCTIONS
# ==========================================
def with_opacity(opacity: float, color: str) -> str:
    """
    Applique manuellement l'opacité à une couleur Hex (#AARRGGBB).
    """
    if not color.startswith("#"):
        return color 
    alpha = int(opacity * 255)
    code = color.lstrip("#")
    return f"#{alpha:02x}{code}"

# ==========================================
# 1. DESIGN SYSTEM & CONSTANTS
# ==========================================
class AppleTheme:
    # Couleurs système (Dark Mode)
    BG_COLOR = "#1C1C1E"        # System Gray 6
    CARD_COLOR = "#2C2C2E"      # Secondary System Background
    TEXT_WHITE = "#FFFFFF"
    TEXT_GREY = "#8E8E93"       # System Gray
    TRANSPARENT = "#00000000"   
    
    # Accents Apple
    BLUE = "#0A84FF"
    GREEN = "#30D158"
    ORANGE = "#FF9F0A"
    RED = "#FF453A"
    PURPLE = "#BF5AF2"

    # Styling
    BORDER_RADIUS = 18
    PADDING = 20

# ==========================================
# 2. DATA MANAGER (Model & Logic)
# ==========================================
class SystemDataManager:
    def __init__(self):
        self.cpu_history = deque([0]*60, maxlen=60) # Historique 60 sec
        self.last_net_io = psutil.net_io_counters()
        self.last_time = time.time()

    def get_metrics(self):
        """Récupère toutes les métriques système."""
        
        # 1. CPU
        cpu_pct = psutil.cpu_percent(interval=None)
        # Sécurité : si psutil renvoie None, on met 0.0
        if cpu_pct is None: cpu_pct = 0.0
        
        self.cpu_history.append(cpu_pct)
        
        # 2. Memory
        mem = psutil.virtual_memory()
        
        # 3. Network Speed
        current_net_io = psutil.net_io_counters()
        current_time = time.time()
        elapsed = current_time - self.last_time
        
        if elapsed <= 0: elapsed = 1 

        bytes_sent = current_net_io.bytes_sent - self.last_net_io.bytes_sent
        bytes_recv = current_net_io.bytes_recv - self.last_net_io.bytes_recv
        
        upload_speed = (bytes_sent / 1024) / elapsed # KB/s
        download_speed = (bytes_recv / 1024) / elapsed # KB/s
        
        self.last_net_io = current_net_io
        self.last_time = current_time

        # 4. Battery
        battery = psutil.sensors_battery()
        batt_pct = battery.percent if battery else 0
        batt_plugged = battery.power_plugged if battery else False
        
        return {
            "cpu_percent": cpu_pct,
            "cpu_history": list(self.cpu_history),
            "ram_percent": mem.percent,
            "ram_used_gb": mem.used / (1024**3),
            "ram_total_gb": mem.total / (1024**3),
            "net_up": upload_speed,
            "net_down": download_speed,
            "battery_percent": batt_pct,
            "battery_plugged": batt_plugged
        }

    def get_top_processes(self, limit=7):
        """Récupère les processus les plus gourmands."""
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                # Force le calcul
                p.info['cpu_percent']
                
                # NETTOYAGE CRITIQUE : Si cpu_percent est None, on le force à 0.0
                if p.info['cpu_percent'] is None:
                    p.info['cpu_percent'] = 0.0
                
                # Gestion des noms None
                if p.info['name'] is None:
                    p.info['name'] = "Unknown"

                procs.append(p.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Tri par CPU décroissant (double sécurité sur le None avec 'or 0')
        sorted_procs = sorted(procs, key=lambda p: p['cpu_percent'] or 0, reverse=True)
        return sorted_procs[:limit]

# ==========================================
# 3. UI COMPONENTS
# ==========================================
class MetricCard(ft.Container):
    """Carte pour les métriques (CPU, RAM, Net)."""
    def __init__(self, title, icon, accent_color, value_suffix=""):
        super().__init__()
        self.accent_color = accent_color
        self.value_suffix = value_suffix
        
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

    def update_data(self, main_val, sub_val, progress_val):
        self.value_text.value = f"{main_val}{self.value_suffix}"
        self.sub_text.value = sub_val
        # Sécurité pour la barre de progression
        safe_progress = 0.0
        try:
            safe_progress = float(progress_val)
        except:
            safe_progress = 0.0
            
        self.progress_bar.value = min(max(safe_progress, 0), 1)
        self.update()

class CPULineChart(ft.Container):
    """Le graphique principal."""
    def __init__(self):
        super().__init__()
        self.data_points = [ft.LineChartDataPoint(i, 0) for i in range(60)]
        
        self.chart = ft.LineChart(
            data_series=[
                ft.LineChartData(
                    data_points=self.data_points,
                    stroke_width=2,
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
            left_axis=ft.ChartAxis(labels=[], show_labels=False),
            bottom_axis=ft.ChartAxis(labels=[], show_labels=False),
            tooltip_bgcolor=AppleTheme.CARD_COLOR,
            horizontal_grid_lines=ft.ChartGridLines(interval=25, color=with_opacity(0.1, "#FFFFFF"), width=1),
            vertical_grid_lines=ft.ChartGridLines(interval=10, color=with_opacity(0.1, "#FFFFFF"), width=1),
            border=ft.border.all(0, AppleTheme.TRANSPARENT) 
        )

        self.content = ft.Column(
            controls=[
                ft.Text("CPU History", size=16, weight="w600", color=AppleTheme.TEXT_WHITE),
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
                # Sécurité si val est None (ne devrait pas arriver avec les fix précédents)
                self.data_points[i].y = val if val is not None else 0
        self.chart.update()

class ProcessList(ft.Container):
    """Tableau des processus."""
    def __init__(self):
        super().__init__()
        
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Process", color=AppleTheme.TEXT_GREY, size=12)),
                ft.DataColumn(ft.Text("PID", color=AppleTheme.TEXT_GREY, size=12), numeric=True),
                ft.DataColumn(ft.Text("CPU%", color=AppleTheme.TEXT_GREY, size=12), numeric=True),
            ],
            rows=[],
            column_spacing=10,
            heading_row_height=30,
            data_row_min_height=40,
        )

        self.content = ft.Column(
            controls=[
                ft.Text("Top Processes", size=16, weight="w600", color=AppleTheme.TEXT_WHITE),
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

    def update_processes(self, procs):
        new_rows = []
        for p in procs:
            # Sécurité ultime avant affichage
            name = p.get('name', 'Unknown')
            pid = p.get('pid', 0)
            cpu = p.get('cpu_percent', 0.0)
            if cpu is None: cpu = 0.0

            new_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(name)[:15], color=AppleTheme.TEXT_WHITE, size=13, weight="w500")),
                        ft.DataCell(ft.Text(str(pid), color=AppleTheme.TEXT_GREY, size=12)),
                        ft.DataCell(ft.Text(f"{cpu:.1f}%", color=AppleTheme.ORANGE, size=13, weight="bold")),
                    ]
                )
            )
        self.data_table.rows = new_rows
        self.data_table.update()

# ==========================================
# 4. MAIN APPLICATION (DashboardUI)
# ==========================================
class DashboardUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.data_manager = SystemDataManager()
        self.running = True
        
        self.setup_page()
        self.build_ui()
        self.start_monitoring()

    def setup_page(self):
        self.page.title = "Taskly - System Monitor"
        self.page.bgcolor = AppleTheme.BG_COLOR
        self.page.padding = 30
        self.page.theme_mode = ft.ThemeMode.DARK
        
        self.page.fonts = {
            "SF Pro": "https://raw.githubusercontent.com/google/fonts/main/ofl/sfpro/SFPro-Regular.ttf"
        }
        self.page.theme = ft.Theme(font_family="SF Pro")
        
        self.page.window.width = 1000
        self.page.window.height = 800
        self.page.window.min_width = 800
        self.page.window.min_height = 600

    def build_ui(self):
        # Header
        header = ft.Row(
            controls=[
                ft.Text("Taskly", size=28, weight="bold", color=AppleTheme.TEXT_WHITE),
                ft.Container(
                    content=ft.Text("Live", color=AppleTheme.GREEN, size=12, weight="bold"),
                    bgcolor=with_opacity(0.2, AppleTheme.GREEN),
                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                    border_radius=20
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        # Metric Cards
        self.cpu_card = MetricCard("CPU Usage", ft.Icons.MEMORY, AppleTheme.BLUE, "%")
        self.ram_card = MetricCard("Memory", ft.Icons.SD_STORAGE, AppleTheme.PURPLE, "%")
        self.net_card = MetricCard("Network", ft.Icons.WIFI, AppleTheme.GREEN, " KB/s")

        top_row = ft.Row(
            controls=[self.cpu_card, self.ram_card, self.net_card],
            spacing=20,
        )

        # Bottom Row
        self.chart_component = CPULineChart()
        self.process_component = ProcessList()

        bottom_row = ft.Row(
            controls=[self.chart_component, self.process_component],
            spacing=20,
            expand=True 
        )

        self.layout = ft.Column(
            controls=[
                header,
                ft.Container(height=20),
                top_row,
                ft.Container(height=10),
                bottom_row
            ],
            expand=True
        )
        
        self.page.add(self.layout)

    def start_monitoring(self):
        monitor_thread = threading.Thread(target=self._update_loop, daemon=True)
        monitor_thread.start()

    def _update_loop(self):
        while self.running:
            try:
                metrics = self.data_manager.get_metrics()
                top_procs = self.data_manager.get_top_processes()

                # Mise à jour des cartes
                self.cpu_card.update_data(
                    f"{metrics['cpu_percent']:.1f}", 
                    "System Load", 
                    metrics['cpu_percent'] / 100
                )
                
                self.ram_card.update_data(
                    f"{metrics['ram_percent']:.1f}", 
                    f"{metrics['ram_used_gb']:.1f} GB / {metrics['ram_total_gb']:.1f} GB", 
                    metrics['ram_percent'] / 100
                )
                
                total_speed = metrics['net_down'] + metrics['net_up']
                max_ref_speed = 5000 
                self.net_card.update_data(
                    f"{metrics['net_down']:.0f}", 
                    f"Up: {metrics['net_up']:.0f} KB/s", 
                    min(total_speed / max_ref_speed, 1.0)
                )

                # Mise à jour du graphique et de la liste
                self.chart_component.update_chart(metrics['cpu_history'])
                self.process_component.update_processes(top_procs)

                time.sleep(1)
                
            except Exception as e:
                # Impression plus détaillée de l'erreur
                print(f"Error in UI Loop: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(1)

def main(page: ft.Page):
    app = DashboardUI(page)

if __name__ == "__main__":
    ft.app(target=main)