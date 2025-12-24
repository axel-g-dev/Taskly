"""
Système d'internationalisation pour Taskly.
Support Français/Anglais avec persistance des préférences.
"""
import json
import os
from pathlib import Path
from utils import debug_log
from constants import CONFIG_FILE_PATH


# Dictionnaire de traductions
TRANSLATIONS = {
    "fr": {
        # Header
        "app_title": "Taskly - Moniteur Système",
        "live": "Live",
        
        # Tooltips
        "tooltip_export": "Exporter les données",
        "tooltip_alerts": "Basculer les alertes",
        "tooltip_info": "Basculer les infos système",
        "tooltip_language": "Changer la langue",
        
        # Metric Cards
        "cpu_usage": "Utilisation CPU",
        "memory": "Mémoire",
        "network": "Réseau",
        "cores": "cœurs",
        "kb_s": "KB/s",
        
        # Charts
        "cpu_history": "Historique CPU",
        "ram_history": "Historique RAM",
        "network_history": "Historique Réseau",
        
        # Process List
        "top_processes": "Processus Principaux",
        "process": "Processus",
        "pid": "PID",
        "cpu_percent": "CPU%",
        "ram_percent": "RAM%",
        "sort_by_cpu": "Trier par CPU",
        "sort_by_ram": "Trier par RAM",
        
        # System Info Panel
        "system_info": "Informations Système",
        "uptime": "Uptime",
        "disk": "Disque",
        "battery": "Batterie",
        "charging": "En charge",
        "discharging": "Décharge",
        "full": "Pleine",
        "not_available": "N/A",
        
        # Alerts
        "alert_cpu_high": "⚠️ Alerte CPU : Utilisation élevée",
        "alert_ram_high": "⚠️ Alerte RAM : Mémoire élevée",
        "alert_temp_high": "🔥 Alerte Température : Surchauffe",
        
        # Export
        "export_success": "Données exportées avec succès",
        "export_error": "Erreur lors de l'export",
    },
    "en": {
        # Header
        "app_title": "Taskly - System Monitor",
        "live": "Live",
        
        # Tooltips
        "tooltip_export": "Export Data",
        "tooltip_alerts": "Toggle Alerts",
        "tooltip_info": "Toggle System Info",
        "tooltip_language": "Change Language",
        
        # Metric Cards
        "cpu_usage": "CPU Usage",
        "memory": "Memory",
        "network": "Network",
        "cores": "cores",
        "kb_s": "KB/s",
        
        # Charts
        "cpu_history": "CPU History",
        "ram_history": "RAM History",
        "network_history": "Network History",
        
        # Process List
        "top_processes": "Top Processes",
        "process": "Process",
        "pid": "PID",
        "cpu_percent": "CPU%",
        "ram_percent": "RAM%",
        "sort_by_cpu": "Sort by CPU",
        "sort_by_ram": "Sort by RAM",
        
        # System Info Panel
        "system_info": "System Information",
        "uptime": "Uptime",
        "disk": "Disk",
        "battery": "Battery",
        "charging": "Charging",
        "discharging": "Discharging",
        "full": "Full",
        "not_available": "N/A",
        
        # Alerts
        "alert_cpu_high": "⚠️ CPU Alert: High Usage",
        "alert_ram_high": "⚠️ RAM Alert: High Memory",
        "alert_temp_high": "🔥 Temperature Alert: Overheating",
        
        # Export
        "export_success": "Data exported successfully",
        "export_error": "Error during export",
    }
}


class TranslationManager:
    """Gestionnaire de traductions avec persistance."""
    
    CONFIG_FILE = Path(CONFIG_FILE_PATH).expanduser()
    ALLOWED_LANGUAGES = ['fr', 'en']  # ✅ SÉCURITÉ : Whitelist des langues autorisées
    
    def __init__(self, default_language="fr"):
        """Initialise le gestionnaire de traductions."""
        self.current_language = self._load_language() or default_language
        debug_log(f"Language initialized: {self.current_language}")
    
    def _validate_config(self, config):
        """
        ✅ SÉCURITÉ : Validation stricte de la configuration.
        
        Args:
            config: Configuration chargée depuis JSON
            
        Returns:
            bool: True si valide, False sinon
        """
        # Vérifier que c'est un dictionnaire
        if not isinstance(config, dict):
            debug_log("Config must be a dict", "WARNING")
            return False
        
        # Vérifier que la langue est dans la whitelist
        lang = config.get('language')
        if lang and lang not in self.ALLOWED_LANGUAGES:
            debug_log(f"Invalid language '{lang}', not in whitelist {self.ALLOWED_LANGUAGES}", "WARNING")
            return False
        
        return True
    
    def _load_language(self):
        """Charge la langue sauvegardée depuis le fichier de config avec validation stricte."""
        try:
            if self.CONFIG_FILE.exists():
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                    # ✅ SÉCURITÉ : Valider avant utilisation
                    if not self._validate_config(config):
                        debug_log("Invalid config file, removing it", "WARNING")
                        self.CONFIG_FILE.unlink(missing_ok=True)
                        return None
                    
                    lang = config.get('language')
                    debug_log(f"Loaded language from config: {lang}")
                    return lang
                    
        except json.JSONDecodeError as e:
            # ✅ SÉCURITÉ : Fichier JSON corrompu → supprimer
            debug_log(f"Corrupted JSON config: {e}", "ERROR")
            self.CONFIG_FILE.unlink(missing_ok=True)
            return None
        except Exception as e:
            debug_log(f"Error loading language config: {e}", "WARNING")
            return None
    
    def _save_language(self):
        """Sauvegarde la langue actuelle dans le fichier de config."""
        try:
            # Créer le dossier parent si nécessaire
            self.CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            config = {}
            if self.CONFIG_FILE.exists():
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            
            # ✅ SÉCURITÉ : Valider avant sauvegarde
            if self.current_language not in self.ALLOWED_LANGUAGES:
                debug_log(f"Cannot save invalid language: {self.current_language}", "ERROR")
                return
            
            config['language'] = self.current_language
            
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            
            debug_log(f"Saved language to config: {self.current_language}")
        except Exception as e:
            debug_log(f"Error saving language config: {e}", "ERROR")
    
    def t(self, key):
        """
        Récupère la traduction pour une clé donnée.
        
        Args:
            key: Clé de traduction
            
        Returns:
            Texte traduit ou la clé si non trouvée
        """
        translation = TRANSLATIONS.get(self.current_language, {}).get(key, key)
        if translation == key:
            debug_log(f"Translation key not found: {key}", "WARNING")
        return translation
    
    def set_language(self, language):
        """
        Change la langue active.
        
        Args:
            language: Code de langue ('fr' ou 'en')
        """
        if language in TRANSLATIONS:
            self.current_language = language
            self._save_language()
            debug_log(f"Language changed to: {language}")
            return True
        else:
            debug_log(f"Invalid language: {language}", "ERROR")
            return False
    
    def toggle_language(self):
        """Bascule entre français et anglais."""
        new_lang = "en" if self.current_language == "fr" else "fr"
        self.set_language(new_lang)
        return new_lang
    
    def get_current_language(self):
        """Retourne la langue actuelle."""
        return self.current_language
    
    def get_language_name(self):
        """Retourne le nom de la langue actuelle."""
        names = {"fr": "Français", "en": "English"}
        return names.get(self.current_language, self.current_language)
