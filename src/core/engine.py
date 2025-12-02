import pygame
import math
import hashlib
import random
import utils.config
import utils.logger

logger = utils.logger.get_logger()
from typing import List, Tuple, Optional

stars_cache = {}
# Conjunto de chunks atualmente considerados "visíveis" (com histerese)
visible_chunk_keys = set()

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

    # Pré-carrega uma borda extra de chunks (hysteresis) para evitar flicker
    load_radius = utils.config.CHUNK_RADIUS + 1
    for cx in range(pcx - load_radius, pcx + load_radius + 1):
        for cy in range(pcy - load_radius, pcy + load_radius + 1):
            for cz in range(pcz - load_radius, pcz + load_radius + 1):
                key = (cx, cy, cz)
                if key not in stars_cache:
                    stars_cache[key] = generate_chunk(cx, cy, cz)
                    chunks_loaded += 1
                    logger.debug(f"Generated chunk {key} with {len(stars_cache[key])} stars (cache_size={len(stars_cache)})")

    # Atualiza conjunto de chunks visíveis com histerese:
    # - adiciona todos os chunks dentro do raio normal
    # - só remove chunks que estejam além de CHUNK_RADIUS + 1
    global visible_chunk_keys
    desired_keys = set()
    for cx in range(pcx - utils.config.CHUNK_RADIUS, pcx + utils.config.CHUNK_RADIUS + 1):
        for cy in range(pcy - utils.config.CHUNK_RADIUS, pcy + utils.config.CHUNK_RADIUS + 1):
            for cz in range(pcz - utils.config.CHUNK_RADIUS, pcz + utils.config.CHUNK_RADIUS + 1):
                desired_keys.add((cx, cy, cz))

    # Adiciona os novos desejados (e loga quais foram adicionados)
    new_added = desired_keys - visible_chunk_keys
    if new_added:
        logger.debug(f"Adding visible chunk keys: {sorted(list(new_added))}")
    visible_chunk_keys.update(desired_keys)

    # Remove apenas os que estão muito distantes (fora do raio + 1)
    to_remove = []
    for key in visible_chunk_keys:
        kx, ky, kz = key
        if abs(kx - pcx) > utils.config.CHUNK_RADIUS + 1 or abs(ky - pcy) > utils.config.CHUNK_RADIUS + 1 or abs(kz - pcz) > utils.config.CHUNK_RADIUS + 1:
            to_remove.append(key)
    for key in to_remove:
        visible_chunk_keys.discard(key)
        logger.debug(f"Removed visible chunk key (out of hysteresis): {key}")

    # Coleta estrelas de todos os chunks que estamos mantendo como visíveis
    for key in visible_chunk_keys:
        if key in stars_cache:
            visible_stars.extend(stars_cache[key])

    logger.debug(f"Visible chunks: {len(visible_chunk_keys)}, visible_stars_count={len(visible_stars)}, chunks_loaded_this_call={chunks_loaded}")
    
    # Prioriza as estrelas mais próximas da câmera e limita a MAX_VISIBLE_STARS
    if len(visible_stars) > utils.config.MAX_VISIBLE_STARS:
        camx, camy, camz = cam_pos[0], cam_pos[1], cam_pos[2]
        star_dist_pairs = [((s[0]-camx)**2 + (s[1]-camy)**2 + (s[2]-camz)**2, s) for s in visible_stars]
        star_dist_pairs.sort(key=lambda x: x[0])
        trimmed = len(visible_stars) - utils.config.MAX_VISIBLE_STARS
        visible_stars = [s for _, s in star_dist_pairs[:utils.config.MAX_VISIBLE_STARS]]
        logger.debug(f"Trimmed {trimmed} stars to MAX_VISIBLE_STARS={utils.config.MAX_VISIBLE_STARS} (kept closest)")
    
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
