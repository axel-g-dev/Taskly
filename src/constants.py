"""
Constantes centralisées pour Taskly.
Toutes les valeurs configurables en un seul endroit.
"""

# ==========================================
# PERFORMANCE & TIMING
# ==========================================
UPDATE_INTERVAL = 1.0           # Secondes entre les mises à jour
HISTORY_SIZE = 30               # Nombre de points d'historique
CACHE_INTERVAL_DISK = 5         # Secondes entre les mises à jour du cache disque
CACHE_INTERVAL_BATTERY = 5      # Secondes entre les mises à jour du cache batterie

# ==========================================
# PROCESS MONITORING
# ==========================================
TOP_PROCESSES_LIMIT = 7         # Nombre de processus à afficher
NORMALIZE_CPU_BY_CORES = True   # Normaliser CPU 0-100% (True) ou afficher total (False)

# ==========================================
# ALERT THRESHOLDS
# ==========================================
ALERT_CPU_THRESHOLD = 90        # Alerte si CPU > 90%
ALERT_RAM_THRESHOLD = 85        # Alerte si RAM > 85%
ALERT_TEMP_THRESHOLD = 80       # Alerte si Température > 80°C
ALERT_COOLDOWN = 30             # Secondes entre alertes similaires

# ==========================================
# UI SETTINGS
# ==========================================
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 850
WINDOW_MIN_WIDTH = 900
WINDOW_MIN_HEIGHT = 700

# Animation
ENABLE_ANIMATIONS = True
ANIMATION_DURATION = 200        # Millisecondes
HOVER_SCALE = 1.02
SHADOW_BLUR = 15

# ==========================================
# EXPORT SETTINGS
# ==========================================
EXPORT_DIRECTORY = "exports"    # Dossier pour les exports

# ==========================================
# INTERNATIONALIZATION
# ==========================================
DEFAULT_LANGUAGE = "fr"         # Langue par défaut (fr/en)
CONFIG_FILE_PATH = "~/.taskly_config.json"  # Fichier de configuration utilisateur

# ==========================================
# DEBUG
# ==========================================
DEBUG = True                    # Active les logs de debug
VERBOSE = True                  # Logs très détaillés
