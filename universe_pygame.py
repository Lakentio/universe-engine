"""Controles
---------
• W/S/A/D … frente/trás/esquerda/direita  
• Q/E … baixa/sobe  
• Mouse … olhar em volta  
• ESC … sair"""

import sys
import math
import hashlib
import random
from pathlib import Path

import pygame

# ────────────────────────────────────────
# Configurações gerais (ajuste conforme hardware)
# ────────────────────────────────────────
WIDTH, HEIGHT = 800, 600
FOV_DEG = 90
CHUNK_SIZE = 32         # Tamanho de um chunk em unidades de mundo
CHUNK_RADIUS = 2         # Quantos chunks carregar ao redor do jogador
STARS_PER_CHUNK = (6, 18)  # min, max
MOVE_SPEED = 10.0        # unidades por segundo
MOUSE_SENS = 0.0025
GLOBAL_SEED = "42‑galactic‑seed"
TARGET_FPS = 60

# ────────────────────────────────────────
# Inicialização Pygame
# ────────────────────────────────────────
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedural Space Explorer (low‑end edition)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 14)

# Atualiza inicialização do mouse
pygame.event.set_grab(False)  # Desativa captura do mouse
pygame.mouse.set_visible(True)  # Torna o cursor visível

# Pré‑cálculo de fator de projeção
SCALE = WIDTH / (2 * math.tan(math.radians(FOV_DEG / 2)))

# ────────────────────────────────────────
# Utilidades de geração procedural
# ────────────────────────────────────────

def coord_seed(*coords: int) -> int:
    """Gera seed determinística de 64 bits a partir de coords + seed global."""
    key = f"{GLOBAL_SEED}:{':'.join(map(str, coords))}".encode()
    return int.from_bytes(hashlib.sha256(key).digest()[:8], "big")

# Cache de chunks → lista de estrelas
# Cada estrela: (x, y, z, tamanho, nome)
stars_cache: dict[tuple[int, int, int], list[tuple[float, float, float, float, str]]] = {}

def generate_star_name(rng: random.Random) -> str:
    """Gera um nome aleatório único para uma estrela."""
    letters = ''.join(rng.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
    numbers = rng.randint(1000, 9999)
    return f"{letters}-{numbers}"

def generate_chunk(cx: int, cy: int, cz: int):
    """Cria estrelas para um chunk dado (coordenadas de chunk, não de mundo)."""
    rng = random.Random(coord_seed(cx, cy, cz))
    n_stars = rng.randint(*STARS_PER_CHUNK)
    stars = []
    for _ in range(n_stars):
        # Posição local dentro do chunk
        lx = rng.uniform(0, CHUNK_SIZE)
        ly = rng.uniform(0, CHUNK_SIZE)
        lz = rng.uniform(0, CHUNK_SIZE)
        size = rng.random() * 1.5 + 0.5  # brilho/tamanho
        name = generate_star_name(rng)  # Nome aleatório único
        # Converte para coordenadas absolutas
        stars.append((cx * CHUNK_SIZE + lx,
                      cy * CHUNK_SIZE + ly,
                      cz * CHUNK_SIZE + lz,
                      size,
                      name))  # Adiciona o nome à estrela
    return stars

last_player_chunk = None  # type: tuple[int, int, int] | None
visible_stars: list[tuple[float, float, float, float, str]] = []

selected_star = None  # Armazena a estrela atualmente selecionada

# ────────────────────────────────────────
# Projeção 3D simples (space‑to‑screen)
# ────────────────────────────────────────

def world_to_screen(px, py, pz, cam_pos, cam_rot):
    """Transforma ponto de mundo em coordenadas 2D de tela (ou None se atrás)."""
    # Translaciona para sistema de coordenadas da câmera
    x, y, z = px - cam_pos[0], py - cam_pos[1], pz - cam_pos[2]

    # Rotação Y (yaw)
    sin_y, cos_y = math.sin(cam_rot[1]), math.cos(cam_rot[1])
    x, z = x * cos_y - z * sin_y, x * sin_y + z * cos_y

    # Rotação X (pitch)
    sin_x, cos_x = math.sin(cam_rot[0]), math.cos(cam_rot[0])
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x

    if z <= 0:  # Atrás da câmera
        return None

    sx = int(WIDTH / 2 + (x / z) * SCALE)
    sy = int(HEIGHT / 2 - (y / z) * SCALE)
    if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
        return (sx, sy)
    return None

# ────────────────────────────────────────
# Funções auxiliares
# ────────────────────────────────────────

def draw_text(text, pos):
    surface = font.render(text, True, (255, 255, 255))
    screen.blit(surface, pos)


def update_visible_stars(cam_pos):
    """Atualiza lista de estrelas se o jogador mudou de chunk."""
    global visible_stars, last_player_chunk
    pcx = math.floor(cam_pos[0] / CHUNK_SIZE)
    pcy = math.floor(cam_pos[1] / CHUNK_SIZE)
    pcz = math.floor(cam_pos[2] / CHUNK_SIZE)
    current_chunk = (pcx, pcy, pcz)
    if current_chunk == last_player_chunk:
        return  # Nada a fazer

    last_player_chunk = current_chunk
    new_visible = []
    for cx in range(pcx - CHUNK_RADIUS, pcx + CHUNK_RADIUS + 1):
        for cy in range(pcy - CHUNK_RADIUS, pcy + CHUNK_RADIUS + 1):
            for cz in range(pcz - CHUNK_RADIUS, pcz + CHUNK_RADIUS + 1):
                key = (cx, cy, cz)
                if key not in stars_cache:
                    stars_cache[key] = generate_chunk(*key)
                new_visible.extend(stars_cache[key])
    visible_stars = new_visible

def draw_cursor():
    """Desenha um cursor visível no centro da tela."""
    mx, my = pygame.mouse.get_pos()
    pygame.draw.circle(screen, (0, 255, 0), (mx, my), 5)

def draw_arrow(pos):
    """Desenha uma seta abaixo da posição especificada, apontando para cima."""
    pygame.draw.line(screen, (255, 0, 0), (pos[0], pos[1] + 10), (pos[0], pos[1] + 20), 2)
    pygame.draw.polygon(screen, (255, 0, 0), [(pos[0], pos[1] + 10), (pos[0] - 5, pos[1] + 15), (pos[0] + 5, pos[1] + 15)])

def draw_star_info(star):
    """Exibe informações da estrela selecionada em uma janela."""
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

def handle_mouse_movement():
    """Controla o movimento da câmera com o mouse."""
    global cam_rot  # Certifica-se de que cam_rot seja acessível
    mx, my = pygame.mouse.get_pos()
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    dx, dy = mx - center_x, my - center_y

    if dx or dy:  # Se o mouse se mover
        cam_rot[1] += dx * MOUSE_SENS
        cam_rot[0] -= dy * MOUSE_SENS  # Inverte o eixo vertical
        cam_rot[0] = max(-math.pi/2 + 0.01, min(math.pi/2 - 0.01, cam_rot[0]))
        pygame.mouse.set_pos(center_x, center_y)  # Reposiciona o mouse no centro

# ────────────────────────────────────────
# Loop principal
# ────────────────────────────────────────

def main():
    global cam_rot  # Certifica-se de que cam_rot seja acessível
    global selected_star  # Adiciona global para acessar a variável corretamente
    cam_pos = [0.0, 0.0, -10.0]
    cam_rot = [0.0, 0.0]  # pitch, yaw

    update_visible_stars(cam_pos)

    while True:
        dt = clock.tick(TARGET_FPS) / 1000.0
        screen.fill((0, 0, 0))

        # ───── Eventos ─────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clique esquerdo
                mx, my = pygame.mouse.get_pos()
                for star in visible_stars:
                    screen_pos = world_to_screen(*star[:3], cam_pos, cam_rot)
                    if screen_pos and math.hypot(mx - screen_pos[0], my - screen_pos[1]) < 10:
                        selected_star = star
                        break

        # ───── Input teclado ─────
        keys = pygame.key.get_pressed()
        forward = keys[pygame.K_w] - keys[pygame.K_s]
        strafe = keys[pygame.K_d] - keys[pygame.K_a]
        vertical = keys[pygame.K_e] - keys[pygame.K_q]

        # Vetor de movimento na direção da view (apenas yaw)
        sin_y, cos_y = math.sin(cam_rot[1]), math.cos(cam_rot[1])
        cam_pos[0] += (strafe * cos_y + forward * sin_y) * MOVE_SPEED * dt
        cam_pos[2] += (forward * cos_y - strafe * sin_y) * MOVE_SPEED * dt
        cam_pos[1] += vertical * MOVE_SPEED * dt

        # ───── Input mouse ─────
        handle_mouse_movement()

        # ───── Atualiza estrelas visíveis ─────
        update_visible_stars(cam_pos)

        # ───── Renderiza estrelas ─────
        for sx, sy, sz, size, name in visible_stars:
            screen_pos = world_to_screen(sx, sy, sz, cam_pos, cam_rot)
            if screen_pos:
                pygame.draw.circle(screen, (255, 255, 255), screen_pos, max(1, int(size)))
                if selected_star and (sx, sy, sz, size, name) == selected_star:
                    draw_arrow(screen_pos)

        # Desenha o cursor visível
        draw_cursor()

        # Exibe informações da estrela selecionada
        if selected_star:
            draw_star_info(selected_star)

        # HUD mínimo
        draw_text(f"Pos: {cam_pos[0]:.1f}, {cam_pos[1]:.1f}, {cam_pos[2]:.1f}", (10, 10))
        draw_text(f"FPS: {clock.get_fps():.1f}", (10, 28))

        pygame.display.flip()

if __name__ == "__main__":
    main()
