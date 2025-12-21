import tkinter as tk
from tkinter import ttk
import psutil
import time
import platform
import datetime
from typing import List, Tuple, Dict, Any

# --- CONFIGURATION & CONSTANTES ---
class Config:
    """Centralise la configuration visuelle et les paramètres."""
    APP_TITLE = "Taskly Monitor"
    APP_SIZE = "640x520"
    REFRESH_RATE_MS = 1000
    
    COLOR_BG = "#1e1e1e"
    COLOR_PANEL = "#252526"
    COLOR_TEXT = "#e0e0e0"
    COLOR_ACCENT = "#007acc"
    COLOR_GRAPH = "#00ffcc"

    FONT_HEADER = ("Helvetica", 10, "bold")
    FONT_BODY = ("Helvetica", 9)
    FONT_MONO = ("Menlo", 10)

# --- GESTION DES DONNÉES (BACKEND) ---
class SystemDataManager:
    def __init__(self):
        self.last_net_io = psutil.net_io_counters()
        self.cpu_history: List[float] = [0.0] * 60

    def get_basic_stats(self) -> Dict[str, Any]:
        cpu = psutil.cpu_percent(interval=None)
        self._update_cpu_history(cpu)
        
        return {
            "cpu": cpu,
            "ram": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
            "battery": psutil.sensors_battery()
        }

    def _update_cpu_history(self, value: float):
        self.cpu_history.pop(0)
        self.cpu_history.append(value)

    def get_network_speed(self) -> Tuple[float, float]:
        current_net = psutil.net_io_counters()
        bytes_recv = current_net.bytes_recv - self.last_net_io.bytes_recv
        bytes_sent = current_net.bytes_sent - self.last_net_io.bytes_sent
        self.last_net_io = current_net
        return (bytes_recv / 1024, bytes_sent / 1024)

    def get_top_processes(self, limit: int = 5) -> List[Dict]:
        """Récupère les processus les plus gourmands en CPU."""
        try:
            # CORRECTION ICI : On gère le cas où cpu_percent est None
            procs = sorted(
                psutil.process_iter(['name', 'cpu_percent']),
                key=lambda p: (p.info['cpu_percent'] or 0.0), # <-- La correction est ici (or 0.0)
                reverse=True
            )
            return [p.info for p in procs[:limit]]
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return []

    @staticmethod
    def get_system_info() -> str:
        node = platform.node().split('.')[0]
        os_ver = platform.mac_ver()[0]
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = str(datetime.datetime.now() - boot_time).split('.')[0]
        return f"🖥️ {node}  |  🍏 macOS {os_ver}  |  ⏱️ Uptime: {uptime}"

# --- COMPOSANTS UI (FRONTEND) ---
class GaugeWidget(tk.Frame):
    def __init__(self, parent, title: str):
        super().__init__(parent, bg=Config.COLOR_PANEL)
        self.pack(fill="x", pady=6)
        
        header = tk.Frame(self, bg=Config.COLOR_PANEL)
        header.pack(fill="x")
        
        tk.Label(header, text=title, bg=Config.COLOR_PANEL, fg=Config.COLOR_TEXT, 
                 font=Config.FONT_BODY).pack(side="left")
        
        self.val_label = tk.Label(header, text="0%", bg=Config.COLOR_PANEL, 
                                  fg=Config.COLOR_ACCENT, font=Config.FONT_HEADER)
        self.val_label.pack(side="right")
        
        self.progress = ttk.Progressbar(self, length=100, mode='determinate', 
                                        style="Blue.Horizontal.TProgressbar")
        self.progress.pack(fill="x", pady=(2, 0))

    def update_value(self, value: float, suffix: str = "%"):
        self.progress['value'] = value
        self.val_label.config(text=f"{value:.1f}{suffix}")

class GraphWidget(tk.Canvas):
    def __init__(self, parent, height=100):
        super().__init__(parent, height=height, bg="#111111", highlightthickness=0)
        self.pack(fill="x", pady=(5, 15))

    def draw_history(self, data: List[float]):
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width <= 1: return
        
        step = width / (len(data) - 1)
        points = []
        
        for i, val in enumerate(data):
            x = i * step
            y = height - (val / 100 * height)
            points.extend([x, y])
            
        if len(points) >= 4:
            self.create_line(points, fill=Config.COLOR_GRAPH, width=2, smooth=True)

# --- APPLICATION PRINCIPALE ---
class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.data_manager = SystemDataManager()
        
        self._setup_window()
        self._setup_styles()
        self._build_ui()
        
        self.update_loop()

    def _setup_window(self):
        self.root.title(Config.APP_TITLE)
        self.root.geometry(Config.APP_SIZE)
        self.root.resizable(False, False)
        self.root.configure(bg=Config.COLOR_BG)

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Blue.Horizontal.TProgressbar", 
                        foreground=Config.COLOR_ACCENT, 
                        background=Config.COLOR_ACCENT, 
                        troughcolor="#333333", 
                        borderwidth=0)

    def _build_ui(self):
        info_frame = tk.Frame(self.root, bg="#333333", height=40)
        info_frame.pack(fill="x")
        self.lbl_info = tk.Label(info_frame, text="Loading...", bg="#333333", fg="white", font=Config.FONT_BODY)
        self.lbl_info.pack(pady=8)

        main_container = tk.Frame(self.root, bg=Config.COLOR_BG)
        main_container.pack(fill="both", expand=True, padx=15, pady=15)

        # Colonne Gauche
        left_col = tk.Frame(main_container, bg=Config.COLOR_PANEL, padx=10, pady=10)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        tk.Label(left_col, text="RESSOURCES", bg=Config.COLOR_PANEL, fg="gray", 
                 font=Config.FONT_HEADER).pack(anchor="w", pady=(0, 5))
        
        self.gauge_cpu = GaugeWidget(left_col, "CPU Usage")
        self.gauge_ram = GaugeWidget(left_col, "RAM Usage")
        self.gauge_disk = GaugeWidget(left_col, "SSD Disk")
        self.gauge_bat = GaugeWidget(left_col, "Batterie")

        # Colonne Droite
        right_col = tk.Frame(main_container, bg=Config.COLOR_PANEL, padx=10, pady=10)
        right_col.pack(side="right", fill="both", expand=True, padx=(8, 0))
        
        tk.Label(right_col, text="HISTORIQUE CPU", bg=Config.COLOR_PANEL, fg="gray", font=Config.FONT_HEADER).pack(anchor="w")
        self.graph = GraphWidget(right_col)
        
        tk.Label(right_col, text="TOP PROCESSUS", bg=Config.COLOR_PANEL, fg="gray", font=Config.FONT_HEADER).pack(anchor="w")
        self.lbl_processes = tk.Label(right_col, text="", bg=Config.COLOR_PANEL, fg="#bbbbbb", font=Config.FONT_MONO, justify="left")
        self.lbl_processes.pack(anchor="w", pady=5)

        # Footer
        self.status_bar = tk.Label(self.root, text="Ready", bg=Config.COLOR_ACCENT, fg="white", font=Config.FONT_HEADER, pady=5)
        self.status_bar.pack(fill="x", side="bottom")

    def update_loop(self):
        stats = self.data_manager.get_basic_stats()
        net_recv, net_sent = self.data_manager.get_network_speed()
        top_procs = self.data_manager.get_top_processes()
        
        self.lbl_info.config(text=self.data_manager.get_system_info())
        
        self.gauge_cpu.update_value(stats['cpu'])
        self.gauge_ram.update_value(stats['ram'])
        self.gauge_disk.update_value(stats['disk'])
        
        bat = stats['battery']
        if bat:
            icon = "⚡" if bat.power_plugged else "🔋"
            self.gauge_bat.update_value(bat.percent, suffix=f"% {icon}")

        self.graph.draw_history(self.data_manager.cpu_history)

        # Protection contre les erreurs si 'top_procs' est vide
        if top_procs:
            proc_text = "\n".join([f"{(p['cpu_percent'] or 0.0):>5.1f}%  {p['name']}" for p in top_procs])
        else:
            proc_text = "Chargement..."
            
        self.lbl_processes.config(text=proc_text)
        self.status_bar.config(text=f"RÉSEAU: ⬇️ {net_recv:.1f} KB/s   |   ⬆️ {net_sent:.1f} KB/s")
        
        self.root.after(Config.REFRESH_RATE_MS, self.update_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()