"""
Configuration et thème de l'application Taskly.
"""
from constants import (
    DEBUG, VERBOSE, UPDATE_INTERVAL, HISTORY_SIZE,
    ALERT_CPU_THRESHOLD, ALERT_RAM_THRESHOLD, ALERT_TEMP_THRESHOLD,
    ENABLE_ANIMATIONS, ANIMATION_DURATION, HOVER_SCALE, SHADOW_BLUR,
    DEFAULT_LANGUAGE
)


# ==========================================
# DESIGN SYSTEM & CONSTANTS
# ==========================================
class AppleTheme:
    """Thème Apple-style pour l'interface."""
    
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
# ALERT THRESHOLDS (importés de constants)
# ==========================================
ALERT_THRESHOLDS = {
    'cpu': ALERT_CPU_THRESHOLD,
    'ram': ALERT_RAM_THRESHOLD,
    'temp': ALERT_TEMP_THRESHOLD,
}


# Note: Les autres constantes sont maintenant dans constants.py
# - UPDATE_INTERVAL
# - HISTORY_SIZE
# - CACHE_INTERVAL
# - ENABLE_ANIMATIONS
# - ANIMATION_DURATION
# - HOVER_SCALE
# - SHADOW_BLUR
# - DEFAULT_LANGUAGE

