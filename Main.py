import math
import sys
import pygame

from settings import *
from map import * 
from raycasting import *
from player import *
from enemies import *
from hud import *
from objects import *




ENEMY_SPEED = 1.2
ENEMY_HIT_POWER = 50
MAX_AMMO = 30
ENEMY_FOV = math.radians(30)  # full FOV width
ENEMY_DETECT_TIME = 2.0

# Spawn and objective
SPAWN_POS = (2.5, 2.5)
OBJECT_POS = [6.5, 4.5]









def draw_floor_and_ceiling(surface):
    surface.fill((40, 40, 50))
    pygame.draw.rect(surface, (100, 110, 120), (0, 0, WIDTH, HEIGHT // 2))
    pygame.draw.rect(surface, (60, 60, 65), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))






def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("FPS Military Camp Demo")
    clock = pygame.time.Clock()

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    player_pos = [SPAWN_POS[0], SPAWN_POS[1]]
    player_angle = 0.0
    move_forward = move_backward = move_left = move_right = False
    ammo = MAX_AMMO
    flash_timer = 0.0
    player_health = 100.0
    carrying = False
    object_pos = OBJECT_POS.copy()

    enemies = [
        {
            "x": 5.5,
            "y": 2.5,
            "patrol": [(5.5, 2.5), (8.5, 2.5)],
            "patrol_index": 0,
            "health": 100,
            "alive": True,
        },
        {
            "x": 7.5,
            "y": 6.5,
            "patrol": [(7.5, 6.5), (4.5, 6.5)],
            "patrol_index": 0,
            "health": 100,
            "alive": True,
        },
        {
            "x": 3.5,
            "y": 7.5,
            "patrol": [(3.5, 7.5), (3.5, 4.5)],
            "patrol_index": 0,
            "health": 100,
            "alive": True,
        },
    ]

    # ensure enemy detection fields
    for e in enemies:
        e.setdefault("see_timer", 0.0)
        e.setdefault("chasing", False)

    while True:
        dt = clock.tick(FPS) / 1000.0
        flash_timer = max(0.0, flash_timer - dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_w:
                    move_forward = True
                elif event.key == pygame.K_s:
                    move_backward = True
                elif event.key == pygame.K_a:
                    move_left = True
                elif event.key == pygame.K_d:
                    move_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    move_forward = False
                elif event.key == pygame.K_s:
                    move_backward = False
                elif event.key == pygame.K_a:
                    move_left = False
                elif event.key == pygame.K_d:
                    move_right = False
            elif event.type == pygame.MOUSEMOTION:
                player_angle = normalize_angle(player_angle + event.rel[0] * PLAYER_ROT_SPEED)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and ammo > 0:
                    if shoot(enemies, player_pos, player_angle):
                        flash_timer = 0.08
                    ammo -= 1

        dx = dy = 0.0
        sin_a = math.sin(player_angle)
        cos_a = math.cos(player_angle)
        if move_forward:
            dx += cos_a * PLAYER_SPEED * dt
            dy += sin_a * PLAYER_SPEED * dt
        if move_backward:
            dx -= cos_a * PLAYER_SPEED * dt
            dy -= sin_a * PLAYER_SPEED * dt
        if move_left:
            dx += sin_a * PLAYER_SPEED * dt
            dy -= cos_a * PLAYER_SPEED * dt
        if move_right:
            dx -= sin_a * PLAYER_SPEED * dt
            dy += cos_a * PLAYER_SPEED * dt


        next_x = player_pos[0] + dx
        next_y = player_pos[1] + dy
        if not is_blocking(int(next_x), int(player_pos[1])):
            player_pos[0] = next_x
        if not is_blocking(int(player_pos[0]), int(next_y)):
            player_pos[1] = next_y

        player = {"pos": player_pos, "health": player_health}
        update_enemies(enemies, dt, player)
        player_health = player["health"]

        draw_floor_and_ceiling(screen)
        cast_rays(screen, player_pos, player_angle)
        draw_enemies(screen, enemies, player_pos, player_angle)
        draw_object(screen, object_pos, player_pos, player_angle)
        draw_hud(screen, ammo, sum(1 for e in enemies if e["alive"]), player_health)
        draw_minimap(screen, player_pos, player_angle, enemies)

        if flash_timer > 0:
            muzzle_flash = pygame.Surface((60, 20))
            muzzle_flash.set_alpha(200)
            muzzle_flash.fill((255, 220, 120))
            screen.blit(muzzle_flash, (WIDTH // 2 + 20, HEIGHT - 160))

        pygame.display.flip()

        object_pos, carrying = update_object(screen, player_pos, object_pos, carrying)
        # lose condition: player health
        if player_health <= 0:
            font = pygame.font.SysFont(None, 72)
            lose_text = font.render("You were defeated! Game Over.", True, (240, 120, 120))
            screen.blit(lose_text, (WIDTH // 2 - lose_text.get_width() // 2, HEIGHT // 2 - 40))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()
