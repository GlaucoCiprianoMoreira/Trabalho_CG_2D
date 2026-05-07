from engine.render.SetPixel import setPixel
from config.Constants import DARKEST

DARKNESS_PIXELS = []
CENTER_X = 80
CENTER_Y = 72
RADIUS_SQ = 24 * 24

for y in range(144):
    for x in range(160):
        dist_sq = (x - CENTER_X) * (x - CENTER_X) + (y - CENTER_Y) * (y - CENTER_Y)
        
        if dist_sq > RADIUS_SQ:
            DARKNESS_PIXELS.append((x, y))

def apply_darkness(surface):
    for x, y in DARKNESS_PIXELS:
        setPixel(surface, x, y, DARKEST)