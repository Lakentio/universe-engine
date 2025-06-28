import pygame
import math
import utils.config
from typing import Tuple, List, Optional

# Pré-calculado para performance
SCALE_CACHE = None
WIDTH_HALF = utils.config.WIDTH // 2
HEIGHT_HALF = utils.config.HEIGHT // 2

def get_scale():
    """Retorna a escala de projeção baseada nas configurações atuais."""
    global SCALE_CACHE
    if SCALE_CACHE is None:
        SCALE_CACHE = utils.config.WIDTH / (2 * math.tan(math.radians(utils.config.FOV_DEG / 2)))
    return SCALE_CACHE

def world_to_screen(px, py, pz, cam_pos, cam_rot):
    """Transforma ponto de mundo em coordenadas 2D de tela - VERSÃO OTIMIZADA."""
    # Cálculos otimizados
    x = px - cam_pos[0]
    y = py - cam_pos[1]
    z = pz - cam_pos[2]
    
    # Rotação otimizada
    sin_y, cos_y = math.sin(cam_rot[1]), math.cos(cam_rot[1])
    x, z = x * cos_y - z * sin_y, x * sin_y + z * cos_y
    
    sin_x, cos_x = math.sin(cam_rot[0]), math.cos(cam_rot[0])
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x

    if z <= 0:
        return None

    # Projeção otimizada
    scale = get_scale()
    sx = int(WIDTH_HALF + (x / z) * scale)
    sy = int(HEIGHT_HALF - (y / z) * scale)
    
    # Verificação rápida de bounds
    if 0 <= sx < utils.config.WIDTH and 0 <= sy < utils.config.HEIGHT:
        return (sx, sy)
    return None

def create_panel_surface(width: int, height: int, alpha: int = None) -> pygame.Surface:
    """Cria uma superfície de painel com transparência."""
    if alpha is None:
        alpha = utils.config.UI_PANEL_ALPHA
    
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    color = (*utils.config.UI_COLORS['panel'], alpha)
    surface.fill(color)
    
    # Adiciona borda sutil
    pygame.draw.rect(surface, utils.config.UI_COLORS['accent'], surface.get_rect(), 1)
    
    return surface

def draw_gradient_background(screen):
    """Desenha um fundo simples preto para máxima performance."""
    screen.fill((0, 0, 0))

def draw_cursor(screen):
    """Desenha um cursor visível no centro da tela."""
    mx, my = pygame.mouse.get_pos()
    
    # Círculo externo
    pygame.draw.circle(screen, utils.config.UI_COLORS['accent'], (mx, my), 8, 2)
    # Círculo interno
    pygame.draw.circle(screen, utils.config.UI_COLORS['text'], (mx, my), 3)
    # Cruz central
    pygame.draw.line(screen, utils.config.UI_COLORS['accent'], (mx-6, my), (mx+6, my), 1)
    pygame.draw.line(screen, utils.config.UI_COLORS['accent'], (mx, my-6), (mx, my+6), 1)

def draw_arrow(screen, pos):
    """Desenha uma seta abaixo da posição especificada."""
    # Seta mais elaborada
    arrow_color = utils.config.UI_COLORS['warning']
    arrow_size = 8
    
    # Linha principal
    pygame.draw.line(screen, arrow_color, (pos[0], pos[1] + 10), (pos[0], pos[1] + 20), 2)
    
    # Ponta da seta
    points = [
        (pos[0], pos[1] + 10),
        (pos[0] - arrow_size, pos[1] + 15),
        (pos[0] + arrow_size, pos[1] + 15)
    ]
    pygame.draw.polygon(screen, arrow_color, points)
    
    # Círculo de destaque
    pygame.draw.circle(screen, arrow_color, pos, 12, 2)

def draw_star_info(screen, star):
    """Exibe informações da estrela selecionada em um painel moderno."""
    panel_width = 280
    panel_height = 160
    
    # Cria painel
    panel = create_panel_surface(panel_width, panel_height)
    
    # Fonte
    font_large = pygame.font.SysFont("monospace", 16, bold=True)
    font_normal = pygame.font.SysFont("monospace", 14)
    font_small = pygame.font.SysFont("monospace", 12)
    
    # Título
    title = font_large.render(f"ESTRELA: {star[4]}", True, utils.config.UI_COLORS['accent'])
    panel.blit(title, (15, 15))
    
    # Informações
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
    
    # Barra de status
    status_y = y_offset + 80
    pygame.draw.rect(panel, (60, 60, 80), (15, status_y, 250, 8))
    pygame.draw.rect(panel, utils.config.UI_COLORS['success'], (15, status_y, 250, 8), 1)
    
    # Status text
    status_text = font_small.render("SELECIONADA", True, utils.config.UI_COLORS['success'])
    panel.blit(status_text, (15, status_y + 12))
    
    # Posiciona o painel
    screen.blit(panel, (utils.config.WIDTH - panel_width - 20, 20))

def draw_text(screen, text, pos, color=None, font_size=None, bold=False):
    """Desenha texto na tela com opções avançadas."""
    if color is None:
        color = utils.config.UI_COLORS['text']
    if font_size is None:
        font_size = utils.config.UI_FONT_SIZE
    
    font = pygame.font.SysFont("monospace", font_size, bold=bold)
    surface = font.render(text, True, color)
    screen.blit(surface, pos)

def draw_hud_panel(screen, cam_pos, fps, universe_info, performance_stats):
    """Desenha o painel principal do HUD."""
    panel_width = 320
    panel_height = 200
    
    # Cria painel principal
    panel = create_panel_surface(panel_width, panel_height)
    
    # Título do painel
    title = pygame.font.SysFont("monospace", 16, bold=True).render("UNIVERSE ENGINE", True, utils.config.UI_COLORS['accent'])
    panel.blit(title, (15, 15))
    
    # Informações de navegação
    nav_y = 45
    draw_text(panel, f"Posição: ({cam_pos[0]:.1f}, {cam_pos[1]:.1f}, {cam_pos[2]:.1f})", (15, nav_y), utils.config.UI_COLORS['text'])
    draw_text(panel, f"Velocidade: {utils.config.MOVE_SPEED:.1f} u.l./s", (15, nav_y + 20), utils.config.UI_COLORS['text'])
    
    # Informações de performance
    perf_y = nav_y + 50
    draw_text(panel, f"FPS: {fps:.1f}", (15, perf_y), utils.config.UI_COLORS['success'])
    draw_text(panel, f"Estrelas Visíveis: {performance_stats.get('total_stars', 0)}", (15, perf_y + 20), utils.config.UI_COLORS['text'])
    draw_text(panel, f"Chunks Carregados: {performance_stats.get('cache_size', 0)}", (15, perf_y + 40), utils.config.UI_COLORS['text'])
    
    # Informações da seed
    seed_y = perf_y + 70
    seed_text = f"Seed: {universe_info['seed'][:25]}{'...' if len(universe_info['seed']) > 25 else ''}"
    draw_text(panel, seed_text, (15, seed_y), utils.config.UI_COLORS['text'])
    
    if universe_info['is_custom']:
        draw_text(panel, "✓ Seed Personalizada", (15, seed_y + 20), utils.config.UI_COLORS['success'])
    
    # Barra de status do sistema
    status_y = seed_y + 50
    pygame.draw.rect(panel, (60, 60, 80), (15, status_y, 290, 6))
    pygame.draw.rect(panel, utils.config.UI_COLORS['success'], (15, status_y, 290, 6), 1)
    
    # Posiciona o painel
    screen.blit(panel, (20, 20))

def draw_minimap(screen, cam_pos, visible_stars, selected_star=None):
    """Desenha um minimapa das estrelas próximas."""
    map_size = 150
    map_x = utils.config.WIDTH - map_size - 20
    map_y = utils.config.HEIGHT - map_size - 20
    
    # Cria painel do minimapa
    panel = create_panel_surface(map_size, map_size)
    
    # Título
    title = pygame.font.SysFont("monospace", 12, bold=True).render("MINIMAPA", True, utils.config.UI_COLORS['accent'])
    panel.blit(title, (10, 10))
    
    # Desenha estrelas no minimapa
    map_center = map_size // 2
    scale = map_size / 200  # Escala do minimapa
    
    for star in visible_stars[:50]:  # Limita a 50 estrelas no minimapa
        # Calcula posição relativa à câmera
        rel_x = (star[0] - cam_pos[0]) * scale
        rel_z = (star[2] - cam_pos[2]) * scale
        
        # Converte para coordenadas do minimapa
        map_pos_x = int(map_center + rel_x)
        map_pos_y = int(map_center + rel_z)
        
        # Verifica se está dentro do minimapa
        if 20 <= map_pos_x < map_size - 20 and 30 <= map_pos_y < map_size - 20:
            color = utils.config.UI_COLORS['warning'] if star == selected_star else utils.config.UI_COLORS['text']
            size = 3 if star == selected_star else 1
            pygame.draw.circle(panel, color, (map_pos_x, map_pos_y), size)
    
    # Desenha a posição da câmera (centro)
    pygame.draw.circle(panel, utils.config.UI_COLORS['accent'], (map_center, map_center), 4, 2)
    
    # Posiciona o minimapa
    screen.blit(panel, (map_x, map_y))

def draw_controls_help(screen):
    """Desenha ajuda dos controles."""
    panel_width = 250
    panel_height = 120
    
    panel = create_panel_surface(panel_width, panel_height)
    
    title = pygame.font.SysFont("monospace", 14, bold=True).render("CONTROLES", True, utils.config.UI_COLORS['accent'])
    panel.blit(title, (15, 15))
    
    controls = [
        "WASD - Movimento",
        "QE - Vertical",
        "Mouse - Rotação",
        "Clique - Selecionar",
        "ESC - Sair"
    ]
    
    for i, control in enumerate(controls):
        draw_text(panel, control, (15, 40 + i * 15), utils.config.UI_COLORS['text'], 12)
    
    screen.blit(panel, (20, utils.config.HEIGHT - panel_height - 20))
