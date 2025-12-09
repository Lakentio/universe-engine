import pygame
import math
import hashlib
import random
import utils.config
import utils.logger
import utils.save_manager as save_manager
import time

logger = utils.logger.get_logger()
from typing import List, Tuple, Optional

stars_cache = {}
# Set of chunk keys currently considered "visible" (with hysteresis)
visible_chunk_keys = set()

def get_active_seed():
    """Return the active seed based on configuration."""
    if utils.config.USE_CUSTOM_SEED:
        return utils.config.CUSTOM_SEED
    return utils.config.GLOBAL_SEED

def coord_seed(*coords: int) -> int:
    """Generate a deterministic 64-bit seed from coordinates and the global seed."""
    active_seed = get_active_seed()
    # Create a unique and consistent string
    coord_string = f"{active_seed}:{':'.join(map(str, coords))}"
    # Use UTF-8 to ensure consistency in encoding
    key_bytes = coord_string.encode('utf-8')
    # Generate full SHA-256 hash
    hash_bytes = hashlib.sha256(key_bytes).digest()
    # Convert to a 64-bit integer using the first 8 bytes
    return int.from_bytes(hash_bytes[:8], byteorder='big', signed=False)

def initialize_pygame():
    """Initialize Pygame and return the screen and clock."""
    pygame.init()
    screen = pygame.display.set_mode((utils.config.WIDTH, utils.config.HEIGHT))
    pygame.display.set_caption("Universe Engine - Procedural Space Explorer")
    clock = pygame.time.Clock()
    return screen, clock

def generate_star_name(rng: random.Random) -> str:
    """Generate a short unique-looking name for a star."""
    letters = ''.join(rng.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
    numbers = rng.randint(1000, 9999)
    return f"{letters}-{numbers}"

def generate_chunk(cx: int, cy: int, cz: int):
    """Create stars for a given chunk (chunk coordinates, not world coords)."""
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
    """Update the list of visible stars - optimized version.

    Uses a chunk cache and a small hysteresis radius to avoid flicker when
    moving between chunks.
    """
    pcx = math.floor(cam_pos[0] / utils.config.CHUNK_SIZE)
    pcy = math.floor(cam_pos[1] / utils.config.CHUNK_SIZE)
    pcz = math.floor(cam_pos[2] / utils.config.CHUNK_SIZE)
    
    visible_stars = []
    chunks_loaded = 0

    # Pre-load an extra border of chunks (hysteresis) to avoid flicker
    load_radius = utils.config.CHUNK_RADIUS + 1
    for cx in range(pcx - load_radius, pcx + load_radius + 1):
        for cy in range(pcy - load_radius, pcy + load_radius + 1):
            for cz in range(pcz - load_radius, pcz + load_radius + 1):
                key = (cx, cy, cz)
                if key not in stars_cache:
                    stars_cache[key] = generate_chunk(cx, cy, cz)
                    chunks_loaded += 1
                    logger.debug(f"Generated chunk {key} with {len(stars_cache[key])} stars (cache_size={len(stars_cache)})")

    # Update the set of visible chunks with hysteresis:
    # - add all chunks inside the normal radius
    # - only remove chunks that are beyond CHUNK_RADIUS + 1
    global visible_chunk_keys
    desired_keys = set()
    for cx in range(pcx - utils.config.CHUNK_RADIUS, pcx + utils.config.CHUNK_RADIUS + 1):
        for cy in range(pcy - utils.config.CHUNK_RADIUS, pcy + utils.config.CHUNK_RADIUS + 1):
            for cz in range(pcz - utils.config.CHUNK_RADIUS, pcz + utils.config.CHUNK_RADIUS + 1):
                desired_keys.add((cx, cy, cz))

    # Add newly desired chunks (and log which ones were added)
    new_added = desired_keys - visible_chunk_keys
    if new_added:
        logger.debug(f"Adding visible chunk keys: {sorted(list(new_added))}")
    visible_chunk_keys.update(desired_keys)

    # Remove only those that are too far away (outside radius + 1)
    to_remove = []
    for key in visible_chunk_keys:
        kx, ky, kz = key
        if abs(kx - pcx) > utils.config.CHUNK_RADIUS + 1 or abs(ky - pcy) > utils.config.CHUNK_RADIUS + 1 or abs(kz - pcz) > utils.config.CHUNK_RADIUS + 1:
            to_remove.append(key)
    for key in to_remove:
        visible_chunk_keys.discard(key)
        logger.debug(f"Removed visible chunk key (out of hysteresis): {key}")

    # Collect stars from all chunks we keep as visible
    for key in visible_chunk_keys:
        if key in stars_cache:
            visible_stars.extend(stars_cache[key])

    logger.debug(f"Visible chunks: {len(visible_chunk_keys)}, visible_stars_count={len(visible_stars)}, chunks_loaded_this_call={chunks_loaded}")
    
    # Prioritize stars closest to the camera and limit to MAX_VISIBLE_STARS
    if len(visible_stars) > utils.config.MAX_VISIBLE_STARS:
        camx, camy, camz = cam_pos[0], cam_pos[1], cam_pos[2]
        star_dist_pairs = [((s[0]-camx)**2 + (s[1]-camy)**2 + (s[2]-camz)**2, s) for s in visible_stars]
        star_dist_pairs.sort(key=lambda x: x[0])
        trimmed = len(visible_stars) - utils.config.MAX_VISIBLE_STARS
        visible_stars = [s for _, s in star_dist_pairs[:utils.config.MAX_VISIBLE_STARS]]
        logger.debug(f"Trimmed {trimmed} stars to MAX_VISIBLE_STARS={utils.config.MAX_VISIBLE_STARS} (kept closest)")
    
    return visible_stars, chunks_loaded

def handle_mouse_movement(cam_rot):
    """Handle camera rotation using the mouse input."""
    mx, my = pygame.mouse.get_pos()
    center_x, center_y = utils.config.WIDTH // 2, utils.config.HEIGHT // 2
    dx, dy = mx - center_x, my - center_y

    if dx or dy:
        cam_rot[1] += dx * utils.config.MOUSE_SENS
        cam_rot[0] -= dy * utils.config.MOUSE_SENS
        cam_rot[0] = max(-math.pi/2 + 0.01, min(math.pi/2 - 0.01, cam_rot[0]))
        pygame.mouse.set_pos(center_x, center_y)

def clear_stars_cache():
    """Clear the star cache so the universe will be regenerated."""
    global stars_cache
    stars_cache.clear()

def set_universe_seed(new_seed: str):
    """Set a new universe seed and clear the cache."""
    global stars_cache
    stars_cache.clear()
    # Update the configuration
    utils.config.USE_CUSTOM_SEED = True
    utils.config.CUSTOM_SEED = new_seed

def get_universe_info():
    """Return information about the current universe seed and cache."""
    active_seed = get_active_seed()
    is_custom = utils.config.USE_CUSTOM_SEED
    return {
        'seed': active_seed,
        'is_custom': is_custom,
        'cache_size': len(stars_cache)
    }

def save_game(name: str, cam_pos, cam_rot, selected_star=None) -> str:
    """Save the current game state under `name`. Returns the saved file path."""
    state = {
        'cam_pos': list(cam_pos),
        'cam_rot': list(cam_rot),
        'selected_star': selected_star,
        'seed': get_active_seed(),
        'timestamp': time.time()
    }
    path = save_manager.save_state(name, state)
    logger.info(f"Saved game '{name}' -> {path}")
    return path

def load_game(name_or_filename: str):
    """Load a save and return the state dictionary, or None if not found."""
    state = save_manager.load_state(name_or_filename)
    if not state:
        logger.warning(f"Save not found: {name_or_filename}")
        return None
    # Apply seed if present
    if 'seed' in state and state.get('seed'):
        set_universe_seed(state.get('seed'))
    logger.info(f"Loaded game '{name_or_filename}'")
    return state

def list_saves():
    """Return metadata for available saves."""
    return save_manager.list_saves()

def get_performance_stats():
    """Return simple performance statistics about cache and stars."""
    return {
        'cache_size': len(stars_cache),
        'total_stars': sum(len(stars) for stars in stars_cache.values()),
        'memory_usage_mb': len(stars_cache) * 0.1  # Approximate estimate
    }
