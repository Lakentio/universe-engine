WIDTH, HEIGHT = 800, 600
FOV_DEG = 90
CHUNK_SIZE = 32
CHUNK_RADIUS = 1
STARS_PER_CHUNK = (2, 5)
MOVE_SPEED = 10.0
MOUSE_SENS = 0.0025
GLOBAL_SEED = "42-galactic-seed"  # Seed padrão - pode ser alterada pelo usuário
TARGET_FPS = 60

# Configuração para seeds personalizadas
USE_CUSTOM_SEED = False  # Define se deve usar seed personalizada
CUSTOM_SEED = "meu-universo-123"  # Seed personalizada do usuário

# Configurações de Performance (ULTRA-OTIMIZADAS)
FRUSTUM_CULLING = False  # Desabilitado para performance
MAX_VISIBLE_STARS = 100  # Reduzido ainda mais
LOD_DISTANCE = 500.0  # Alto para não limitar
STAR_FADE_DISTANCE = 200.0  # Alto para não limitar

# Configurações de UI/HUD (MANTIDAS)
UI_SCALE = 1.0  # Escala da interface
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
