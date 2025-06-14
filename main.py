from engine import initialize_pygame, update_visible_stars, handle_mouse_movement
from render import draw_cursor, draw_arrow, draw_star_info, draw_text, world_to_screen
from config import WIDTH, HEIGHT, TARGET_FPS, MOVE_SPEED
import pygame
import sys
import math

def main():
    cam_pos = [0.0, 0.0, -10.0]
    cam_rot = [0.0, 0.0]  # pitch, yaw
    selected_star = None

    screen, clock = initialize_pygame()
    update_visible_stars(cam_pos)

    while True:
        dt = clock.tick(TARGET_FPS) / 1000.0
        screen.fill((0, 0, 0))

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
                for star in update_visible_stars(cam_pos):
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
        cam_pos[0] += (strafe * cos_y + forward * sin_y) * MOVE_SPEED * dt
        cam_pos[2] += (forward * cos_y - strafe * sin_y) * MOVE_SPEED * dt
        cam_pos[1] += vertical * MOVE_SPEED * dt

        # Input mouse
        handle_mouse_movement(cam_rot)

        # Atualiza estrelas visíveis
        update_visible_stars(cam_pos)

        # Renderiza estrelas
        for sx, sy, sz, size, name in update_visible_stars(cam_pos):
            screen_pos = world_to_screen(sx, sy, sz, cam_pos, cam_rot)
            if screen_pos:
                pygame.draw.circle(screen, (255, 255, 255), screen_pos, max(1, int(size)))
                if selected_star and (sx, sy, sz, size, name) == selected_star:
                    draw_arrow(screen, screen_pos)

        # Desenha o cursor visível
        draw_cursor(screen)

        # Exibe informações da estrela selecionada
        if selected_star:
            draw_star_info(screen, selected_star)

        # HUD mínimo
        draw_text(screen, f"Pos: {cam_pos[0]:.1f}, {cam_pos[1]:.1f}, {cam_pos[2]:.1f}", (10, 10))
        draw_text(screen, f"FPS: {clock.get_fps():.1f}", (10, 28))

        pygame.display.flip()

if __name__ == "__main__":
    main()
