import pygame
import numpy as np
from .SetPixel import setPixel

def load_png_matrix(path):
    img = pygame.image.load(path).convert_alpha()
    w, h = img.get_width(), img.get_height()

    matriz = np.zeros((h, w, 4), dtype=np.uint8)

    for y in range(h):
        for x in range(w):
            matriz[y][x] = img.get_at((x, y))

    return matriz


def draw_sprite(surface, matriz, posX, posY):
    h, w, _ = matriz.shape

    for y in range(h):
        for x in range(w):
            color = matriz[y][x]

            if color[3] == 0:
                continue

            setPixel(surface, posX + x, posY + y, color)

