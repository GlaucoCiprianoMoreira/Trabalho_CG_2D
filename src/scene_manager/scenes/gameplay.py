import pygame
import random

import audio_manager
from scene_manager.scene import Scene
from constants import load_tiles
from loader.LoadMap import draw_level, levels
from loader.LoadMatrix import load_png_matrix, draw_sprite
from mechanics.Player import Player
from mechanics.Ore import Ore
from engine.Crystal import Crystal
from global_variables import inventory

class GameplayScene(Scene):
    def __init__(self, manager):
        self.manager = manager
        self.tiles = load_tiles()
        self.level = [row[:] for row in random.choice(levels)]

        self.GAME_W = 160
        self.GAME_H = 144

        player_sprites = {
            "up":    [load_png_matrix("assets/sprites/player/player_tras1.png"),     load_png_matrix("assets/sprites/player/player_tras2.png"),
                      load_png_matrix("assets/sprites/player/player_tras3.png"),     load_png_matrix("assets/sprites/player/player_tras4.png")],
            "down":  [load_png_matrix("assets/sprites/player/player_frente1.png"),   load_png_matrix("assets/sprites/player/player_frente2.png"),
                      load_png_matrix("assets/sprites/player/player_frente3.png"),   load_png_matrix("assets/sprites/player/player_frente4.png")],
            "left":  [load_png_matrix("assets/sprites/player/player_esquerda1.png"), load_png_matrix("assets/sprites/player/player_esquerda2.png"),
                      load_png_matrix("assets/sprites/player/player_esquerda3.png"), load_png_matrix("assets/sprites/player/player_esquerda4.png")],
            "right": [load_png_matrix("assets/sprites/player/player_direita1.png"),  load_png_matrix("assets/sprites/player/player_direita2.png"),
                      load_png_matrix("assets/sprites/player/player_direita3.png"),  load_png_matrix("assets/sprites/player/player_direita4.png")],
        }
        self.ore_sprite = load_png_matrix("assets/sprites/ore/ore-01.png")
        
        self.player = Player(16, 16, player_sprites)
        self.ores = []
        self.crystals = []
        for y, row in enumerate(self.level):
            for x, tile_id in enumerate(row):
                if tile_id == 2:
                    self.ores.append(Ore(x * 16, y * 16, self.ore_sprite))
                    self.level[y][x] = 0
    
    def on_enter(self):
        audio_manager.play_music_queue(['moss-lit-caverns', 'quest', 'resonance'])
    
    def on_exit(self):
        pass
    
    def handle_event(self, event):
        pass

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys, self.level, self.ores)

        # --- LÓGICA DE MINERAÇÃO ---
        if self.player.is_mining:
            self.player.is_mining = False # Consome o input
            fx, fy = self.player.get_facing_point()
            
            for ore in self.ores:
                if (ore.x <= fx <= ore.x + 16) and (ore.y <= fy <= ore.y + 16):
                    ore.hit()
                    if ore.health <= 0:
                        self.ores.remove(ore)
                        self.crystals.append(Crystal(ore.x, ore.y+2))
                    break
        for ore in self.ores:
            ore.update(dt)
        for crystal in self.crystals[:]:
            crystal.update(dt)
            if crystal.check_collection(self.player.x, self.player.y):
                inventory.inventory_ore += 1
                self.crystals.remove(crystal)
                audio_manager.play_sfx('colect')
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        camera_x = (self.player.x + 8) - (self.GAME_W / 2)
        camera_y = (self.player.y + 8) - (self.GAME_H / 2)
        draw_level(screen, self.level, self.tiles, camera_x, camera_y)
        for ore in self.ores:
            ore.draw(screen, camera_x, camera_y)
        for crystal in self.crystals:
            crystal.draw(screen, camera_x, camera_y)
        current_sprite = self.player.get_current_sprite()
        centro_x = int((self.GAME_W / 2) - 8) # Subtrai metade da largura do sprite para centralizar
        centro_y = int((self.GAME_H / 2) - 8) # Subtrai metade da altura do sprite para centralizar
        draw_sprite(screen, current_sprite, centro_x, centro_y)