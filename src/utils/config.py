WIDTH, HEIGHT = 800, 600
FOV_DEG = 90
CHUNK_SIZE = 128
CHUNK_RADIUS = 1
STARS_PER_CHUNK = (10, 30)
MOVE_SPEED = 10.0
MOUSE_SENS = 0.0025
GLOBAL_SEED = "lakentio2"  # Seed padrão - pode ser alterada pelo usuário
TARGET_FPS = 60

# Configuração para seeds personalizadas
USE_CUSTOM_SEED = False # Define se deve usar seed personalizada
CUSTOM_SEED = "Lakentio"  # Seed personalizada do usuário

# Configurações de Performance (ULTRA-OTIMIZADAS)
FRUSTUM_CULLING = False  # Desabilitado para performance
MAX_VISIBLE_STARS = 1000  # Aumentado para depuração (mostrar mais estrelas)
LOD_DISTANCE = 500.0  # Alto para não limitar
STAR_FADE_DISTANCE = 200.0  # Alto para não limitar

# Configurações de UI/HUD (MANTIDAS)
UI_SCALE = 3  # Escala da interface
UI_COLORS = {
    'background': (20, 20, 30),
    'panel': (40, 40, 60),
    'text': (220, 220, 255),
    'accent': (100, 150, 255),
    'warning': (255, 150, 100),
    'success': (100, 255, 150)
}
UI_FONT_SIZE = 14
UI_PANEL_ALPHA = 180  # Transparência dos painéis (0-255)

# Logging / Debug
DEBUG_LOG = True # Habilita logs de depuração para desenvolvimento
LOG_FILE = "universe_debug.log"
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
