"""
Gestionnaire de données système pour Taskly.
"""
import psutil
import time
from collections import deque
from utils import debug_log, verbose_log


class SystemDataManager:
    """Gère la collecte et le stockage des métriques système."""
    
    def __init__(self):
        debug_log("Initializing SystemDataManager")
        # Optimized: Reduced history size from 60 to 30 for better memory usage
        self.cpu_history = deque([0]*30, maxlen=30)
        self.ram_history = deque([0]*30, maxlen=30)
        self.net_history = deque([0]*30, maxlen=30)
        self.net_down_history = deque([0]*30, maxlen=30)
        self.net_up_history = deque([0]*30, maxlen=30)
        self.temp_history = deque([0]*30, maxlen=30)
        self.last_net_io = psutil.net_io_counters()
        self.last_time = time.time()
        self.boot_time = psutil.boot_time()
        # Cache for expensive operations
        self.last_disk_check = 0
        self.cached_disk_info = None
        self.last_battery_check = 0
        self.cached_battery_info = None
        debug_log("SystemDataManager initialized successfully")

    def get_metrics(self):
        """Récupère toutes les métriques système."""
        verbose_log("Fetching system metrics...")
        try:
            # 1. CPU
            # Note: psutil.cpu_percent() retourne déjà une valeur normalisée 0-100%
            # même sur multi-core (moyenne de tous les cores)
            cpu_pct = psutil.cpu_percent(interval=None)
            if cpu_pct is None:
                cpu_pct = 0.0
            
            # Assurer que la valeur reste dans 0-100%
            cpu_pct = min(max(cpu_pct, 0), 100)
            
            self.cpu_history.append(cpu_pct)
            verbose_log(f"CPU: {cpu_pct:.1f}%")
            
            cpu_count = psutil.cpu_count(logical=False)
            cpu_count_logical = psutil.cpu_count(logical=True)
            cpu_freq = psutil.cpu_freq()
            
            # 2. Memory
            mem = psutil.virtual_memory()
            self.ram_history.append(mem.percent)
            verbose_log(f"RAM: {mem.percent:.1f}% ({mem.used / (1024**3):.1f} GB used)")
            
            # 3. Disk (cached - updated every 5 seconds)
            current_time_disk = time.time()
            if self.cached_disk_info is None or (current_time_disk - self.last_disk_check) > 5:
                disk = psutil.disk_usage('/')
                disk_io = psutil.disk_io_counters()
                self.cached_disk_info = {
                    'percent': disk.percent,
                    'used_gb': disk.used / (1024**3),
                    'total_gb': disk.total / (1024**3),
                    'read': disk_io.read_bytes if disk_io else 0,
                    'write': disk_io.write_bytes if disk_io else 0
                }
                self.last_disk_check = current_time_disk
                verbose_log(f"Disk cache updated: {disk.percent:.1f}%")
            
            # 4. Network Speed
            current_net_io = psutil.net_io_counters()
            current_time = time.time()
            elapsed = current_time - self.last_time
            
            if elapsed <= 0:
                elapsed = 1

            bytes_sent = current_net_io.bytes_sent - self.last_net_io.bytes_sent
            bytes_recv = current_net_io.bytes_recv - self.last_net_io.bytes_recv
            
            upload_speed = (bytes_sent / 1024) / elapsed
            download_speed = (bytes_recv / 1024) / elapsed
            
            total_speed = upload_speed + download_speed
            self.net_history.append(min(total_speed / 10, 100))
            self.net_down_history.append(download_speed)
            self.net_up_history.append(upload_speed)
            
            verbose_log(f"Network: ↓{download_speed:.0f} KB/s ↑{upload_speed:.0f} KB/s")
            
            self.last_net_io = current_net_io
            self.last_time = current_time

            # 5. Battery (cached - updated every 5 seconds)
            if self.cached_battery_info is None or (current_time_disk - self.last_battery_check) > 5:
                battery = psutil.sensors_battery()
                self.cached_battery_info = {
                    'percent': battery.percent if battery else 0,
                    'plugged': battery.power_plugged if battery else False,
                    'time_left': battery.secsleft if battery and battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
                }
                self.last_battery_check = current_time_disk
                verbose_log(f"Battery cache updated: {self.cached_battery_info['percent']:.0f}%")
            
            # 6. System uptime
            uptime_seconds = time.time() - self.boot_time
            
            # 7. Temperature (improved detection)
            cpu_temp = None
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    # Priority order: coretemp (Linux), k10temp (AMD), CPU Thermal (macOS)
                    priority_sensors = ['coretemp', 'k10temp', 'cpu_thermal', 'cpu-thermal']
                    
                    # Try priority sensors first
                    for sensor_name in priority_sensors:
                        if sensor_name in temps and temps[sensor_name]:
                            cpu_temp = temps[sensor_name][0].current
                            verbose_log(f"CPU Temp ({sensor_name}): {cpu_temp:.0f}°C")
                            break
                    
                    # Fallback: use first available sensor
                    if cpu_temp is None:
                        for name, entries in temps.items():
                            if entries and entries[0].current > 0:
                                cpu_temp = entries[0].current
                                verbose_log(f"CPU Temp ({name}): {cpu_temp:.0f}°C")
                                break
            except (AttributeError, OSError) as e:
                debug_log(f"Temperature sensors not available: {e}", "WARNING")
                cpu_temp = None
            except Exception as e:
                debug_log(f"Could not read temperature: {e}", "WARNING")
                cpu_temp = None
            
            # Add to temperature history
            self.temp_history.append(cpu_temp if cpu_temp else 0)
            
            metrics = {
                "cpu_percent": cpu_pct,
                "cpu_count": cpu_count,
                "cpu_count_logical": cpu_count_logical,
                "cpu_freq": cpu_freq.current if cpu_freq else 0,
                "cpu_history": list(self.cpu_history),
                "cpu_temp": cpu_temp,
                "temp_history": list(self.temp_history),
                
                "ram_percent": mem.percent,
                "ram_used_gb": mem.used / (1024**3),
                "ram_total_gb": mem.total / (1024**3),
                "ram_available_gb": mem.available / (1024**3),
                "ram_history": list(self.ram_history),
                
                "disk_percent": self.cached_disk_info['percent'],
                "disk_used_gb": self.cached_disk_info['used_gb'],
                "disk_total_gb": self.cached_disk_info['total_gb'],
                "disk_read": self.cached_disk_info['read'],
                "disk_write": self.cached_disk_info['write'],
                
                "net_up": upload_speed,
                "net_down": download_speed,
                "net_total_sent": current_net_io.bytes_sent,
                "net_total_recv": current_net_io.bytes_recv,
                "net_history": list(self.net_history),
                "net_down_history": list(self.net_down_history),
                "net_up_history": list(self.net_up_history),
                
                "battery_percent": self.cached_battery_info['percent'],
                "battery_plugged": self.cached_battery_info['plugged'],
                "battery_time_left": self.cached_battery_info['time_left'],
                
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
                "cpu_freq": 0, "cpu_history": [0]*30, "cpu_temp": None, "temp_history": [0]*30,
                "ram_percent": 0, "ram_used_gb": 0, "ram_total_gb": 0,
                "ram_available_gb": 0, "ram_history": [0]*30,
                "disk_percent": 0, "disk_used_gb": 0, "disk_total_gb": 0,
                "disk_read": 0, "disk_write": 0,
                "net_up": 0, "net_down": 0, "net_total_sent": 0,
                "net_total_recv": 0, "net_history": [0]*30,
                "net_down_history": [0]*30, "net_up_history": [0]*30,
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
