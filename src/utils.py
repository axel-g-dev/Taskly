"""
Fonctions utilitaires pour Taskly.
"""
import logging
from datetime import datetime
from config import DEBUG, VERBOSE


# ==========================================
# LOGGING SYSTEM
# ==========================================
def setup_logger(name="taskly"):
    """Configure et retourne un logger optimisé."""
    logger = logging.getLogger(name)
    
    # Configurer le niveau en fonction de DEBUG/VERBOSE
    if VERBOSE:
        logger.setLevel(logging.DEBUG)
    elif DEBUG:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)
    
    # Éviter les handlers dupliqués
    if not logger.handlers:
        # Handler console avec format personnalisé
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s',
            datefmt='%H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


# Logger global
logger = setup_logger()


# ==========================================
# BACKWARD COMPATIBILITY
# ==========================================
def debug_log(message, level="INFO"):
    """
    Fonction de compatibilité pour l'ancien système.
    DEPRECATED: Utiliser logger.info(), logger.debug(), etc.
    """
    level_map = {
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "VERBOSE": logging.DEBUG
    }
    logger.log(level_map.get(level, logging.INFO), message)


def verbose_log(message):
    """
    Fonction de compatibilité.
    DEPRECATED: Utiliser logger.debug()
    """
    logger.debug(message)


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
