"""
Module d'export de données système.
"""
import json
import csv
from datetime import datetime
from pathlib import Path
from utils import debug_log
from constants import EXPORT_DIRECTORY


class DataExporter:
    """Gère l'export des métriques système."""
    
    def __init__(self, export_dir=EXPORT_DIRECTORY):
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(exist_ok=True)
        debug_log(f"DataExporter initialized, export directory: {self.export_dir}")
    
    def export_to_json(self, metrics, filename=None):
        """Exporte les métriques en JSON."""
        if filename is None:
            filename = f"taskly_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = self.export_dir / filename
        
        try:
            # Prepare data for JSON serialization
            export_data = {
                'timestamp': datetime.now().isoformat(),
                'metrics': {
                    'cpu': {
                        'percent': metrics['cpu_percent'],
                        'count': metrics['cpu_count'],
                        'freq_mhz': metrics['cpu_freq'],
                        'history': metrics['cpu_history']
                    },
                    'memory': {
                        'percent': metrics['ram_percent'],
                        'used_gb': metrics['ram_used_gb'],
                        'total_gb': metrics['ram_total_gb'],
                        'available_gb': metrics['ram_available_gb'],
                        'history': metrics['ram_history']
                    },
                    'disk': {
                        'percent': metrics['disk_percent'],
                        'used_gb': metrics['disk_used_gb'],
                        'total_gb': metrics['disk_total_gb']
                    },
                    'network': {
                        'upload_kbps': metrics['net_up'],
                        'download_kbps': metrics['net_down'],
                        'total_sent_bytes': metrics['net_total_sent'],
                        'total_recv_bytes': metrics['net_total_recv'],
                        'history': metrics['net_history']
                    },
                    'battery': {
                        'percent': metrics['battery_percent'],
                        'plugged': metrics['battery_plugged'],
                        'time_left_seconds': metrics['battery_time_left']
                    },
                    'system': {
                        'uptime_seconds': metrics['uptime']
                    }
                }
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)
            
            debug_log(f"Metrics exported to JSON: {filepath}")
            return str(filepath)
        
        except Exception as e:
            debug_log(f"Error exporting to JSON: {e}", "ERROR")
            return None
    
    def export_to_csv(self, metrics, filename=None):
        """Exporte les métriques en CSV."""
        if filename is None:
            filename = f"taskly_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = self.export_dir / filename
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Header
                writer.writerow(['Timestamp', datetime.now().isoformat()])
                writer.writerow([])
                
                # CPU
                writer.writerow(['CPU Metrics'])
                writer.writerow(['Usage %', 'Cores', 'Frequency MHz'])
                writer.writerow([
                    f"{metrics['cpu_percent']:.1f}",
                    metrics['cpu_count'],
                    f"{metrics['cpu_freq']:.0f}"
                ])
                writer.writerow([])
                
                # Memory
                writer.writerow(['Memory Metrics'])
                writer.writerow(['Usage %', 'Used GB', 'Total GB', 'Available GB'])
                writer.writerow([
                    f"{metrics['ram_percent']:.1f}",
                    f"{metrics['ram_used_gb']:.2f}",
                    f"{metrics['ram_total_gb']:.2f}",
                    f"{metrics['ram_available_gb']:.2f}"
                ])
                writer.writerow([])
                
                # Disk
                writer.writerow(['Disk Metrics'])
                writer.writerow(['Usage %', 'Used GB', 'Total GB'])
                writer.writerow([
                    f"{metrics['disk_percent']:.1f}",
                    f"{metrics['disk_used_gb']:.2f}",
                    f"{metrics['disk_total_gb']:.2f}"
                ])
                writer.writerow([])
                
                # Network
                writer.writerow(['Network Metrics'])
                writer.writerow(['Upload KB/s', 'Download KB/s', 'Total Sent GB', 'Total Received GB'])
                writer.writerow([
                    f"{metrics['net_up']:.2f}",
                    f"{metrics['net_down']:.2f}",
                    f"{metrics['net_total_sent'] / (1024**3):.2f}",
                    f"{metrics['net_total_recv'] / (1024**3):.2f}"
                ])
                writer.writerow([])
                
                # Battery
                writer.writerow(['Battery Metrics'])
                writer.writerow(['Level %', 'Plugged', 'Time Left'])
                time_left = f"{metrics['battery_time_left']//60:.0f} min" if metrics['battery_time_left'] else 'N/A'
                writer.writerow([
                    f"{metrics['battery_percent']:.0f}",
                    'Yes' if metrics['battery_plugged'] else 'No',
                    time_left
                ])
            
            debug_log(f"Metrics exported to CSV: {filepath}")
            return str(filepath)
        
        except Exception as e:
            debug_log(f"Error exporting to CSV: {e}", "ERROR")
            return None
    
    def get_export_history(self, limit=10):
        """Retourne la liste des fichiers exportés récemment."""
        try:
            files = sorted(
                self.export_dir.glob("taskly_metrics_*"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )
            return [str(f) for f in files[:limit]]
        except Exception as e:
            debug_log(f"Error getting export history: {e}", "ERROR")
            return []
