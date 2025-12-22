"""
Configuration et thème de l'application Taskly.
"""

# ==========================================
# DEBUG FLAGS
# ==========================================
DEBUG = True  # Active les logs de debug
VERBOSE = True  # Logs très détaillés


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
# ALERT THRESHOLDS
# ==========================================
ALERT_THRESHOLDS = {
    'cpu': 90,      # Alert if CPU > 90%
    'ram': 85,      # Alert if RAM > 85%
    'temp': 80,     # Alert if Temp > 80°C
}


# ==========================================
# PERFORMANCE SETTINGS
# ==========================================
UPDATE_INTERVAL = 1.0       # seconds between updates
HISTORY_SIZE = 30           # number of data points to keep
CACHE_INTERVAL = 5          # seconds between disk/battery cache updates


# ==========================================
# UI ANIMATION SETTINGS
# ==========================================
ENABLE_ANIMATIONS = True    # Enable/disable animations
ANIMATION_DURATION = 200    # Animation duration (ms) - short for performance
HOVER_SCALE = 1.02          # Scale on hover (subtle)
SHADOW_BLUR = 15            # Shadow blur radius
