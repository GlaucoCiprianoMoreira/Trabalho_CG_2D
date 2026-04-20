import pygame
from .LoadMatrix import load_png_matrix, draw_sprite
from constants import load_tiles

level = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,2,2,1,2,2,2,1,2,1],
    [1,2,2,2,2,2,2,2,2,1],
    [1,2,1,2,2,1,2,2,2,1],
    [1,2,2,2,2,2,2,2,2,1],
    [1,2,2,2,1,2,2,2,2,1],
    [1,2,2,2,1,2,2,2,2,1],
    [1,2,2,2,1,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1],
]

def draw_level(surface, level, tiles):
    for y in range(len(level)):
        for x in range(len(level[y])):

            tile = level[y][x]

            if tile == 0:
                continue

            sprite = tiles[tile]

            draw_sprite(surface, sprite, x*16, y*16)