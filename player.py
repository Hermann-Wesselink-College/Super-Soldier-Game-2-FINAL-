import pygame
import math

# Importeert alle instellingen uit settings.py
from settings import *

# Importeert functies uit game_map.py
from game_map import *

def wall_between(x1, y1, x2, y2):
    #True als er een muur tussen (x1, y1) en (x2, y2) zit
    steps = int(math.hypot(x2 - x1, y2 - y1)) // (TILE_SIZE // 2)
    for i in range(1, steps):
        t = i / steps
        mx = int((x1 + (x2 - x1) * t) // TILE_SIZE)
        my = int((y1 + (y2 - y1) * t) // TILE_SIZE)
        if is_wall(mx, my):
            return True
    return False    

# Player class
# Zorgt voor alles wat met de speler te maken heeft
class Player:
    
    # Wordt uitgevoerd wanneer een Player object wordt gemaakt    
    def __init__(self, x, y):
        
        # Startpositie van de speler        
        self.x = x
        self.y = y
        
        # Gezondheid van de speler
        self.health = 100
        
        # Aantal kogels van de speler
        self.ammo = 12
        
        # Hoek waaronder de speler kijkt
        self.angle = 0.0
        
        # Of de speler het compound vervoert
        self.carrying = False

        # Bewegingssnelheid van de speler
        self.speed = 3.0
        
        # Grootte van de speler        
        self.size = PLAYER_SIZE
        
        # Of de speler een sleutel heeft
        self.has_key = False
        
    # Simpele move functie
    # Verplaatst speler met dx en dy
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    # Update functie
    # Wordt elke frame uitgevoerd
    def update(self, keys, cam_x, cam_y):
        
        # Beweging van de speler op basis van toetsenbord input
        
        # W toets = omhoog bewegen        
        if keys[pygame.K_w]:
            
            
            # Nieuwe y positie berekenen
            new_y = self.y - self.speed
            
            # Check voor muur
            if not is_wall(int(self.x // TILE_SIZE), int(new_y // TILE_SIZE)):
                
                # Verplaatst speler omhoog
                self.y = new_y
        
        # S toets = omlaag bewegen
        if keys[pygame.K_s]:
            
            # Nieuwe y positie berekenen
            new_y = self.y + self.speed

            # Check voor muur
            if not is_wall(int(self.x // TILE_SIZE), int(new_y // TILE_SIZE)):
                
                # Verplaatst speler omlaag
                self.y = new_y
        
        # A toets = links bewegen        
        if keys[pygame.K_a]:
             
             # Nieuwe x positie berekenen
             new_x = self.x - self.speed
             
             # Check voor muur
             if not is_wall(int(new_x // TILE_SIZE), int(self.y // TILE_SIZE)):
                
                # Verplaatst speler links
                self.x = new_x
        
        # D toets = rechts bewegen        
        if keys[pygame.K_d]:
            
            # Nieuwe x positie berekenen
            new_x = self.x + self.speed
            
            # Check voor muur
            if not is_wall(int(new_x // TILE_SIZE), int(self.y // TILE_SIZE)):
                
                # Verplaatst speler rechts
                self.x = new_x
        
        # Update kijkrichting van de speler op basis van muispositie

        # Haalt positie van de muis op
        mx, my = pygame.mouse.get_pos()
        
        # Bereken richting van speler naar muis
        # atan2 geeft een hoek/richting terug  
        self.angle = math.atan2((my + cam_y) - self.y, (mx + cam_x) - self.x)      

    # Tekent de speler op het scherm
    def draw(self, screen, cam_x, cam_y, player_img):
        # 1. Scale the raw asset to a reasonable player size first (e.g., 32x32 or 48x48)
        scaled_img = pygame.transform.scale(player_img, (32, 32))
        
        # 2. Rotate the scaled image (negate angle because pygame rotates counter-clockwise)
        rotated_img = pygame.transform.rotate(scaled_img, -math.degrees(self.angle))
        
        # 3. Secure the center position so it doesn't wobble or grow
        new_rect = rotated_img.get_rect(center=(int(self.x - cam_x), int(self.y - cam_y)))
        
        # 4. Draw to screen
        screen.blit(rotated_img, new_rect.topleft)

    # shoot function for the player
    def shoot(self, enemies):
        
        # Controleert of speler nog ammo heeft
        if self.ammo > 0:
            
            # Gebruikt 1 kogel            
            self.ammo -= 1

            hit_one = False

            # Gaat langs alle enemies            
            for enemy in enemies:
                
                # Slaat dode enemies over                
                if not enemy.alive:
                    continue
                if hit_one :
                    continue
                
                # Verschil tussen enemy en speler                
                dx = enemy.x - self.x
                dy = enemy.y - self.y
                
                # Richting naar enemy                
                angle_to_enemy = math.atan2(dy, dx)
                
                # Verschil tussen kijkrichting speler en enemy                
                angle_diff = abs(angle_to_enemy - self.angle + math.pi) % (2 * math.pi) -math.pi
                
                # Controleert:
                # - of enemy dichtbij kijkrichting zit
                # - en binnen bereik is                
                if abs(angle_diff) < 0.15 and math.hypot(dx, dy) < 500:
                    
                    #Checkt of er een muur tussen speler en enemy zit
                    if not wall_between(self.x, self.y, enemy.x, enemy.y):
                        enemy.health -= 50
                        if enemy.health <= 0:
                            enemy.alive = False
                        hit_one = True
                    
    
            # Geeft True terug als er geschoten is            
            return True
        
        # Geeft False terug als speler geen ammo heeft
        return False
    
    # Functie om sleutel op te pakken    
    def pickup_key(self):
        
        # Controleert of speler op een sleutel tile staat        
        if get_tile(int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)) == 'K':
            
            # Geeft speler de sleutel
            self.has_key = True
            
            # Laat weten dat speler het compound draagt            
            self.carrying = True
    