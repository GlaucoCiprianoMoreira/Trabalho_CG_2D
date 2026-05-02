import pygame
from .LoadMatrix import load_png_matrix, draw_sprite
from constants import load_tiles

# ID=2 representa o minério
levels = [
    [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,2,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1],
        [1,0,2,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1],
        [1,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1],
        [1,0,0,1,1,1,0,0,0,0,0,0,0,1,1,1,1,0,0,1],
        [1,0,0,0,1,1,0,0,1,1,1,0,0,1,1,1,1,0,0,1],
        [1,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,0,0,0,1],
        [1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1],
        [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
        [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
        [1,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,1,1],
        [1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,1],
        [1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,1],
        [1,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ],
]

def draw_level(surface, level, tiles, camera_x, camera_y):
    TILE_SIZE = 16

    start_col = int(camera_x // TILE_SIZE)
    end_col = int((camera_x + surface.get_width()) // TILE_SIZE) + 1
    start_row = int(camera_y // TILE_SIZE)
    end_row = int((camera_y + surface.get_height()) // TILE_SIZE) + 1

    start_col = max(0, start_col)
    end_col = min(len(level[0]), end_col)
    start_row = max(0, start_row)
    end_row = min(len(level), end_row)

    for y in range(start_row, end_row):
        for x in range(start_col, end_col):

            tile = level[y][x]

            if tile < 0:
                continue

            sprite = tiles[tile]

            #Converte as coordenadas do mundo para coordenadas da tela
            screen_x = int((x * TILE_SIZE) - camera_x)
            screen_y = int((y * TILE_SIZE) - camera_y)

            draw_sprite(surface, sprite, screen_x, screen_y)