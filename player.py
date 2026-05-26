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

def update(self, keys):
        # Move up
        if keys[pygame.K_w]:
            new_y = self.y - self.speed
            if not is_wall(int(self.x // TILE_SIZE), int(new_y // TILE_SIZE)):
                self.y = new_y