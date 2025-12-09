from core.engine import initialize_pygame, update_visible_stars, handle_mouse_movement, get_universe_info, get_performance_stats, save_game, load_game, list_saves
from rendering.render import (
    draw_cursor, draw_arrow, draw_star_info, draw_text, world_to_screen,
    draw_gradient_background, create_panel_surface
)
import utils.config
import os
import pygame
import sys
import math
import time
import utils.logger

logger = utils.logger.get_logger()

def main(load=None, save_on_start=None, headless=False, fps=None, profile=False):
    cam_pos = [0.0, 0.0, -10.0]
    cam_rot = [0.0, 0.0]  # pitch, yaw
    selected_star = None
    # In-game save input
    save_input_active = False
    save_input_text = ""
    # Input UI font
    input_font = None
    frame_times = []  # For calculating average FPS
    last_time = time.time()

    # Apply runtime flags
    if fps is not None:
        utils.config.TARGET_FPS = int(fps)
    if profile:
        utils.config.DEBUG_LOG = True

    screen, clock = initialize_pygame()

    # initialize input font after pygame.init
    input_font = pygame.font.SysFont("monospace", 16, bold=True)
    
    # If requested via CLI, apply the loaded state before generating chunks
    if load:
        state = load_game(load)
        if state:
            cam_pos = state.get('cam_pos', cam_pos)
            cam_rot = state.get('cam_rot', cam_rot)
            selected_star = state.get('selected_star', selected_star)

    # Initialize visible stars
    visible_stars, chunks_loaded = update_visible_stars(cam_pos, cam_rot)
    last_chunk_update = 0.0
    # If requested via CLI, save immediately with the provided name
    if save_on_start:
        try:
            path = save_game(save_on_start, cam_pos, cam_rot, selected_star)
            logger.info(f"Saved on start -> {path}")
        except Exception:
            logger.exception("Failed to save on start")
    # Automatic simulation to reproduce movement across chunks
    AUTO_MOVE = os.getenv('DEBUG_SIM_MOVE', '0') == '1'
    prev_chunk = (math.floor(cam_pos[0] / utils.config.CHUNK_SIZE), math.floor(cam_pos[1] / utils.config.CHUNK_SIZE), math.floor(cam_pos[2] / utils.config.CHUNK_SIZE))

    while True:
        current_time = time.time()
        dt = clock.tick(utils.config.TARGET_FPS) / 1000.0
        
        # Calculate average FPS (simplified)
        frame_times.append(current_time - last_time)
        if len(frame_times) > 30:  # Reduzido de 60 para 30
            frame_times.pop(0)
        avg_fps = 1.0 / (sum(frame_times) / len(frame_times)) if frame_times else 0
        last_time = current_time

            # Draw a simple background
        draw_gradient_background(screen)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # Text input for saving
            if save_input_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                                    # confirm save
                        if save_input_text.strip():
                            try:
                                path = save_game(save_input_text.strip(), cam_pos, cam_rot, selected_star)
                                logger.info(f"Saved -> {path}")
                            except Exception:
                                logger.exception("Failed to save via input")
                        save_input_active = False
                        save_input_text = ""
                    elif event.key == pygame.K_ESCAPE:
                        save_input_active = False
                        save_input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        save_input_text = save_input_text[:-1]
                    else:
                        # use event.unicode to respect keyboard layout
                        ch = getattr(event, 'unicode', '')
                        if ch and len(ch) == 1:
                            save_input_text += ch
                # while in input mode, ignore other handlers
                continue
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
                # Quick save with timestamp
                try:
                    save_name = f"quick_{int(time.time())}"
                    path = save_game(save_name, cam_pos, cam_rot, selected_star)
                    logger.info(f"Quick saved -> {path}")
                except Exception as e:
                    logger.exception(f"Failed to quick save: {e}")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F6:
                # Open input to enter save name
                save_input_active = True
                save_input_text = ""
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F9:
                # Quick load: try to load the most recent save
                try:
                    saves = list_saves()
                    if saves:
                        latest = saves[0]['filename']
                        state = load_game(latest)
                        if state:
                            cam_pos = state.get('cam_pos', cam_pos)
                            cam_rot = state.get('cam_rot', cam_rot)
                            selected_star = state.get('selected_star', selected_star)
                            logger.info(f"Quick loaded {latest}")
                    else:
                        logger.info("No save found to load.")
                except Exception as e:
                    logger.exception(f"Failed to quick load: {e}")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F8:
                # List saves in the logger
                try:
                    saves = list_saves()
                    logger.info(f"Available saves ({len(saves)}): {[s['filename'] for s in saves]}")
                except Exception as e:
                    logger.exception(f"Failed to list saves: {e}")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                mx, my = pygame.mouse.get_pos()
                # Search all visible stars for selection
                for star in visible_stars:
                    screen_pos = world_to_screen(*star[:3], cam_pos, cam_rot)
                    if screen_pos and math.hypot(mx - screen_pos[0], my - screen_pos[1]) < 10:
                        selected_star = star
                        # Selection log
                        sx, sy, sz, ssize, sname = star
                        cx = math.floor(sx / utils.config.CHUNK_SIZE)
                        cy = math.floor(sy / utils.config.CHUNK_SIZE)
                        cz = math.floor(sz / utils.config.CHUNK_SIZE)
                        logger.info(f"Star selected: {sname} at ({sx:.1f},{sy:.1f},{sz:.1f}) in chunk ({cx},{cy},{cz})")
                        break

        # Keyboard input
        keys = pygame.key.get_pressed()
        forward = keys[pygame.K_w] - keys[pygame.K_s]
        strafe = keys[pygame.K_d] - keys[pygame.K_a]
        vertical = keys[pygame.K_e] - keys[pygame.K_q]

        sin_y, cos_y = math.sin(cam_rot[1]), math.cos(cam_rot[1])
        cam_pos[0] += (strafe * cos_y + forward * sin_y) * utils.config.MOVE_SPEED * dt
        cam_pos[2] += (forward * cos_y - strafe * sin_y) * utils.config.MOVE_SPEED * dt
        cam_pos[1] += vertical * utils.config.MOVE_SPEED * dt

        # Mouse input
        handle_mouse_movement(cam_rot)

        # Auto-move for debug (always forward in the current direction)
        if AUTO_MOVE:
            auto_forward = 1.0
            sin_y, cos_y = math.sin(cam_rot[1]), math.cos(cam_rot[1])
            cam_pos[0] += (auto_forward * sin_y) * utils.config.MOVE_SPEED * dt
            cam_pos[2] += (auto_forward * cos_y) * utils.config.MOVE_SPEED * dt
            # Check if we crossed a chunk boundary
            pcx = math.floor(cam_pos[0] / utils.config.CHUNK_SIZE)
            pcy = math.floor(cam_pos[1] / utils.config.CHUNK_SIZE)
            pcz = math.floor(cam_pos[2] / utils.config.CHUNK_SIZE)
            cur_chunk = (pcx, pcy, pcz)
            if cur_chunk != prev_chunk:
                logger.info(f"Crossed chunk boundary: {prev_chunk} -> {cur_chunk}, cam_pos=({cam_pos[0]:.1f},{cam_pos[1]:.1f},{cam_pos[2]:.1f})")
                prev_chunk = cur_chunk

        # Update visible stars periodically (time-based instead of per-frame)
        if current_time - last_chunk_update > 0.12:  # ~8-9 updates per second
            visible_stars, chunks_loaded = update_visible_stars(cam_pos, cam_rot)
            last_chunk_update = current_time
            # Check if the selected star is still visible
            if selected_star and selected_star not in visible_stars:
                logger.info(f"Selected star no longer visible, clearing selection: {selected_star[4]}")
                selected_star = None

            # Log statistics after chunk update
            stats = get_performance_stats()
            logger.debug(f"Chunk update: chunks_loaded={chunks_loaded}, cache_size={stats.get('cache_size')}, total_stars={stats.get('total_stars')}")
            # Additional culling/projection stats for debugging
            def _camera_space_z(px, py, pz, cam_pos, cam_rot):
                x = px - cam_pos[0]
                y = py - cam_pos[1]
                z = pz - cam_pos[2]
                sin_y, cos_y = math.sin(cam_rot[1]), math.cos(cam_rot[1])
                x, z = x * cos_y - z * sin_y, x * sin_y + z * cos_y
                sin_x, cos_x = math.sin(cam_rot[0]), math.cos(cam_rot[0])
                y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
                return z

            total_tested = len(visible_stars)
            in_front = sum(1 for s in visible_stars if _camera_space_z(s[0], s[1], s[2], cam_pos, cam_rot) > 0)
            on_screen = sum(1 for s in visible_stars if world_to_screen(s[0], s[1], s[2], cam_pos, cam_rot) is not None)
            logger.debug(f"Projection stats: tested={total_tested}, in_front={in_front}, on_screen={on_screen}")

        # Render stars (optimized)
        rendered_count = 0
        for sx, sy, sz, size, name in visible_stars:
            screen_pos = world_to_screen(sx, sy, sz, cam_pos, cam_rot)
            if screen_pos:
                # Ultra-simple rendering
                pygame.draw.circle(screen, (255, 255, 255), screen_pos, max(1, int(size)))
                rendered_count += 1
                
                # Highlight selected star
                if selected_star and (sx, sy, sz, size, name) == selected_star:
                    draw_arrow(screen, screen_pos)

        # Draw visible cursor
        draw_cursor(screen)

        # HUD with important information
        draw_text(screen, f"FPS: {avg_fps:.1f}", (10, 10), utils.config.UI_COLORS['success'])
        draw_text(screen, f"Estrelas: {rendered_count}", (10, 30), utils.config.UI_COLORS['text'])
        draw_text(screen, f"Pos: ({cam_pos[0]:.0f}, {cam_pos[1]:.0f}, {cam_pos[2]:.0f})", (10, 50), utils.config.UI_COLORS['text'])
        
        # Seed information
        universe_info = get_universe_info()
        seed_text = f"Seed: {universe_info['seed'][:20]}{'...' if len(universe_info['seed']) > 20 else ''}"
        draw_text(screen, seed_text, (10, 70), utils.config.UI_COLORS['text'])
        
        # Display selected star information (if any)
        if selected_star:
            draw_star_info(screen, selected_star)

        # If save input mode is active, draw a simple panel
        if save_input_active:
            panel_w = 420
            panel_h = 80
            panel = create_panel_surface(panel_w, panel_h)
            prompt = input_font.render("Nome do save:", True, utils.config.UI_COLORS['accent'])
            panel.blit(prompt, (12, 10))
            # User text
            txt = input_font.render(save_input_text or "(digite e pressione ENTER)", True, utils.config.UI_COLORS['text'])
            panel.blit(txt, (12, 38))
            screen.blit(panel, ((utils.config.WIDTH - panel_w) // 2, (utils.config.HEIGHT - panel_h) // 2))

        pygame.display.flip()

if __name__ == "__main__":
    main()
