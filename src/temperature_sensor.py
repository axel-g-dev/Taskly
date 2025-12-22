"""
Module de gestion des capteurs de température multi-plateforme.
Supporte psutil (Linux/Windows) et osx-cpu-temp (macOS).
"""
import subprocess
import platform
import psutil
from utils import debug_log, verbose_log


class TemperatureSensor:
    """Classe abstraite pour la lecture de température CPU."""
    
    def __init__(self):
        self.platform = platform.system()
        self.sensor_type = self._detect_sensor_type()
        debug_log(f"Temperature sensor initialized: {self.sensor_type} on {self.platform}")
    
    def _detect_sensor_type(self):
        """Détecte le type de capteur disponible."""
        # Essayer psutil d'abord (Linux/Windows)
        try:
            temps = psutil.sensors_temperatures()
            if temps and len(temps) > 0:
                return "psutil"
        except (AttributeError, OSError):
            pass
        
        # Sur macOS, essayer osx-cpu-temp
        if self.platform == "Darwin":  # macOS
            if self._check_osx_cpu_temp():
                return "osx-cpu-temp"
        
        return "none"
    
    def _check_osx_cpu_temp(self):
        """Vérifie si osx-cpu-temp est installé."""
        try:
            result = subprocess.run(
                ['which', 'osx-cpu-temp'],
                capture_output=True,
                text=True,
                timeout=2
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def is_available(self):
        """Retourne True si un capteur de température est disponible."""
        return self.sensor_type != "none"
    
    def get_temperature(self):
        """Récupère la température CPU actuelle."""
        if self.sensor_type == "psutil":
            return self._get_temp_psutil()
        elif self.sensor_type == "osx-cpu-temp":
            return self._get_temp_osx()
        return None
    
    def _get_temp_psutil(self):
        """Récupère la température via psutil (Linux/Windows)."""
        try:
            temps = psutil.sensors_temperatures()
            if not temps:
                return None
            
            # Priority order: coretemp (Linux), k10temp (AMD), CPU Thermal
            priority_sensors = ['coretemp', 'k10temp', 'cpu_thermal', 'cpu-thermal']
            
            # Try priority sensors first
            for sensor_name in priority_sensors:
                if sensor_name in temps and temps[sensor_name]:
                    temp = temps[sensor_name][0].current
                    verbose_log(f"CPU Temp ({sensor_name}): {temp:.0f}°C")
                    return temp
            
            # Fallback: use first available sensor
            for name, entries in temps.items():
                if entries and entries[0].current > 0:
                    temp = entries[0].current
                    verbose_log(f"CPU Temp ({name}): {temp:.0f}°C")
                    return temp
            
            return None
        except Exception as e:
            verbose_log(f"Error reading psutil temperature: {e}")
            return None
    
    def _get_temp_osx(self):
        """
        Récupère la température CPU via osx-cpu-temp (macOS).
        
        Note: osx-cpu-temp lit la température du package CPU (capteur TC0P), qui représente
        la température moyenne globale du processeur. Cette valeur est plus stable et 
        représentative de la charge globale que les températures individuelles des cœurs
        (TC0D, TC1D, etc.) qui peuvent être plus élevées mais plus variables.
        
        La température du package est celle utilisée par la plupart des outils de monitoring
        standard et est recommandée pour un suivi général de la santé du système.
        """
        try:
            result = subprocess.run(
                ['osx-cpu-temp', '-c'],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.returncode == 0:
                # Format de sortie: "61.8°C"
                output = result.stdout.strip()
                # Extraire le nombre de "XX.X°C"
                temp_str = output.replace('°C', '').strip()
                temp = float(temp_str)
                verbose_log(f"CPU Temp (TC0P package): {temp:.0f}°C")
                return temp
            
            return None
        except subprocess.TimeoutExpired:
            debug_log("osx-cpu-temp command timed out", "WARNING")
            return None
        except ValueError as e:
            debug_log(f"Could not parse osx-cpu-temp output: {e}", "WARNING")
            return None
        except Exception as e:
            verbose_log(f"Error reading osx-cpu-temp: {e}")
            return None
    
    def get_sensor_info(self):
        """Retourne des informations sur le capteur utilisé."""
        return {
            'platform': self.platform,
            'sensor_type': self.sensor_type,
            'available': self.is_available()
        }
