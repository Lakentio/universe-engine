from core.engine import initialize_pygame, update_visible_stars, handle_mouse_movement, get_universe_info, get_performance_stats
from rendering.render import (
    draw_cursor, draw_arrow, draw_star_info, draw_text, world_to_screen,
    draw_gradient_background
)
import utils.config
import pygame
import sys
import math
import time

def main():
    cam_pos = [0.0, 0.0, -10.0]
    cam_rot = [0.0, 0.0]  # pitch, yaw
    selected_star = None
    frame_times = []  # Para calcular FPS médio
    last_time = time.time()

    screen, clock = initialize_pygame()
    
    # Inicializa estrelas visíveis
    visible_stars, chunks_loaded = update_visible_stars(cam_pos, cam_rot)

    while True:
        current_time = time.time()
        dt = clock.tick(utils.config.TARGET_FPS) / 1000.0
        
        # Calcula FPS médio (simplificado)
        frame_times.append(current_time - last_time)
        if len(frame_times) > 30:  # Reduzido de 60 para 30
            frame_times.pop(0)
        avg_fps = 1.0 / (sum(frame_times) / len(frame_times)) if frame_times else 0
        last_time = current_time

        # Desenha fundo simples
        draw_gradient_background(screen)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clique esquerdo
                mx, my = pygame.mouse.get_pos()
                # Busca em todas as estrelas visíveis para seleção
                for star in visible_stars:
                    screen_pos = world_to_screen(*star[:3], cam_pos, cam_rot)
                    if screen_pos and math.hypot(mx - screen_pos[0], my - screen_pos[1]) < 10:
                        selected_star = star
                        break

        # Input teclado
        keys = pygame.key.get_pressed()
        forward = keys[pygame.K_w] - keys[pygame.K_s]
        strafe = keys[pygame.K_d] - keys[pygame.K_a]
        vertical = keys[pygame.K_e] - keys[pygame.K_q]

        sin_y, cos_y = math.sin(cam_rot[1]), math.cos(cam_rot[1])
        cam_pos[0] += (strafe * cos_y + forward * sin_y) * utils.config.MOVE_SPEED * dt
        cam_pos[2] += (forward * cos_y - strafe * sin_y) * utils.config.MOVE_SPEED * dt
        cam_pos[1] += vertical * utils.config.MOVE_SPEED * dt

        # Input mouse
        handle_mouse_movement(cam_rot)

        # Atualiza estrelas visíveis (menos frequente)
        if len(frame_times) % 5 == 0:  # Atualiza a cada 5 frames
            visible_stars, chunks_loaded = update_visible_stars(cam_pos, cam_rot)
            # Verifica se a estrela selecionada ainda está visível
            if selected_star and selected_star not in visible_stars:
                selected_star = None

        # Renderiza estrelas (otimizado)
        rendered_count = 0
        for sx, sy, sz, size, name in visible_stars:
            screen_pos = world_to_screen(sx, sy, sz, cam_pos, cam_rot)
            if screen_pos:
                # Renderização ultra-simples
                pygame.draw.circle(screen, (255, 255, 255), screen_pos, max(1, int(size)))
                rendered_count += 1
                
                # Destaca estrela selecionada
                if selected_star and (sx, sy, sz, size, name) == selected_star:
                    draw_arrow(screen, screen_pos)

        # Desenha o cursor visível
        draw_cursor(screen)

        # HUD com informações importantes
        draw_text(screen, f"FPS: {avg_fps:.1f}", (10, 10), utils.config.UI_COLORS['success'])
        draw_text(screen, f"Estrelas: {rendered_count}", (10, 30), utils.config.UI_COLORS['text'])
        draw_text(screen, f"Pos: ({cam_pos[0]:.0f}, {cam_pos[1]:.0f}, {cam_pos[2]:.0f})", (10, 50), utils.config.UI_COLORS['text'])
        
        # Informações da seed
        universe_info = get_universe_info()
        seed_text = f"Seed: {universe_info['seed'][:20]}{'...' if len(universe_info['seed']) > 20 else ''}"
        draw_text(screen, seed_text, (10, 70), utils.config.UI_COLORS['text'])
        
        # Exibe informações da estrela selecionada (apenas se selecionada)
        if selected_star:
            draw_star_info(screen, selected_star)

        pygame.display.flip()

if __name__ == "__main__":
    main()
