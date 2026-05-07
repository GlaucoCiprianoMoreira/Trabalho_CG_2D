import pygame
import numpy as np
from engine.render.Transformations import scale, apply
from engine.render.SetPixel import setPixel

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

    surf_w = surface.get_width()
    surf_h = surface.get_height()

    start_x = max(0, -posX)
    start_y = max(0, -posY)
    
    end_x = min(w, surf_w - posX)
    end_y = min(h, surf_h - posY)

    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            color = matrix[y][x]

            if color[3] == 0:
                continue

            setPixel(surface, posX + x, posY + y, color)

def draw_sprite_transformed(surface, matrix, posX, posY, scale_factor):
    if scale_factor <= 0:
        return

    h, w, _ = matrix.shape
    new_w = int(w * scale_factor)
    new_h = int(h * scale_factor)
    
    offset_x = int((w - new_w) / 2)
    offset_y = int((h - new_h) / 2)

    surf_w = surface.get_width()
    surf_h = surface.get_height()

    start_x = max(0, -(posX + offset_x))
    start_y = max(0, -(posY + offset_y))
    end_x = min(new_w, surf_w - (posX + offset_x))
    end_y = min(new_h, surf_h - (posY + offset_y))

    M_inv = scale(1.0 / scale_factor, 1.0 / scale_factor)

    for dy in range(start_y, end_y):
        for dx in range(start_x, end_x):
            
            src_x, src_y = apply((dx, dy), M_inv)

            if 0 <= src_x < w and 0 <= src_y < h:
                color = matrix[src_y][src_x]
                if color[3] == 0:
                    continue
                
                setPixel(surface, posX + offset_x + dx, posY + offset_y + dy, color)