from engine.SetPixel import setPixel
from constants import DARKEST

DARKNESS_PIXELS = []
CENTER_X = 80
CENTER_Y = 72
RADIUS_SQ = 24 * 24 # Diâmetro 48 = Raio 24

for y in range(144):
    for x in range(160):
        # Matemática clássica: (X - Xc)² + (Y - Yc)²
        dist_sq = (x - CENTER_X) * (x - CENTER_X) + (y - CENTER_Y) * (y - CENTER_Y)
        
        # Se estiver fora do raio, adiciona na lista de pintura
        if dist_sq > RADIUS_SQ:
            DARKNESS_PIXELS.append((x, y))

def apply_darkness(surface):
    """
    Pinta de DARKEST todos os pixels pré-calculados que estão 
    fora do círculo central de diâmetro 48.
    """
    for x, y in DARKNESS_PIXELS:
        setPixel(surface, x, y, DARKEST)