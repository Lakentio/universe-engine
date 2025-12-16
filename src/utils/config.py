WIDTH, HEIGHT = 800, 600
FOV_DEG = 90
CHUNK_SIZE = 128
CHUNK_RADIUS = 1
STARS_PER_CHUNK = (10, 30)
MOVE_SPEED = 50.0
MOUSE_SENS = 0.0025
GLOBAL_SEED = "lakentio2"  # Default seed - can be changed by user
TARGET_FPS = 1000

# Configuration for custom seeds
USE_CUSTOM_SEED = False  # Whether to use a custom seed
CUSTOM_SEED = "Lakentio"  # User-provided custom seed

# Performance settings (tweaks for development/debug)
FRUSTUM_CULLING = False  # Disabled for performance
MAX_VISIBLE_STARS = 1000  # Increased for debugging (show more stars)
LOD_DISTANCE = 500.0  # High to not limit
STAR_FADE_DISTANCE = 200.0  # High to not limit

# UI/HUD settings (kept as-is)
UI_SCALE = 3  # Interface scale
UI_COLORS = {
    'background': (20, 20, 30),
    'panel': (40, 40, 60),
    'text': (220, 220, 255),
    'accent': (100, 150, 255),
    'warning': (255, 150, 100),
    'success': (100, 255, 150)
}
UI_FONT_SIZE = 24
UI_PANEL_ALPHA = 180  # Panel transparency (0-255)

# Logging / Debug
DEBUG_LOG = True # Activate logs for depuration
LOG_FILE = "universe_debug.log"
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
