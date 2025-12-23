"""
Gestionnaire de données système pour Taskly.
Version refactorisée et optimisée.
"""
import psutil
import time
from collections import deque
from utils import debug_log, verbose_log
from constants import (
    HISTORY_SIZE, CACHE_INTERVAL_DISK, CACHE_INTERVAL_BATTERY,
    TOP_PROCESSES_LIMIT, NORMALIZE_CPU_BY_CORES
)


class SystemDataManager:
    """Gère la collecte et le stockage des métriques système de manière modulaire."""
    
    def __init__(self):
        debug_log("Initializing SystemDataManager")
        
        # Historiques optimisés
        self.cpu_history = deque([0] * HISTORY_SIZE, maxlen=HISTORY_SIZE)
        self.ram_history = deque([0] * HISTORY_SIZE, maxlen=HISTORY_SIZE)
        self.net_history = deque([0] * HISTORY_SIZE, maxlen=HISTORY_SIZE)
        self.net_down_history = deque([0] * HISTORY_SIZE, maxlen=HISTORY_SIZE)
        self.net_up_history = deque([0] * HISTORY_SIZE, maxlen=HISTORY_SIZE)

        # État réseau
        self.last_net_io = psutil.net_io_counters()
        self.last_time = time.time()
        
        # Informations système
        self.boot_time = psutil.boot_time()
        self.cpu_count = psutil.cpu_count(logical=True) or 1
        
        # Cache pour opérations coûteuses
        self.last_disk_check = 0
        self.cached_disk_info = None
        self.last_battery_check = 0
        self.cached_battery_info = None
        
        debug_log("SystemDataManager initialized successfully")

    def _should_update_cache(self, last_check_time, interval):
        """Vérifie si le cache doit être mis à jour."""
        return time.time() - last_check_time > interval

    def _get_cpu_metrics(self):
        """Collecte les métriques CPU."""
        try:
            # CPU percentage (déjà normalisé 0-100% par psutil pour le système global)
            cpu_pct = psutil.cpu_percent(interval=None)
            if cpu_pct is None:
                cpu_pct = 0.0
            
            # Assurer que la valeur reste dans 0-100%
            cpu_pct = min(max(cpu_pct, 0), 100)
            self.cpu_history.append(cpu_pct)
            
            verbose_log(f"CPU: {cpu_pct:.1f}%")
            
            # Informations CPU
            cpu_count = psutil.cpu_count(logical=False)
            cpu_count_logical = psutil.cpu_count(logical=True)
            cpu_freq = psutil.cpu_freq()
            
            return {
                'cpu_percent': cpu_pct,
                'cpu_count': cpu_count,
                'cpu_count_logical': cpu_count_logical,
                'cpu_freq': cpu_freq.current if cpu_freq else 0,
                'cpu_history': list(self.cpu_history),
            }
        except Exception as e:
            debug_log(f"Error fetching CPU metrics: {e}", "ERROR")
            return {
                'cpu_percent': 0,
                'cpu_count': 0,
                'cpu_count_logical': 0,
                'cpu_freq': 0,
                'cpu_history': list(self.cpu_history),
            }

    def _get_memory_metrics(self):
        """Collecte les métriques mémoire."""
        try:
            mem = psutil.virtual_memory()
            self.ram_history.append(mem.percent)
            
            verbose_log(f"RAM: {mem.percent:.1f}% ({mem.used / (1024**3):.1f} GB used)")
            
            return {
                'ram_percent': mem.percent,
                'ram_used_gb': mem.used / (1024**3),
                'ram_total_gb': mem.total / (1024**3),
                'ram_available_gb': mem.available / (1024**3),
                'ram_history': list(self.ram_history),
            }
        except Exception as e:
            debug_log(f"Error fetching memory metrics: {e}", "ERROR")
            return {
                'ram_percent': 0,
                'ram_used_gb': 0,
                'ram_total_gb': 0,
                'ram_available_gb': 0,
                'ram_history': list(self.ram_history),
            }

    def _get_disk_metrics(self):
        """Collecte les métriques disque (avec cache)."""
        try:
            if self.cached_disk_info is None or self._should_update_cache(
                self.last_disk_check, CACHE_INTERVAL_DISK
            ):
                disk = psutil.disk_usage('/')
                disk_io = psutil.disk_io_counters()
                
                self.cached_disk_info = {
                    'disk_percent': disk.percent,
                    'disk_used_gb': disk.used / (1024**3),
                    'disk_total_gb': disk.total / (1024**3),
                    'disk_read': disk_io.read_bytes if disk_io else 0,
                    'disk_write': disk_io.write_bytes if disk_io else 0,
                }
                self.last_disk_check = time.time()
                verbose_log(f"Disk cache updated: {disk.percent:.1f}%")
            
            return self.cached_disk_info
        except Exception as e:
            debug_log(f"Error fetching disk metrics: {e}", "ERROR")
            return {
                'disk_percent': 0,
                'disk_used_gb': 0,
                'disk_total_gb': 0,
                'disk_read': 0,
                'disk_write': 0,
            }

    def _get_network_metrics(self):
        """Collecte les métriques réseau."""
        try:
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

            return {
                'net_up': upload_speed,
                'net_down': download_speed,
                'net_total_sent': current_net_io.bytes_sent,
                'net_total_recv': current_net_io.bytes_recv,
                'net_history': list(self.net_history),
                'net_down_history': list(self.net_down_history),
                'net_up_history': list(self.net_up_history),
            }
        except Exception as e:
            debug_log(f"Error fetching network metrics: {e}", "ERROR")
            return {
                'net_up': 0,
                'net_down': 0,
                'net_total_sent': 0,
                'net_total_recv': 0,
                'net_history': list(self.net_history),
                'net_down_history': list(self.net_down_history),
                'net_up_history': list(self.net_up_history),
            }

    def _get_battery_metrics(self):
        """Collecte les métriques batterie (avec cache)."""
        try:
            if self.cached_battery_info is None or self._should_update_cache(
                self.last_battery_check, CACHE_INTERVAL_BATTERY
            ):
                battery = psutil.sensors_battery()
                
                self.cached_battery_info = {
                    'battery_percent': battery.percent if battery else 0,
                    'battery_plugged': battery.power_plugged if battery else False,
                    'battery_time_left': battery.secsleft if battery and battery.secsleft != psutil.POWER_TIME_UNLIMITED else None,
                }
                self.last_battery_check = time.time()
                verbose_log(f"Battery cache updated: {self.cached_battery_info['battery_percent']:.0f}%")
            
            return self.cached_battery_info
        except Exception as e:
            debug_log(f"Error fetching battery metrics: {e}", "ERROR")
            return {
                'battery_percent': 0,
                'battery_plugged': False,
                'battery_time_left': None,
            }

    def _get_system_metrics(self):
        """Collecte les métriques système générales."""
        try:
            uptime_seconds = time.time() - self.boot_time
            return {'uptime': uptime_seconds}
        except Exception as e:
            debug_log(f"Error fetching system metrics: {e}", "ERROR")
            return {'uptime': 0}

    def get_metrics(self):
        """
        Récupère toutes les métriques système.
        Méthode principale qui agrège toutes les métriques.
        """
        verbose_log("Fetching system metrics...")
        
        try:
            # Collecter toutes les métriques via les méthodes modulaires
            metrics = {}
            metrics.update(self._get_cpu_metrics())
            metrics.update(self._get_memory_metrics())
            metrics.update(self._get_disk_metrics())
            metrics.update(self._get_network_metrics())
            metrics.update(self._get_battery_metrics())
            metrics.update(self._get_system_metrics())
            
            return metrics
            
        except Exception as e:
            debug_log(f"Error in get_metrics: {e}", "ERROR")
            import traceback
            traceback.print_exc()
            
            # Retourne des valeurs par défaut en cas d'erreur critique
            return self._get_default_metrics()

    def _get_default_metrics(self):
        """Retourne des métriques par défaut en cas d'erreur."""
        return {
            'cpu_percent': 0, 'cpu_count': 0, 'cpu_count_logical': 0,
            'cpu_freq': 0, 'cpu_history': [0] * HISTORY_SIZE,
            'ram_percent': 0, 'ram_used_gb': 0, 'ram_total_gb': 0,
            'ram_available_gb': 0, 'ram_history': [0] * HISTORY_SIZE,
            'disk_percent': 0, 'disk_used_gb': 0, 'disk_total_gb': 0,
            'disk_read': 0, 'disk_write': 0,
            'net_up': 0, 'net_down': 0, 'net_total_sent': 0,
            'net_total_recv': 0, 'net_history': [0] * HISTORY_SIZE,
            'net_down_history': [0] * HISTORY_SIZE, 'net_up_history': [0] * HISTORY_SIZE,
            'battery_percent': 0, 'battery_plugged': False,
            'battery_time_left': None, 'uptime': 0,
        }

    def get_top_processes(self, limit=TOP_PROCESSES_LIMIT, sort_by='cpu', normalize_cpu=NORMALIZE_CPU_BY_CORES):
        """
        Récupère les processus les plus gourmands.
        
        Args:
            limit: Nombre de processus à retourner
            sort_by: 'cpu' ou 'memory'
            normalize_cpu: Si True, normalise CPU par nombre de cœurs (0-100%)
                          Si False, affiche le total (peut dépasser 100%)
        
        Returns:
            Liste des processus triés
        """
        verbose_log(f"Fetching top {limit} processes (sorted by {sort_by}, normalize={normalize_cpu})")
        procs = []
        
        try:
            for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    # Valeurs par défaut si None
                    cpu_pct = p.info['cpu_percent'] or 0.0
                    mem_pct = p.info['memory_percent'] or 0.0
                    name = p.info['name'] or "Unknown"
                    
                    # FIX: Normaliser CPU par nombre de cœurs pour obtenir 0-100%
                    if normalize_cpu and cpu_pct > 0:
                        # Sur un système multi-cœurs, psutil peut retourner >100%
                        # Ex: 2 cœurs à 100% = 200% CPU
                        # On normalise: 200% / 2 cœurs = 100%
                        # Note: psutil retourne déjà un %, donc pas besoin de *100
                        cpu_pct = min(cpu_pct / self.cpu_count, 100)
                    
                    procs.append({
                        'pid': p.info['pid'],
                        'name': name,
                        'cpu_percent': cpu_pct,
                        'memory_percent': mem_pct,
                    })
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # Processus terminé ou accès refusé, on ignore
                    pass
            
            # Tri par CPU ou mémoire
            sort_key = 'cpu_percent' if sort_by == 'cpu' else 'memory_percent'
            sorted_procs = sorted(procs, key=lambda p: p[sort_key], reverse=True)
            
            verbose_log(f"Found {len(procs)} processes, returning top {limit}")
            return sorted_procs[:limit]
            
        except Exception as e:
            debug_log(f"Error getting processes: {e}", "ERROR")
            return []
