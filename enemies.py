
import pygame
import math
import player

# Haalt instellingen op
from settings import *

# Functie om te checken of een tile een muur is
from game_map import is_wall 

class Enemy:

    # Wordt aangeroepen bij het maken van een enemy object
    def __init__(self, x, y, patrol):
        
        # Startpositie van de enemy
        self.x = x
        self.y = y
        
        # Lijst met punten waar de enemy tussen heen en weer loopt
        self.patrol = patrol
        
        # Gezondheid (nu nog niet echt gebruikt)
        self.health = 100
        
        # Welke patrol point de enemy nu als doel heeft
        self.patrol_index = 0
        
        # Timer voor het detecteren van de speler
        self.see_timer = 0.0
        
        # Of de enemy nog leeft
        self.alive = True
        
        # Of de enemy de speler aan het achtervolgen is
        self.chasing = False
        
        # Richting waarin de enemy kijkt (in radialen)
        self.angle = 0.0
        
        # Snelheid van de enemy (komt uit settings.py)
        self.speed = ENEMY_SPEED
    
    # Wordt elke frame aangeroepen
    # dt = delta time (tijd tussen frames)
    # player = speler object (zodat enemy speler kan volgen/detecteren)
    def update(self, dt, player):
        
        # Als enemy dood is, doe niks meer
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
        
        # Totale afstand naar target
        distance = math.hypot(dx, dy)

        # Als de enemy nog niet bij het doel is
        if distance > 5:
            
            # Bereken kijkrichting naar target
            self.angle = math.atan2(dy, dx)
            
            # Normaleerde beweging richting target
            move_x = (dx / distance) * self.speed
            move_y = (dy / distance) * self.speed
            
            # Check of er geen muur is in X richting
            if not is_wall(int((self.x + move_x) // TILE_SIZE), int(self.y // TILE_SIZE)):
                self.x += move_x
            
            # Check of er geen muur is in Y richting        
            if not is_wall(int(self.x // TILE_SIZE), int((self.y + move_y) // TILE_SIZE)):
                self.y += move_y
        else:
            # reached target, switch to next patrol point
            self.patrol_index = (self.patrol_index + 1) % len(self.patrol)

        # Detectie van de speler (FOV)

        # Verschil tussen speler en enemy
        dx_p = player.x - self.x
        dy_p = player.y - self.y
        
        # Afstand tot speler        
        dist_to_player = math.hypot(dx_p, dy_p)
        
        # Hoek naar speler        
        angle_to_player = math.atan2(dy_p, dx_p)
        
        # Verschil tussen waar enemy kijkt en waar speler is        
        angle_diff = abs(angle_to_player - self.angle) % (2 * math.pi)

        # Check of speler in gezichtsveld + binnen bereik is
        if angle_diff < math.radians(ENEMY_FOV_ANGLE) and dist_to_player < ENEMY_FOV_RANGE:
            
            # Verhoog timer als speler gezien wordt
            self.see_timer += dt
            self.chasing = True
        
        else:
            # Laat timer langzaam afnemen als speler niet zichtbaar is
            self.see_timer = max(0.0, self.see_timer - dt)

        # Als speler lang genoeg gezien is gaat enemy achtervolgen
        if self.see_timer >= ENEMEY_DETECT_TIME:
            self.chasing = True

        if self.chasing:
            dist_to_player = math.hypot(dx_p, dy_p)
            if dist_to_player < ENEMY_FOV_RANGE:
                player.health -= ENEMY_SHOOT_RANGE * dt
            elif dist_to_player > ENEMY_SHOOT_RANGE:
                self.chasing = False
    
    # Tekent de enemy op het scherm
    def draw(self, screen, cam_x, cam_y):
        
        # Alleen tekenen als enemy leeft
        if self.alive:
            
            # Tekent de enemy als een rode cirkel
            pygame.draw.circle(screen, RED, (int(self.x - cam_x), int(self.y - cam_y)), 12)
            
            # Gezichtsveld (FOV) berekenen
            fov = math.radians(ENEMY_FOV_ANGLE)
            
            # Linker kant van FOV
            left_x = self.x + math.cos(self.angle - fov) * ENEMY_FOV_RANGE
            left_y = self.y + math.sin(self.angle - fov) * ENEMY_FOV_RANGE
            
            # Rechter kant van FOV
            right_x = self.x + math.cos(self.angle + fov) * ENEMY_FOV_RANGE
            right_y = self.y + math.sin(self.angle + fov) * ENEMY_FOV_RANGE

            # Tekent het FOV als een driehoek
            pygame.draw.polygon(screen, (255, 255, 0, 80), [
                (int(self.x - cam_x), int(self.y - cam_y)),
                (int(left_x - cam_x), int(left_y - cam_y)),
                (int(right_x - cam_x), int(right_y - cam_y))
            ]) 