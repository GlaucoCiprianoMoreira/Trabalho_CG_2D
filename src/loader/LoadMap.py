import random

from .LoadMatrix import draw_sprite
from config.Constants import TILE_SIZE
from game.mechanics.Ore import Ore
from game.mechanics.Chest import Chest
from game.mechanics.Mimic import Mimic

levels = [
    # [
    #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #     [1, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 4, 1],
    #     [1, 0, 0, 2, 1, 1, 2, 2, 0, 2, 1, 1, 0, 0, 0, 1],
    #     [1, 0, 0, 0, 1, 1,11,11,11, 1, 1, 2, 0, 0, 0, 1],
    #     [1, 0, 0, 0, 1, 1, 1,11,11, 3, 1, 1, 0, 0, 0, 1],
    #     [1, 0, 1, 0, 2, 1, 3, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    #     [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 2, 0, 0, 0, 1],
    #     [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    #     [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    #     [1, 3, 0, 2, 1, 1, 0, 0, 3, 0, 0, 1, 0, 1, 0, 1],
    #     [1, 3, 3, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 1, 0, 1],
    #     [1, 3, 1, 1, 0, 0, 0, 0, 0, 3, 0, 0, 3, 1, 0, 1],
    #     [1, 0, 0, 1, 1, 3, 0, 0, 0, 0, 0, 1, 3, 1, 0, 1],
    #     [1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 3, 1, 1, 1, 0, 1],
    #     [1, 0, 0, 2, 1, 1, 1, 1, 1, 3, 3, 3, 0, 0, 0, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    # ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0,11, 1, 1, 1, 4, 1],
        [1, 0, 0, 1, 2, 0, 2, 1, 0, 0, 1],
        [1, 0, 2, 1, 1, 0, 0, 2, 2, 0, 1],
        [1, 2, 0,11, 1, 1, 0, 0, 2, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
        [1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1],
        [1, 3, 3, 1, 1, 0, 3, 1, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
]

def draw_level(surface, level, tiles, camera_x, camera_y):
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

            screen_x = int((x * TILE_SIZE) - camera_x)
            screen_y = int((y * TILE_SIZE) - camera_y)

            draw_sprite(surface, sprite, screen_x, screen_y)

def check_ore_trap_chest_tiles(level, ores, traps, trigger_map, ore_sprite, chest_sprites, mimic_sprites):
    chests = []
    mimics = []
    
    for y, row in enumerate(level):
        for x, tile_id in enumerate(row):
            if tile_id == 2:
                ores.append(Ore(x * 16, y * 16, ore_sprite))
                level[y][x] = 0
            elif tile_id == 11:
                traps.append((x * 16, y * 16))
                trigger_map[y][x] = 11
                level[y][x] = 0
            elif tile_id == 3:
                if random.random() < 0.5:
                    chests.append(Chest(x * 16, y * 16, chest_sprites))
                else:
                    mimics.append(Mimic(x * 16, y * 16, mimic_sprites))
                level[y][x] = 0
            elif tile_id == 4:
                trigger_map[y][x] = 4
    return level, ores, traps, chests, mimics, trigger_map