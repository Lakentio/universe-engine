import pygame
import math
import hashlib
import random
import utils.config
from typing import List, Tuple, Optional

stars_cache = {}

def get_active_seed():
    """Retorna a seed ativa baseada na configuração."""
    if utils.config.USE_CUSTOM_SEED:
        return utils.config.CUSTOM_SEED
    return utils.config.GLOBAL_SEED

def coord_seed(*coords: int) -> int:
    """Gera seed determinística de 64 bits a partir de coords + seed global."""
    active_seed = get_active_seed()
    # Cria uma string única e consistente
    coord_string = f"{active_seed}:{':'.join(map(str, coords))}"
    # Usa UTF-8 para garantir consistência na codificação
    key_bytes = coord_string.encode('utf-8')
    # Gera hash SHA-256 completo
    hash_bytes = hashlib.sha256(key_bytes).digest()
    # Converte para inteiro de 64 bits usando os primeiros 8 bytes
    return int.from_bytes(hash_bytes[:8], byteorder='big', signed=False)

def initialize_pygame():
    """Inicializa o Pygame e retorna a tela e o relógio."""
    pygame.init()
    screen = pygame.display.set_mode((utils.config.WIDTH, utils.config.HEIGHT))
    pygame.display.set_caption("Universe Engine - Procedural Space Explorer")
    clock = pygame.time.Clock()
    return screen, clock

def generate_star_name(rng: random.Random) -> str:
    """Gera um nome aleatório único para uma estrela."""
    letters = ''.join(rng.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
    numbers = rng.randint(1000, 9999)
    return f"{letters}-{numbers}"

def generate_chunk(cx: int, cy: int, cz: int):
    """Cria estrelas para um chunk dado (coordenadas de chunk, não de mundo)."""
    rng = random.Random(coord_seed(cx, cy, cz))
    n_stars = rng.randint(*utils.config.STARS_PER_CHUNK)
    stars = []
    for _ in range(n_stars):
        lx = rng.uniform(0, utils.config.CHUNK_SIZE)
        ly = rng.uniform(0, utils.config.CHUNK_SIZE)
        lz = rng.uniform(0, utils.config.CHUNK_SIZE)
        size = rng.random() * 1.5 + 0.5
        name = generate_star_name(rng)
        stars.append((cx * utils.config.CHUNK_SIZE + lx, cy * utils.config.CHUNK_SIZE + ly, cz * utils.config.CHUNK_SIZE + lz, size, name))
    return stars

def update_visible_stars(cam_pos: List[float], cam_rot: List[float] = None) -> List[Tuple]:
    """Atualiza lista de estrelas visíveis - VERSÃO OTIMIZADA."""
    pcx = math.floor(cam_pos[0] / utils.config.CHUNK_SIZE)
    pcy = math.floor(cam_pos[1] / utils.config.CHUNK_SIZE)
    pcz = math.floor(cam_pos[2] / utils.config.CHUNK_SIZE)
    
    visible_stars = []
    chunks_loaded = 0
    
    # Loop simples e direto
    for cx in range(pcx - utils.config.CHUNK_RADIUS, pcx + utils.config.CHUNK_RADIUS + 1):
        for cy in range(pcy - utils.config.CHUNK_RADIUS, pcy + utils.config.CHUNK_RADIUS + 1):
            for cz in range(pcz - utils.config.CHUNK_RADIUS, pcz + utils.config.CHUNK_RADIUS + 1):
                key = (cx, cy, cz)
                if key not in stars_cache:
                    stars_cache[key] = generate_chunk(cx, cy, cz)
                    chunks_loaded += 1
                
                # Adiciona todas as estrelas do chunk
                visible_stars.extend(stars_cache[key])
    
    # Limite simples de estrelas
    if len(visible_stars) > utils.config.MAX_VISIBLE_STARS:
        visible_stars = visible_stars[:utils.config.MAX_VISIBLE_STARS]
    
    return visible_stars, chunks_loaded

def handle_mouse_movement(cam_rot):
    """Controla o movimento da câmera com o mouse."""
    mx, my = pygame.mouse.get_pos()
    center_x, center_y = utils.config.WIDTH // 2, utils.config.HEIGHT // 2
    dx, dy = mx - center_x, my - center_y

    if dx or dy:
        cam_rot[1] += dx * utils.config.MOUSE_SENS
        cam_rot[0] -= dy * utils.config.MOUSE_SENS
        cam_rot[0] = max(-math.pi/2 + 0.01, min(math.pi/2 - 0.01, cam_rot[0]))
        pygame.mouse.set_pos(center_x, center_y)

def clear_stars_cache():
    """Limpa o cache de estrelas para regenerar o universo."""
    global stars_cache
    stars_cache.clear()

def set_universe_seed(new_seed: str):
    """Define uma nova seed para o universo e limpa o cache."""
    global stars_cache
    stars_cache.clear()
    # Atualiza a configuração
    utils.config.USE_CUSTOM_SEED = True
    utils.config.CUSTOM_SEED = new_seed

def get_universe_info():
    """Retorna informações sobre a seed atual do universo."""
    active_seed = get_active_seed()
    is_custom = utils.config.USE_CUSTOM_SEED
    return {
        'seed': active_seed,
        'is_custom': is_custom,
        'cache_size': len(stars_cache)
    }

def get_performance_stats():
    """Retorna estatísticas de performance."""
    return {
        'cache_size': len(stars_cache),
        'total_stars': sum(len(stars) for stars in stars_cache.values()),
        'memory_usage_mb': len(stars_cache) * 0.1  # Estimativa aproximada
    }
