import pygame
import math
import hashlib
import random
from config import WIDTH, HEIGHT, GLOBAL_SEED, CHUNK_SIZE, CHUNK_RADIUS, STARS_PER_CHUNK, MOUSE_SENS

stars_cache = {}

def initialize_pygame():
    """Inicializa o Pygame e retorna a tela e o relógio."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Procedural Space Explorer (low‑end edition)")
    clock = pygame.time.Clock()
    return screen, clock

def coord_seed(*coords: int) -> int:
    """Gera seed determinística de 64 bits a partir de coords + seed global."""
    key = f"{GLOBAL_SEED}:{':'.join(map(str, coords))}".encode()
    return int.from_bytes(hashlib.sha256(key).digest()[:8], "big")

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
        lx = rng.uniform(0, CHUNK_SIZE)
        ly = rng.uniform(0, CHUNK_SIZE)
        lz = rng.uniform(0, CHUNK_SIZE)
        size = rng.random() * 1.5 + 0.5
        name = generate_star_name(rng)
        stars.append((cx * CHUNK_SIZE + lx, cy * CHUNK_SIZE + ly, cz * CHUNK_SIZE + lz, size, name))
    return stars

def update_visible_stars(cam_pos):
    """Atualiza lista de estrelas visíveis com base na posição da câmera."""
    pcx = math.floor(cam_pos[0] / CHUNK_SIZE)
    pcy = math.floor(cam_pos[1] / CHUNK_SIZE)
    pcz = math.floor(cam_pos[2] / CHUNK_SIZE)
    visible_stars = []
    for cx in range(pcx - CHUNK_RADIUS, pcx + CHUNK_RADIUS + 1):
        for cy in range(pcy - CHUNK_RADIUS, pcy + CHUNK_RADIUS + 1):
            for cz in range(pcz - CHUNK_RADIUS, pcz + CHUNK_RADIUS + 1):
                key = (cx, cy, cz)
                if key not in stars_cache:
                    stars_cache[key] = generate_chunk(cx, cy, cz)
                visible_stars.extend(stars_cache[key])
    return visible_stars

def handle_mouse_movement(cam_rot):
    """Controla o movimento da câmera com o mouse."""
    mx, my = pygame.mouse.get_pos()
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    dx, dy = mx - center_x, my - center_y

    if dx or dy:
        cam_rot[1] += dx * MOUSE_SENS
        cam_rot[0] -= dy * MOUSE_SENS
        cam_rot[0] = max(-math.pi/2 + 0.01, min(math.pi/2 - 0.01, cam_rot[0]))
        pygame.mouse.set_pos(center_x, center_y)
