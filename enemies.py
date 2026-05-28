
import pygame
import math
import player
from settings import *
from game_map import is_wall 

class Enemy:
    def __init__(self, x, y, patrol):
        self.x = x
        self.y = y
        self.patrol = patrol
        self.health = 100
        self.patrol_index = 0
        self.see_timer = 0.0
        self.alive = True
        self.chasing = False
        self.angle = 0.0
        self.speed = ENEMY_SPEED
    
    def update(self, dt, player):
        if not self.alive:
            return

        # get current patrol target
        if self.chasing == True:
            target_x, target_y = player.x, player.y
        else:
            target_x, target_y = self.patrol[self.patrol_index]

        # move toward target
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)

        if distance > 5:
            self.angle = math.atan2(dy, dx)
            move_x = (dx / distance) * self.speed
            move_y = (dy / distance) * self.speed
            if not is_wall(int((self.x + move_x) // TILE_SIZE), int(self.y // TILE_SIZE)):
                self.x += move_x
            if not is_wall(int(self.x // TILE_SIZE), int((self.y + move_y) // TILE_SIZE)):
                self.y += move_y
        else:
            # reached target, switch to next patrol point
            self.patrol_index = (self.patrol_index + 1) % len(self.patrol)

        # check if player is in FOV
        dx_p = player.x - self.x
        dy_p = player.y - self.y
        dist_to_player = math.hypot(dx_p, dy_p)
        angle_to_player = math.atan2(dy_p, dx_p)
        angle_diff = abs(angle_to_player - self.angle) % (2 * math.pi)

        if angle_diff < math.radians(ENEMY_FOV_ANGLE) and dist_to_player < ENEMY_FOV_RANGE:
            self.see_timer += dt
            self.chasing = True
        else:
            self.see_timer = max(0.0, self.see_timer - dt)

        if self.see_timer >= ENEMEY_DETECT_TIME:
            self.chasing = True

        if self.chasing:
            dist_to_player = math.hypot(dx_p, dy_p)
            if dist_to_player > ENEMY_FOV_RANGE:
                player.health -= ENEMY_SHOOT_RANGE * dt
    
    def draw(self, screen, cam_x, cam_y):
        if self.alive:
            pygame.draw.circle(screen, RED, (int(self.x - cam_x), int(self.y - cam_y)), 12)
            fov = math.radians(ENEMY_FOV_ANGLE)
            left_x = self.x + math.cos(self.angle - fov) * ENEMY_FOV_RANGE
            left_y = self.y + math.sin(self.angle - fov) * ENEMY_FOV_RANGE
            right_x = self.x + math.cos(self.angle + fov) * ENEMY_FOV_RANGE
            right_y = self.y + math.sin(self.angle + fov) * ENEMY_FOV_RANGE

            pygame.draw.polygon(screen, (255, 255, 0, 80), [
                (int(self.x - cam_x), int(self.y - cam_y)),
                (int(left_x - cam_x), int(left_y - cam_y)),
                (int(right_x - cam_x), int(right_y - cam_y))
            ]) 