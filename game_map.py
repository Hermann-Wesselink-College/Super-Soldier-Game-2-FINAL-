# Importeert instellingen uit settings.py
from settings import *

# De volledige map van het spel
# Elke string wordt omgezet naar een lijst van losse tekens
# Hierdoor kun je individuele tiles aanpassen tijdens het spel
TILE_MAP = [

    # # = muur
    # . = vloer/gras
    # X = chest/compound
    # K = sleutel
    list("########################################"),
    list("#......................................#"),
    list("#......................................#"),
    list("#...########...........########........#"),
    list("#...#......#...........#......#........#"),
    list("#...#..X...#...........#..K...#........#"),
    list("#...#......#...........#......#........#"),
    list("#...###....#...........###..###........#"),
    list("#......................................#"),
    list("#......................................#"),
    list("#......############################....#"),
    list("#......#..........................#....#"),
    list("#......#..........................#....#"),
    list("#......#...K......................#....#"),
    list("#......#..........................#....#"),
    list("#......####################..######....#"),
    list("#......................................#"),
    list("#...........####.....####..............#"),
    list("#...........#........#.................#"),
    list("#...........#.K......#.................#"),
    list("#...........####.....####..............#"),
    list("#......................................#"),
    list("#......................................#"),
    list("#......................................#"),
    list("########################################"),
]
# Breedte van de map
# Kijkt hoeveel tiles er in de eerste rij zitten
MAP_WIDTH = len(TILE_MAP[0])

# Hoogte van de map
# Kijkt hoeveel rijen de map heeft
MAP_HEIGHT = len(TILE_MAP)

# Functie die controleert of een tile een muur is
def is_wall(mx, my):
    
    # Controleert of positie buiten de map ligt
    if mx < 0 or my < 0 or mx >= MAP_WIDTH or my >= MAP_HEIGHT:
        
        # Buiten de map telt als muur        
        return True
    
    # Geeft True terug als de tile een muur (#) is
    return TILE_MAP[my][mx] == '#'

# Functie die teruggeeft welke tile op een positie staat
def get_tile (mx,my):
    
    # Controleert of positie buiten de map ligt
    if mx < 0 or my < 0 or mx >= MAP_WIDTH or my >= MAP_HEIGHT:
        
        # Buiten de map wordt behandeld als muur
        return '#'
    
    # Geeft de tile terug op positie mx,my
    # Bijvoorbeeld '#', '.', 'K' of 'X'    
    return TILE_MAP[my][mx]


