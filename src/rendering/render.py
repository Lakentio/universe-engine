import pygame
import math
import utils.config
from typing import Tuple, List, Optional

# Precomputed values for performance
SCALE_CACHE: Optional[float] = None
WIDTH_HALF = utils.config.WIDTH // 2
HEIGHT_HALF = utils.config.HEIGHT // 2

def get_scale() -> float:
    """Return the projection scale based on current configuration.

    Uses a simple cache to avoid recalculating the tangent each frame.
    """
    global SCALE_CACHE
    if SCALE_CACHE is None:
        SCALE_CACHE = utils.config.WIDTH / (2 * math.tan(math.radians(utils.config.FOV_DEG / 2)))
    return SCALE_CACHE

def world_to_screen(px: float, py: float, pz: float, cam_pos: List[float], cam_rot: List[float]) -> Optional[Tuple[int, int]]:
    """Transform a 3D world point into 2D screen coordinates.

    Returns `None` if the point is behind the camera or outside the screen.
    """
    # Optimized calculations
    x = px - cam_pos[0]
    y = py - cam_pos[1]
    z = pz - cam_pos[2]
    
    # Optimized rotation
    sin_y, cos_y = math.sin(cam_rot[1]), math.cos(cam_rot[1])
    x, z = x * cos_y - z * sin_y, x * sin_y + z * cos_y
    
    sin_x, cos_x = math.sin(cam_rot[0]), math.cos(cam_rot[0])
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x

    if z <= 0:
        return None

    # Optimized projection
    scale = get_scale()
    sx = int(WIDTH_HALF + (x / z) * scale)
    sy = int(HEIGHT_HALF - (y / z) * scale)
    
    # Quick bounds check
    if 0 <= sx < utils.config.WIDTH and 0 <= sy < utils.config.HEIGHT:
        return (sx, sy)
    return None

def create_panel_surface(width: int, height: int, alpha: int = None) -> pygame.Surface:
    """Create and return an RGBA surface (panel) with default color and border.

    `alpha` controls transparency (0-255). When `None`, the default from config is used.
    """
    if alpha is None:
        alpha = utils.config.UI_PANEL_ALPHA
    
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    color = (*utils.config.UI_COLORS['panel'], alpha)
    surface.fill(color)
    
    # Add a subtle border
    pygame.draw.rect(surface, utils.config.UI_COLORS['accent'], surface.get_rect(), 1)
    
    return surface

def draw_gradient_background(screen: pygame.Surface) -> None:
    """Draw the game background.

    Currently uses a solid fill for performance; can be enhanced later.
    """
    screen.fill((0, 0, 0))

def draw_cursor(screen: pygame.Surface) -> None:
    """Draw the cursor at the current mouse position."""
    mx, my = pygame.mouse.get_pos()
    
    # Outer circle
    pygame.draw.circle(screen, utils.config.UI_COLORS['accent'], (mx, my), 8, 2)
    # Inner circle
    pygame.draw.circle(screen, utils.config.UI_COLORS['text'], (mx, my), 3)
    # Center cross
    pygame.draw.line(screen, utils.config.UI_COLORS['accent'], (mx-6, my), (mx+6, my), 1)
    pygame.draw.line(screen, utils.config.UI_COLORS['accent'], (mx, my-6), (mx, my+6), 1)

def draw_arrow(screen: pygame.Surface, pos: Tuple[int, int]) -> None:
    """Draw an arrow pointing at `pos` (screen coordinates)."""
    # Slightly more elaborate arrow
    arrow_color = utils.config.UI_COLORS['warning']
    arrow_size = 8
    
    # Main shaft line
    pygame.draw.line(screen, arrow_color, (pos[0], pos[1] + 10), (pos[0], pos[1] + 20), 2)
    
    # Arrow head
    points = [
        (pos[0], pos[1] + 10),
        (pos[0] - arrow_size, pos[1] + 15),
        (pos[0] + arrow_size, pos[1] + 15)
    ]
    pygame.draw.polygon(screen, arrow_color, points)
    
    # Highlight circle
    pygame.draw.circle(screen, arrow_color, pos, 12, 2)

def draw_star_info(screen: pygame.Surface, star: Tuple[float, float, float, float, str]) -> None:
    """Display detailed information about the selected `star` in a panel.

    `star` is a tuple (x, y, z, size, name).
    """
    panel_width = 280
    panel_height = 160
    
    # Create panel
    panel = create_panel_surface(panel_width, panel_height)
    
    # Fonts
    font_large = pygame.font.SysFont("monospace", 16, bold=True)
    font_normal = pygame.font.SysFont("monospace", 14)
    font_small = pygame.font.SysFont("monospace", 12)
    
    # Title
    title = font_large.render(f"ESTRELA: {star[4]}", True, utils.config.UI_COLORS['accent'])
    panel.blit(title, (15, 15))
    
    # Info lines
    info_lines = [
        f"Posição: ({star[0]:.1f}, {star[1]:.1f}, {star[2]:.1f})",
        f"Tamanho: {star[3]:.2f}",
        f"Tipo: Estrela Classe G",
        f"Distância: {math.sqrt(star[0]**2 + star[1]**2 + star[2]**2):.1f} u.l."
    ]
    
    y_offset = 45
    for i, line in enumerate(info_lines):
        color = utils.config.UI_COLORS['text'] if i < 2 else utils.config.UI_COLORS['text']
        text_surface = font_normal.render(line, True, color)
        panel.blit(text_surface, (15, y_offset + i * 20))
    
    # Status bar
    status_y = y_offset + 80
    pygame.draw.rect(panel, (60, 60, 80), (15, status_y, 250, 8))
    pygame.draw.rect(panel, utils.config.UI_COLORS['success'], (15, status_y, 250, 8), 1)
    
    # Status text
    status_text = font_small.render("SELECIONADA", True, utils.config.UI_COLORS['success'])
    panel.blit(status_text, (15, status_y + 12))
    
    # Position the panel
    screen.blit(panel, (utils.config.WIDTH - panel_width - 20, 20))

def draw_text(screen: pygame.Surface, text: str, pos: Tuple[int, int], color: Tuple[int, int, int] = None, font_size: int = None, bold: bool = False) -> None:
    """Draw `text` on the screen at `pos` with styling options.

    Uses default colors and fonts when not specified.
    """
    if color is None:
        color = utils.config.UI_COLORS['text']
    if font_size is None:
        font_size = utils.config.UI_FONT_SIZE
    
    font = pygame.font.SysFont("monospace", font_size, bold=bold)
    surface = font.render(text, True, color)
    screen.blit(surface, pos)

def draw_hud_panel(screen: pygame.Surface, cam_pos: List[float], fps: float, universe_info: dict, performance_stats: dict) -> None:
    """Draw the main HUD panel with navigation and performance information."""
    panel_width = 320
    panel_height = 200
    
    # Create main panel
    panel = create_panel_surface(panel_width, panel_height)
    
    # Panel title
    title = pygame.font.SysFont("monospace", 16, bold=True).render("UNIVERSE ENGINE", True, utils.config.UI_COLORS['accent'])
    panel.blit(title, (15, 15))
    
    # Navigation information
    nav_y = 45
    draw_text(panel, f"Posição: ({cam_pos[0]:.1f}, {cam_pos[1]:.1f}, {cam_pos[2]:.1f})", (15, nav_y), utils.config.UI_COLORS['text'])
    draw_text(panel, f"Velocidade: {utils.config.MOVE_SPEED:.1f} u.l./s", (15, nav_y + 20), utils.config.UI_COLORS['text'])
    
    # Performance information
    perf_y = nav_y + 50
    draw_text(panel, f"FPS: {fps:.1f}", (15, perf_y), utils.config.UI_COLORS['success'])
    draw_text(panel, f"Estrelas Visíveis: {performance_stats.get('total_stars', 0)}", (15, perf_y + 20), utils.config.UI_COLORS['text'])
    draw_text(panel, f"Chunks Carregados: {performance_stats.get('cache_size', 0)}", (15, perf_y + 40), utils.config.UI_COLORS['text'])
    
    # Seed information
    seed_y = perf_y + 70
    seed_text = f"Seed: {universe_info['seed'][:25]}{'...' if len(universe_info['seed']) > 25 else ''}"
    draw_text(panel, seed_text, (15, seed_y), utils.config.UI_COLORS['text'])
    
    if universe_info['is_custom']:
        draw_text(panel, "✓ Seed Personalizada", (15, seed_y + 20), utils.config.UI_COLORS['success'])
    
    # System status bar
    status_y = seed_y + 50
    pygame.draw.rect(panel, (60, 60, 80), (15, status_y, 290, 6))
    pygame.draw.rect(panel, utils.config.UI_COLORS['success'], (15, status_y, 290, 6), 1)
    
    # Position the panel
    screen.blit(panel, (20, 20))

def draw_minimap(screen: pygame.Surface, cam_pos: List[float], visible_stars: List[Tuple], selected_star: Optional[Tuple] = None) -> None:
    """Draw a minimap showing nearby stars relative to the camera.

    `visible_stars` is a list of star tuples (x,y,z,size,name).
    """
    map_size = 150
    map_x = utils.config.WIDTH - map_size - 20
    map_y = utils.config.HEIGHT - map_size - 20
    
    # Create minimap panel
    panel = create_panel_surface(map_size, map_size)
    
    # Title
    title = pygame.font.SysFont("monospace", 12, bold=True).render("MINIMAPA", True, utils.config.UI_COLORS['accent'])
    panel.blit(title, (10, 10))
    
    # Draw stars on the minimap
    map_center = map_size // 2
    scale = map_size / 200  # Minimap scale
    
    for star in visible_stars[:50]:  # Limit to 50 stars on the minimap
        # Calculate position relative to the camera
        rel_x = (star[0] - cam_pos[0]) * scale
        rel_z = (star[2] - cam_pos[2]) * scale
        
        # Convert to minimap coordinates
        map_pos_x = int(map_center + rel_x)
        map_pos_y = int(map_center + rel_z)
        
        # Check if inside the minimap area
        if 20 <= map_pos_x < map_size - 20 and 30 <= map_pos_y < map_size - 20:
            color = utils.config.UI_COLORS['warning'] if star == selected_star else utils.config.UI_COLORS['text']
            size = 3 if star == selected_star else 1
            pygame.draw.circle(panel, color, (map_pos_x, map_pos_y), size)
    
    # Draw camera position (center)
    pygame.draw.circle(panel, utils.config.UI_COLORS['accent'], (map_center, map_center), 4, 2)
    
    # Position the minimap
    screen.blit(panel, (map_x, map_y))

def draw_controls_help(screen: pygame.Surface) -> None:
    """Show a panel with the game controls.

    Useful for new contributors or quick testing of the interface.
    """
    panel_width = 250
    panel_height = 120
    
    panel = create_panel_surface(panel_width, panel_height)
    
    title = pygame.font.SysFont("monospace", 14, bold=True).render("CONTROLS", True, utils.config.UI_COLORS['accent'])
    panel.blit(title, (15, 15))
    
    controls = [
        "WASD - Moviment",
        "QE - Vertical",
        "Mouse - Rotation",
        "Clique - Select",
        "ESC - Quit"
    ]
    
    for i, control in enumerate(controls):
        draw_text(panel, control, (15, 40 + i * 15), utils.config.UI_COLORS['text'], 12)
    
    screen.blit(panel, (20, utils.config.HEIGHT - panel_height - 20))
