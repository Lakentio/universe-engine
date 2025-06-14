import pygame
import math
from config import WIDTH, HEIGHT, FOV_DEG

SCALE = WIDTH / (2 * math.tan(math.radians(FOV_DEG / 2)))

def world_to_screen(px, py, pz, cam_pos, cam_rot):
    """Transforma ponto de mundo em coordenadas 2D de tela."""
    x, y, z = px - cam_pos[0], py - cam_pos[1], pz - cam_pos[2]
    sin_y, cos_y = math.sin(cam_rot[1]), math.cos(cam_rot[1])
    x, z = x * cos_y - z * sin_y, x * sin_y + z * cos_y
    sin_x, cos_x = math.sin(cam_rot[0]), math.cos(cam_rot[0])
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x

    if z <= 0:
        return None

    sx = int(WIDTH / 2 + (x / z) * SCALE)
    sy = int(HEIGHT / 2 - (y / z) * SCALE)
    if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
        return (sx, sy)
    return None

def draw_cursor(screen):
    """Desenha um cursor visível no centro da tela."""
    mx, my = pygame.mouse.get_pos()
    pygame.draw.circle(screen, (0, 255, 0), (mx, my), 5)

def draw_arrow(screen, pos):
    """Desenha uma seta abaixo da posição especificada."""
    pygame.draw.line(screen, (255, 0, 0), (pos[0], pos[1] + 10), (pos[0], pos[1] + 20), 2)
    pygame.draw.polygon(screen, (255, 0, 0), [(pos[0], pos[1] + 10), (pos[0] - 5, pos[1] + 15), (pos[0] + 5, pos[1] + 15)])

def draw_star_info(screen, star):
    """Exibe informações da estrela selecionada."""
    info_surface = pygame.Surface((200, 120))
    info_surface.fill((30, 30, 30))
    pygame.draw.rect(info_surface, (255, 255, 255), info_surface.get_rect(), 1)
    font = pygame.font.SysFont("monospace", 14)
    lines = [
        f"Nome: {star[4]}",
        f"Pos: {star[0]:.1f}, {star[1]:.1f}, {star[2]:.1f}",
        f"Tamanho: {star[3]:.2f}"
    ]
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, (255, 255, 255))
        info_surface.blit(text_surface, (10, 10 + i * 20))
    screen.blit(info_surface, (WIDTH - 210, 10))

def draw_text(screen, text, pos):
    """Desenha texto na tela."""
    surface = pygame.font.SysFont("monospace", 14).render(text, True, (255, 255, 255))
    screen.blit(surface, pos)
