import pygame
import sys

# Importeert alle instellingen uit settings.py
from settings import *

# Importeert de Player class uit player.py
from player import *

# Importeert de map en functies uit game_map.py
from game_map import *

# Importeert de Enemy class uit enemies.py
from enemies import *

# Importeert de hud file
from hud import *

# Hoofdfunctie van het spel
def main():
    
    # Start pygame op 
    pygame.init()

    
   
    
    # Maakt het scherm aan met de breedte en hoogte uit settings.py
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    # PNG's
    player_img = pygame.image.load("assets/Player.png").convert_alpha()
    enemy_img = pygame.image.load("assets/enemy.png").convert_alpha()
    bullet_img = pygame.image.load("assets/bullet.png").convert_alpha()
    tree_img = pygame.image.load("assets/tree.png").convert_alpha()
    
    # Tile textures
    wall_img = pygame.image.load("assets/wall.png").convert()
    floor_img = pygame.image.load("assets/floor.png").convert()
    key_img = pygame.image.load("assets/key.png").convert_alpha()
    chest_img = pygame.image.load("assets/chest.png").convert_alpha()

    # Scale tile textures to TILE_SIZE (64x64)
    wall_img = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))
    floor_img = pygame.transform.scale(floor_img, (TILE_SIZE, TILE_SIZE))
    key_img = pygame.transform.scale(key_img, (TILE_SIZE, TILE_SIZE))
    chest_img = pygame.transform.scale(chest_img, (TILE_SIZE, TILE_SIZE))
    tree_img = pygame.transform.scale(tree_img, (TILE_SIZE, TILE_SIZE))

    # Zet de titel van het spel bovenaan het venster
    pygame.display.set_caption("Evil Israeli camp")
    
    # Clock object om FPS te regelen
    clock = pygame.time.Clock()

    # Maakt de speler aan op de spawnpositie
    player = Player(SPAWN_POS[0], SPAWN_POS[1])

    import random

    chests = []

    for y, row in enumerate(TILE_MAP):
        for x, tile in enumerate(row):
            if tile == "K":
                chests.append((x, y))

    key_chest = random.choice(chests)
    
    # Lijst met vijanden
    # Elke enemy krijgt een startpositie en een pad waar hij heen beweegt
    # Replace the whole enemy creation loop with this:
    import random

    def random_floor_pos():
        while True:
            x = random.randint(1, MAP_WIDTH - 2)
            y = random.randint(1, MAP_HEIGHT - 2)
            if not is_wall(x, y):
                return (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2)

    enemies = []
    for i in range(6):
        patrol = [random_floor_pos() for _ in range(4)]
        enemies.append(Enemy(patrol[0][0], patrol[0][1], patrol))
            
    # Houdt bij in welke game state het spel zit
    # Bijvoorbeeld "playing" of "WIN"
    game_state = "playing"

    cam_x = 0
    cam_y = 0

    # Objective popup
    showing_objective = True
    obj_font_big = pygame.font.SysFont(None, 64)
    obj_font = pygame.font.SysFont(None, 32)
    while showing_objective:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                showing_objective = False
        screen.fill(BLACK)
        screen.blit(obj_font_big.render("MISSION BRIEFING", True, YELLOW), (WIDTH//2 - 220, HEIGHT//2 - 120))
        screen.blit(obj_font.render("1. Find the KEY hidden in the camp", True, WHITE), (WIDTH//2 - 220, HEIGHT//2 - 40))
        screen.blit(obj_font.render("2. Use the key to open the CHEST", True, WHITE), (WIDTH//2 - 220, HEIGHT//2))
        screen.blit(obj_font.render("3. Carry the compound back to SPAWN", True, WHITE), (WIDTH//2 - 220, HEIGHT//2 + 40))
        screen.blit(obj_font.render("Watch out — enemies will hunt you!", True, RED), (WIDTH//2 - 220, HEIGHT//2 + 80))
        screen.blit(obj_font.render("Press any key to start", True, GREY), (WIDTH//2 - 130, HEIGHT//2 + 140))
        pygame.display.flip()

    pygame.event.clear()
    paused = False

    # Oneindige game loop
    while True:


         # Zorgt dat het spel op de juiste FPS draait
        clock.tick(FPS)

       

        screen.fill(BLACK)


        if paused:
            # Draw a dark overlay over the current frame
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            pause_font = pygame.font.SysFont(None, 64)
            screen.blit(pause_font.render("PAUSED", True, WHITE), (WIDTH//2 - 100, HEIGHT//2 - 60))
            resume_text = pygame.font.SysFont(None, 32).render("Press P to resume", True, GREY)
            screen.blit(resume_text, (WIDTH//2 - 100, HEIGHT//2))
            pygame.display.flip()
            continue

    
        start_x = max(0, int(cam_x // TILE_SIZE))
        end_x = min(MAP_WIDTH, int((cam_x + WIDTH) // TILE_SIZE) + 1)
        start_y = max(0, int(cam_y // TILE_SIZE))
        end_y = min(MAP_HEIGHT, int((cam_y + HEIGHT) // TILE_SIZE) + 1)
        
        
                
       
        
        # Delta time
        # Tijd tussen frames in seconden
        dt = clock.get_time() / 1000.0

        # --- PLACE THIS IMMEDIATELY AFTER: dt = clock.get_time() / 1000.0 ---

        # 1. Clear the screen FIRST
        screen.fill(BLACK)

        # 2. Render Optimized Map Tiles (The camera viewport loop)
        start_x = max(0, int(cam_x // TILE_SIZE))
        end_x = min(MAP_WIDTH, int((cam_x + WIDTH) // TILE_SIZE) + 1)
        start_y = max(0, int(cam_y // TILE_SIZE))
        end_y = min(MAP_HEIGHT, int((cam_y + HEIGHT) // TILE_SIZE) + 1)
        
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = TILE_MAP[y][x]
                
                screen_x = x * TILE_SIZE - cam_x
                screen_y = y * TILE_SIZE - cam_y
                
                # Render Floor Background
                screen.blit(floor_img, (screen_x, screen_y))
                
                # Overlay Objects
                if tile == '#':
                    screen.blit(wall_img, (screen_x, screen_y))
                elif tile == 'K':
                    screen.blit(key_img, (screen_x, screen_y))
                elif tile == 'X':
                    screen.blit(chest_img, (screen_x, screen_y))
                elif tile == 'T':
                    screen.blit(tree_img, (screen_x, screen_y))

        # 3. Update Camera Postion based on Player Movement
        cam_x = int(player.x - WIDTH // 2)
        cam_y = int(player.y - HEIGHT // 2)

        keys = pygame.key.get_pressed()
        player.update(keys, cam_x, cam_y)

        # 4. Update Game Logic and States
        tile_x = int(player.x // TILE_SIZE)
        tile_y = int(player.y // TILE_SIZE)
        player_tile = get_tile(tile_x, tile_y)

        spawn_x, spawn_y = SPAWN_POS
        distance = ((player.x - spawn_x) ** 2 + (player.y - spawn_y) ** 2) ** 0.5

        if player.carrying and distance < 40:
            game_state = "WIN"
        if player.health <= 0:
            game_state = "LOSE"

        for enemy in enemies: 
            enemy.update(dt, player)

        # 5. Draw Entities over the rendered background map
        player.draw(screen, cam_x, cam_y, player_img)

        # Glow effect when carrying compound
        if player.carrying:
            glow_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 255, 0, 60), (40, 40), 40)
            pygame.draw.circle(glow_surf, (255, 255, 0, 30), (40, 40), 35)
            screen.blit(glow_surf, (int(player.x - cam_x) - 40, int(player.y - cam_y) - 40))
        
        for enemy in enemies:
            enemy.draw(screen, cam_x, cam_y, enemy_img) # Pass enemy_img asset here if you modified enemies.py

        # Bekijkt alle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.shoot(enemies, bullet_img)
        
        
       

        # Replace BOTH message blocks with this:
        if player.has_key and not player.carrying:
            font = pygame.font.SysFont(None, 36)
            screen.blit(font.render("You have the key! Find the CHEST!", True, YELLOW), (20, 20))

        if player.carrying:
            font = pygame.font.SysFont(None, 36)
            screen.blit(font.render("Compound secured! Return to SPAWN!", True, (0, 255, 100)), (20, 20))

        # Highlight spawn zone
            spawn_screen_x = SPAWN_POS[0] - cam_x
            spawn_screen_y = SPAWN_POS[1] - cam_y
            spawn_surf = pygame.Surface((TILE_SIZE * 2, TILE_SIZE * 2), pygame.SRCALPHA)
            pygame.draw.rect(spawn_surf, (0, 255, 100, 60), (0, 0, TILE_SIZE * 2, TILE_SIZE * 2), border_radius=8)
            pygame.draw.rect(spawn_surf, (0, 255, 100, 120), (0, 0, TILE_SIZE * 2, TILE_SIZE * 2), 3, border_radius=8)
            screen.blit(spawn_surf, (spawn_screen_x - TILE_SIZE, spawn_screen_y - TILE_SIZE))
        # Controleert of de speler op een sleutel tile staat
        if player_tile == 'K':

            if (tile_x, tile_y) == key_chest:
                if (tile_x, tile_y) == key_chest:
                    player.has_key = True
                    TILE_MAP[tile_y][tile_x] = "."

            

       
        # Controleert of de speler op een chest staat en de sleutel heeft
        elif player_tile == "X" and player.has_key:
            
            # Maakt een font aan
            font = pygame.font.SysFont(None, 36)
            
            # Tekstbericht wanneer het compound is opgepakt
            text = font.render("You picked up the compound! Get back to the spawn!", True, WHITE)
            
            # Tekent de tekst op het scherm
            screen.blit(text, (20, 60))
            
            # Laat weten dat de speler nu het compound draagt
            player.carrying = True
            
            # Verwijdert de chest van de map
            TILE_MAP[tile_y][tile_x] = "."


            # Hud tekenen
        hud_font = pygame.font.SysFont(None, 36)

        # Health bar tekenen
        pygame.draw.rect(screen, (80, 0, 0), (20, HEIGHT -40, 200, 20))
        # Health bar fill
        hp_width = int(200 * (player.health / PLAYER_HEALTH))
        pygame.draw.rect(screen, (220, 50, 50), (20, HEIGHT -40, hp_width, 20))
        pygame.draw.rect(screen, WHITE, (20, HEIGHT - 40, 200, 20), 2)
        hud_font.render("HP", True, WHITE)
        screen.blit(hud_font.render("HP", True, WHITE), (230, HEIGHT - 40)) 

        # Ammo count tekenen
        ammo_text = hud_font.render(f"AMMO: {player.ammo} / {MAX_AMMO}", True, YELLOW)
        screen.blit(ammo_text, (WIDTH - 200, HEIGHT - 65))
        # Update het volledige scherm
        player.update_bullets(enemies)
        # Alles wat getekend is wordt nu zichtbaar
        for b in player.bullets:
            b.draw(screen, cam_x, cam_y)

        if game_state == "WIN":
            
            # Maakt het scherm zwart
            screen.fill(BLACK)
            
            # Maakt een lettertype aan         
            font = pygame.font.SysFont(None, 72)
            
            # Maakt de tekst "YOU WIN!"           
            text = font.render("YOU WIN!", True, GREEN)
            
            # Tekent de tekst op het scherm            
            screen.blit(text,  (WIDTH//2 - 200, HEIGHT//2))
            
            # Update het scherm
            pygame.display.flip()
            
            # Gaat terug naar het begin van de loop
            continue

        if game_state == "LOSE":
            screen.fill(BLACK)
            font = pygame.font.SysFont(None, 72)
            text = font.render("YOU DIED!", True, RED)
            screen.blit(text, (WIDTH//2 - 150, HEIGHT//2))
            pygame.display.flip()
            continue

        pygame.display.flip()


# Zorgt ervoor dat main() alleen wordt uitgevoerd
# als dit bestand direct wordt gestart
if __name__ == "__main__":
    
    # Start het spel    
    main()