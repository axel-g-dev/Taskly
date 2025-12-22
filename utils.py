"""
Fonctions utilitaires pour Taskly.
"""
from datetime import datetime
from config import DEBUG, VERBOSE


# ==========================================
# LOGGING FUNCTIONS
# ==========================================
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
# HELPER FUNCTIONS
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
