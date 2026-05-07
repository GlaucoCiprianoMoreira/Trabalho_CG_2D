import pygame
import numpy as np
from .SetPixel import setPixel

def load_png_matrix(path):
    img = pygame.image.load(path).convert_alpha()
    w, h = img.get_width(), img.get_height()

    matrix = np.zeros((h, w, 4), dtype=np.uint8)

    for y in range(h):
        for x in range(w):
            matrix[y][x] = img.get_at((x, y))

    return matrix


def draw_sprite(surface, matrix, posX, posY):
    h, w, _ = matrix.shape

    for y in range(h):
        for x in range(w):
            color = matrix[y][x]

            if color[3] == 0:
                continue

            setPixel(surface, posX + x, posY + y, color)

