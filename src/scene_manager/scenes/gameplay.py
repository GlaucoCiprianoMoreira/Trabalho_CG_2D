import pygame
import random

from scene_manager.scene import Scene
from constants import load_tiles
from loader.LoadMap import draw_level, levels
from loader.LoadMatrix import load_png_matrix, draw_sprite
from mechanics.Player import Player

class GameplayScene(Scene):
    def __init__(self, manager):
        self.manager = manager
        self.tiles = load_tiles()
        self.level = random.choice(levels)

        self.GAME_W = 160
        self.GAME_H = 144

        player_sprites = {
            "up": [load_png_matrix("assets/player/player_frente1.png"), load_png_matrix("assets/player/player_frente2.png"),
                    load_png_matrix("assets/player/player_frente3.png"), load_png_matrix("assets/player/player_frente4.png")],
            "down": [load_png_matrix("assets/player/player_frente1.png"), load_png_matrix("assets/player/player_frente2.png"),
                     load_png_matrix("assets/player/player_frente3.png"), load_png_matrix("assets/player/player_frente4.png")],
            "left": [load_png_matrix("assets/player/player_frente1.png"), load_png_matrix("assets/player/player_frente2.png"),
                     load_png_matrix("assets/player/player_frente3.png"), load_png_matrix("assets/player/player_frente4.png")],
            "right": [load_png_matrix("assets/player/player_frente1.png"), load_png_matrix("assets/player/player_frente2.png"),
                      load_png_matrix("assets/player/player_frente3.png"), load_png_matrix("assets/player/player_frente4.png")],
        }
        
        self.player = Player(100, 100, player_sprites)
    
    def handle_event(self, event):
        pass

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys)
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        camera_x = self.player.x - (self.GAME_W / 2)
        camera_y = self.player.y - (self.GAME_H / 2)
        draw_level(screen, self.level, self.tiles, camera_x, camera_y)
        current_sprite = self.player.get_current_sprite()
        centro_x = int((self.GAME_W / 2) - 8) # Subtrai metade da largura do sprite para centralizar
        centro_y = int((self.GAME_H / 2) - 8) # Subtrai metade da altura do sprite para centralizar
        draw_sprite(screen, current_sprite, centro_x, centro_y)