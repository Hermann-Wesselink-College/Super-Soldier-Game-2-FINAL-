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
    
    # Zet de titel van het spel bovenaan het venster
    pygame.display.set_caption("Evil Israeli camp")
    
    # Clock object om FPS te regelen
    clock = pygame.time.Clock()

    # Maakt de speler aan op de spawnpositie
    player = Player(SPAWN_POS[0], SPAWN_POS[1])
    
    # Lijst met vijanden
    # Elke enemy krijgt een startpositie en een pad waar hij heen beweegt
    import random

    enemies = []

    for i in range(6):

        patrol = []

        for j in range(4):
            patrol.append((
                random.randint(128, 1152),
                random.randint(128, 1152)
            ))
        
        enemies.append(
            Enemy(
                patrol[0][0],
                patrol[0][1],
                patrol
            )
        )
    # Houdt bij in welke game state het spel zit
    # Bijvoorbeeld "playing" of "WIN"
    game_state = "playing"

    # Oneindige game loop
    while True:

        # Controleert of de speler gewonnen heeft
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
                
        # Zorgt dat het spel op de juiste FPS draait
        clock.tick(FPS)
        
        # Delta time
        # Tijd tussen frames in seconden
        dt = clock.get_time() / 1000.0

        # Bekijkt alle events
        for event in pygame.event.get():
            
            # Als speler het venster sluit            
            if event.type == pygame.QUIT:
                
                # Sluit pygame af                
                pygame.quit()
                
                # Sluit het programma volledig                
                sys.exit()
            
            # Controleert of de muis wordt ingedrukt            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                # Controleert of linker muisknop wordt gebruikt                
                if event.button == 1:  # Left click
                    
                    # Laat de speler schieten                    
                    player.shoot(enemies)
        
        # Camera positie
        # Zorgt ervoor dat de speler in het midden van het scherm blijft
        cam_x = int(player.x - WIDTH // 2)
        cam_y = int(player.y - HEIGHT // 2)

        # Bekijkt welke toetsen worden ingedrukt
        keys = pygame.key.get_pressed()
        
        # Update de speler
        player.update(keys, cam_x, cam_y)

        # Zet spelerpositie om naar tile positie
        tile_x = int(player.x // TILE_SIZE)
        tile_y = int(player.y // TILE_SIZE)
        
        # Kijkt op welke tile de speler staat
        player_tile = get_tile(tile_x, tile_y)

        # Maakt een font voor tekst
        font = pygame.font.SysFont(None, 36)

        # Spawnpositie opslaan
        spawn_x, spawn_y = SPAWN_POS

        # Berekenen van afstand tussen speler en spawn
        # Stelling van Pythagoras        
        distance = ((player.x - spawn_x) ** 2 + (player.y - spawn_y) ** 2) ** 0.5

        # Als speler het compound draagt EN dichtbij spawn is
        if player.carrying and distance < 40:
            
            # Dan wint de speler            
            game_state = "WIN"
        if player.health <= 0:
            game_state = "LOSE"

        # Update alle enemies        
        for enemy in enemies: 
            enemy.update(dt, player)
        
        # Maakt het scherm zwart voordat alles opnieuw getekend wordt
        screen.fill(BLACK)

        # Gaat door alle rijen van de map heen
        for y, row in enumerate(TILE_MAP):
            
            # Gaat door alle tiles in de huidige rij        
            for x, tile in enumerate(row):
                
                # Maakt een rechthoek voor de tile
                # x * TILE_SIZE en y * TILE_SIZE bepalen de positie op de map
                # cam_x en cam_y zorgen ervoor dat de camera meebeweegt
                rect = pygame.Rect(x * TILE_SIZE - cam_x, y * TILE_SIZE - cam_y, TILE_SIZE, TILE_SIZE)
                
                # Controleert welk soort tile het is

                # Muur tile
                if tile == '#':
                    pygame.draw.rect(screen, GREY, rect)
                
                # Gras/vloer tile
                elif tile == '.':
                    pygame.draw.rect(screen, DARK_GREEN, rect)
                
                # Compound/objectief tile
                elif tile == 'C':
                    pygame.draw.rect(screen, YELLOW, rect)
                
                # Sleutel tile
                elif tile == 'K':
                    pygame.draw.rect(screen, BLUE, rect)
                
                # Chest/kist tile
                elif tile == 'X':
                    pygame.draw.rect(screen, (139, 69, 19), rect)

        # Tekent de speler op het scherm
        # cam_x en cam_y zorgen ervoor dat de speler op de juiste plek staat t.o.v. de camera        
        player.draw(screen, cam_x, cam_y)
        
        # Gaat door alle enemies heen
        for enemy in enemies:
            
            # Tekent elke enemy op het scherm
            enemy.draw(screen, cam_x, cam_y)

        # Controleert of de speler het object draagt
        if player.carrying:
            
            # Maakt een font aan voor tekst
            font = pygame.font.SysFont(None, 36)
            
            # Maakt een tekstbericht
            text = font.render("You have the key! Get the compound!", True, WHITE)
            
            # Tekent de tekst linksboven op het scherm
            screen.blit(text, (20, 20))

        # Controleert of de speler op een sleutel tile staat
        if player_tile == 'K':
            
            # Geeft de speler de sleutel
            player.pickup_key()
            
            # Verandert de tile naar vloer zodat de sleutel verdwijnt
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
        # Alles wat getekend is wordt nu zichtbaar
        pygame.display.flip()


# Zorgt ervoor dat main() alleen wordt uitgevoerd
# als dit bestand direct wordt gestart
if __name__ == "__main__":
    
    # Start het spel    
    main()