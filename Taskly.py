import flet as ft
import psutil
import time
import threading
from collections import deque
from datetime import datetime

# ==========================================
# DEBUG FLAGS
# ==========================================
DEBUG = True  # Active les logs de debug
VERBOSE = True  # Logs très détaillés

def debug_log(message, level="INFO"):
    """Affiche un message de debug avec timestamp."""
    if DEBUG:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] [{level}] {message}")

def verbose_log(message):
    """Affiche un message verbose uniquement si VERBOSE=True."""
    if VERBOSE:
        debug_log(message, "VERBOSE")

# ==========================================
# 0. HELPER FUNCTIONS
# ==========================================
def with_opacity(opacity: float, color: str) -> str:
    """Applique manuellement l'opacité à une couleur Hex (#AARRGGBB)."""
    if not color.startswith("#"):
        return color 
    alpha = int(opacity * 255)
    code = color.lstrip("#")
    return f"#{alpha:02x}{code}"

def format_bytes(bytes_value):
    """Formate les bytes en unités lisibles."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

def format_uptime(seconds):
    """Formate l'uptime en format lisible."""
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    if days > 0:
        return f"{int(days)}d {int(hours)}h"
    elif hours > 0:
        return f"{int(hours)}h {int(minutes)}m"
    else:
        return f"{int(minutes)}m"

# ==========================================
# 1. DESIGN SYSTEM & CONSTANTS
# ==========================================
class AppleTheme:
    # Couleurs système (Dark Mode)
    BG_COLOR = "#1C1C1E"
    CARD_COLOR = "#2C2C2E"
    TEXT_WHITE = "#FFFFFF"
    TEXT_GREY = "#8E8E93"
    TRANSPARENT = "#00000000"   
    
    # Accents Apple
    BLUE = "#0A84FF"
    GREEN = "#30D158"
    ORANGE = "#FF9F0A"
    RED = "#FF453A"
    PURPLE = "#BF5AF2"
    YELLOW = "#FFD60A"
    PINK = "#FF375F"
    CYAN = "#64D2FF"

    # Styling
    BORDER_RADIUS = 18
    PADDING = 20

# ==========================================
# 2. DATA MANAGER (Model & Logic)
# ==========================================
class SystemDataManager:
    def __init__(self):
        debug_log("Initializing SystemDataManager")
        self.cpu_history = deque([0]*60, maxlen=60)
        self.ram_history = deque([0]*60, maxlen=60)
        self.net_history = deque([0]*60, maxlen=60)
        self.last_net_io = psutil.net_io_counters()
        self.last_time = time.time()
        self.boot_time = psutil.boot_time()
        debug_log("SystemDataManager initialized successfully")

    def get_metrics(self):
        """Récupère toutes les métriques système."""
        verbose_log("Fetching system metrics...")
        try:
            # 1. CPU
            cpu_pct = psutil.cpu_percent(interval=None)
            if cpu_pct is None: cpu_pct = 0.0
            self.cpu_history.append(cpu_pct)
            verbose_log(f"CPU: {cpu_pct:.1f}%")
            
            cpu_count = psutil.cpu_count(logical=False)
            cpu_count_logical = psutil.cpu_count(logical=True)
            cpu_freq = psutil.cpu_freq()
            
            # 2. Memory
            mem = psutil.virtual_memory()
            self.ram_history.append(mem.percent)
            verbose_log(f"RAM: {mem.percent:.1f}% ({mem.used / (1024**3):.1f} GB used)")
            
            # 3. Disk
            disk = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()
            
            # 4. Network Speed
            current_net_io = psutil.net_io_counters()
            current_time = time.time()
            elapsed = current_time - self.last_time
            
            if elapsed <= 0: elapsed = 1 

            bytes_sent = current_net_io.bytes_sent - self.last_net_io.bytes_sent
            bytes_recv = current_net_io.bytes_recv - self.last_net_io.bytes_recv
            
            upload_speed = (bytes_sent / 1024) / elapsed
            download_speed = (bytes_recv / 1024) / elapsed
            
            total_speed = upload_speed + download_speed
            self.net_history.append(min(total_speed / 10, 100))
            
            verbose_log(f"Network: ↓{download_speed:.0f} KB/s ↑{upload_speed:.0f} KB/s")
            
            self.last_net_io = current_net_io
            self.last_time = current_time

            # 5. Battery
            battery = psutil.sensors_battery()
            batt_pct = battery.percent if battery else 0
            batt_plugged = battery.power_plugged if battery else False
            batt_time_left = battery.secsleft if battery and battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
            
            # 6. System uptime
            uptime_seconds = time.time() - self.boot_time
            
            # 7. Temperature (si disponible)
            cpu_temp = None
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        if entries:
                            cpu_temp = entries[0].current
                            verbose_log(f"CPU Temp: {cpu_temp:.0f}°C")
                            break
            except Exception as e:
                debug_log(f"Could not read temperature: {e}", "WARNING")
                cpu_temp = None
            
            metrics = {
                "cpu_percent": cpu_pct,
                "cpu_count": cpu_count,
                "cpu_count_logical": cpu_count_logical,
                "cpu_freq": cpu_freq.current if cpu_freq else 0,
                "cpu_history": list(self.cpu_history),
                "cpu_temp": cpu_temp,
                
                "ram_percent": mem.percent,
                "ram_used_gb": mem.used / (1024**3),
                "ram_total_gb": mem.total / (1024**3),
                "ram_available_gb": mem.available / (1024**3),
                "ram_history": list(self.ram_history),
                
                "disk_percent": disk.percent,
                "disk_used_gb": disk.used / (1024**3),
                "disk_total_gb": disk.total / (1024**3),
                "disk_read": disk_io.read_bytes if disk_io else 0,
                "disk_write": disk_io.write_bytes if disk_io else 0,
                
                "net_up": upload_speed,
                "net_down": download_speed,
                "net_total_sent": current_net_io.bytes_sent,
                "net_total_recv": current_net_io.bytes_recv,
                "net_history": list(self.net_history),
                
                "battery_percent": batt_pct,
                "battery_plugged": batt_plugged,
                "battery_time_left": batt_time_left,
                
                "uptime": uptime_seconds,
            }
            
            return metrics
            
        except Exception as e:
            debug_log(f"Error fetching metrics: {e}", "ERROR")
            import traceback
            traceback.print_exc()
            # Retourne des valeurs par défaut en cas d'erreur
            return {
                "cpu_percent": 0, "cpu_count": 0, "cpu_count_logical": 0,
                "cpu_freq": 0, "cpu_history": [0]*60, "cpu_temp": None,
                "ram_percent": 0, "ram_used_gb": 0, "ram_total_gb": 0,
                "ram_available_gb": 0, "ram_history": [0]*60,
                "disk_percent": 0, "disk_used_gb": 0, "disk_total_gb": 0,
                "disk_read": 0, "disk_write": 0,
                "net_up": 0, "net_down": 0, "net_total_sent": 0,
                "net_total_recv": 0, "net_history": [0]*60,
                "battery_percent": 0, "battery_plugged": False,
                "battery_time_left": None, "uptime": 0,
            }

    def get_top_processes(self, limit=7, sort_by='cpu'):
        """Récupère les processus les plus gourmands."""
        verbose_log(f"Fetching top {limit} processes (sorted by {sort_by})")
        procs = []
        try:
            for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    if p.info['cpu_percent'] is None:
                        p.info['cpu_percent'] = 0.0
                    if p.info['memory_percent'] is None:
                        p.info['memory_percent'] = 0.0
                    if p.info['name'] is None:
                        p.info['name'] = "Unknown"
                    procs.append(p.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                    verbose_log(f"Process access error: {e}")
                    pass
            
            sort_key = 'cpu_percent' if sort_by == 'cpu' else 'memory_percent'
            sorted_procs = sorted(procs, key=lambda p: p[sort_key] or 0, reverse=True)
            verbose_log(f"Found {len(procs)} processes, returning top {limit}")
            return sorted_procs[:limit]
        except Exception as e:
            debug_log(f"Error getting processes: {e}", "ERROR")
            return []

# ==========================================
# 3. UI COMPONENTS
# ==========================================
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
            if cpu is None: cpu = 0.0
            if mem is None: mem = 0.0

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

class SystemInfoPanel(ft.Container):
    """Panel d'informations système détaillées."""
    def __init__(self):
        super().__init__()
        
        self.cpu_info = ft.Text("", size=12, color=AppleTheme.TEXT_GREY)
        self.disk_info = ft.Text("", size=12, color=AppleTheme.TEXT_GREY)
        self.uptime_info = ft.Text("", size=12, color=AppleTheme.TEXT_GREY)
        self.battery_info = ft.Text("", size=12, color=AppleTheme.TEXT_GREY)
        
        self.content = ft.Column(
            controls=[
                ft.Text("System Info", size=16, weight="w600", color=AppleTheme.TEXT_WHITE),
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

# ==========================================
# 4. MAIN APPLICATION (DashboardUI)
# ==========================================
class DashboardUI:
    def __init__(self, page: ft.Page):
        debug_log("=" * 60)
        debug_log("TASKLY - SYSTEM MONITOR STARTING")
        debug_log("=" * 60)
        self.page = page
        self.data_manager = SystemDataManager()
        self.running = True
        self.current_sort = 'cpu'
        self.show_details = False
        
        debug_log("Setting up page...")
        self.setup_page()
        debug_log("Building UI...")
        self.build_ui()
        debug_log("Starting monitoring thread...")
        self.start_monitoring()
        debug_log("Taskly initialization complete!")

    def setup_page(self):
        debug_log("Configuring page settings")
        self.page.title = "Taskly - System Monitor"
        self.page.bgcolor = AppleTheme.BG_COLOR
        self.page.padding = 30
        self.page.theme_mode = ft.ThemeMode.DARK
        
        self.page.fonts = {
            "SF Pro": "https://raw.githubusercontent.com/google/fonts/main/ofl/sfpro/SFPro-Regular.ttf"
        }
        self.page.theme = ft.Theme(font_family="SF Pro")
        
        self.page.window.width = 1200
        self.page.window.height = 850
        self.page.window.min_width = 900
        self.page.window.min_height = 700
        debug_log(f"Window size: {self.page.window.width}x{self.page.window.height}")

    def toggle_details(self, e):
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

    def build_ui(self):
        debug_log("Building UI components...")
        # Header avec horloge
        self.clock_text = ft.Text(
            datetime.now().strftime("%H:%M:%S"),
            size=12,
            color=AppleTheme.TEXT_GREY
        )
        
        header = ft.Row(
            controls=[
                ft.Row([
                    ft.Text("Taskly", size=28, weight="bold", color=AppleTheme.TEXT_WHITE),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CIRCLE, color=AppleTheme.GREEN, size=8),
                            ft.Text("Live", color=AppleTheme.GREEN, size=12, weight="bold")
                        ], spacing=5),
                        bgcolor=with_opacity(0.2, AppleTheme.GREEN),
                        padding=ft.padding.symmetric(horizontal=10, vertical=5),
                        border_radius=20
                    )
                ], spacing=15),
                ft.Row([
                    self.clock_text,
                    ft.IconButton(
                        icon=ft.Icons.INFO_OUTLINE,
                        icon_color=AppleTheme.BLUE,
                        on_click=self.toggle_details,
                        tooltip="Toggle System Info"
                    )
                ], spacing=10)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        debug_log("Header created")

        # Metric Cards
        debug_log("Creating metric cards...")
        self.cpu_card = MetricCard("CPU Usage", ft.Icons.MEMORY, AppleTheme.BLUE, "%")
        self.ram_card = MetricCard("Memory", ft.Icons.SD_STORAGE, AppleTheme.PURPLE, "%")
        self.net_card = MetricCard("Network", ft.Icons.WIFI, AppleTheme.GREEN, " KB/s")

        top_row = ft.Row(
            controls=[self.cpu_card, self.ram_card, self.net_card],
            spacing=20,
        )
        debug_log("Metric cards created")

        # System Info Panel (caché par défaut)
        debug_log("Creating system info panel...")
        self.info_panel = SystemInfoPanel()

        # Bottom Row avec graphiques
        debug_log("Creating chart and process list...")
        self.chart_component = CPULineChart()
        self.process_component = ProcessList(on_sort_change=self._handle_sort_change)

        bottom_row = ft.Row(
            controls=[self.chart_component, self.process_component],
            spacing=20,
            expand=True 
        )
        debug_log("Charts created")

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
        
        debug_log("Adding layout to page...")
        self.page.add(self.layout)
        debug_log("UI build complete!")

    def _handle_sort_change(self, sort_type):
        debug_log(f"Process sort changed to: {sort_type}")
        self.current_sort = sort_type

    def start_monitoring(self):
        debug_log("Starting monitoring thread...")
        monitor_thread = threading.Thread(target=self._update_loop, daemon=True)
        monitor_thread.start()
        debug_log("Monitoring thread started")

    def _update_loop(self):
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

                # Mise à jour du graphique et de la liste
                verbose_log("Updating chart and process list...")
                self.chart_component.update_chart(metrics['cpu_history'])
                self.process_component.update_processes(top_procs)
                
                # Mise à jour info panel si visible
                if self.show_details:
                    verbose_log("Updating info panel...")
                    self.info_panel.update_info(metrics)

                verbose_log(f"Update iteration {iteration} complete")
                time.sleep(1)
                
            except Exception as e:
                debug_log(f"ERROR in update loop (iteration {iteration}): {e}", "ERROR")
                import traceback
                traceback.print_exc()
                time.sleep(1)

def main(page: ft.Page):
    app = DashboardUI(page)

if __name__ == "__main__":
    ft.app(target=main)