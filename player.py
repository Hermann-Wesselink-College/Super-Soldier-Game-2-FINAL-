import pygame
import math
from settings import *
from game_map import *


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.ammo = 12
        self.angle = 0.0
        self.carrying = False
        self.speed = 1.0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def update(self, keys):
        # Move up
        if keys[pygame.K_w]:
            new_y = self.y - self.speed
            if not is_wall(int(self.x // TILE_SIZE), int(new_y // TILE_SIZE)):
                self.y = new_y#Move down
        
        if keys[pygame.K_s]:
            new_y = self.y + self.speed
            if not is_wall(int(self.x // TILE_SIZE), int(new_y // TILE_SIZE)):
                self.y = new_y
        
        if keys[pygame.K_a]:
             new_x = self.x - self.speed
             if not is_wall(int(new_x // TILE_SIZE), int(self.y // TILE_SIZE)):
                self.x = new_x
        
        if keys[pygame.K_d]:
            new_x = self.x + self.speed
            if not is_wall(int(new_x // TILE_SIZE), int(self.y // TILE_SIZE)):
                self.x = new_x
        
        mx, my = pygame.mouse.get_pos()
        self.angle = math.atan2(my -self.y, mx - self.x)

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), 10)