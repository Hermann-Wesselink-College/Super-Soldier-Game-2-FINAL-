import pygame
import sys
from settings import *
from player import *
from game_map import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Evil Israeli camp")
    clock = pygame.time.Clock()

    player = Player(SPAWN_POS[0], SPAWN_POS[1])

    while True:

       
        

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.update(keys)
        cam_x = int(player.x - WIDTH // 2)
        cam_y = int(player.y - HEIGHT // 2)

        screen.fill(BLACK)

        for y, row in enumerate(TILE_MAP):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE - cam_x, y * TILE_SIZE - cam_y, TILE_SIZE, TILE_SIZE)
                if tile == '#':
                    pygame.draw.rect(screen, GREY, rect)
                elif tile == '.':
                    pygame.draw.rect(screen, DARK_GREEN, rect)
                elif tile == 'C':
                    pygame.draw.rect(screen, YELLOW, rect)
        player.draw(screen, cam_x, cam_y)
        pygame.display.flip()


if __name__ == "__main__":
    main()
