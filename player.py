import settings
import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.ammo = settings.MAX_AMMO
        self.angle = 0.0
        self.carrying = False

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= self.speed
    new_y = self.y - self.speed
    if not map.is_wall(new_y // map.TILE_SIZE):
        self.y = new_y
