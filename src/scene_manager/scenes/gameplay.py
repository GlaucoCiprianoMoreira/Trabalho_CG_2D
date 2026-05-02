import pygame
import random

from scene_manager.scene import Scene
from constants import load_tiles
from loader.LoadMap import draw_level, levels, check_ore_trap_chest_tiles
from loader.LoadMatrix import load_png_matrix, draw_sprite
from mechanics.Player import Player
from mechanics.Ore import Ore
from engine.Crystal import Crystal
from global_variables import inventory
from mechanics.Physics import check_trigger

class GameplayScene(Scene):
    def __init__(self, manager):
        self.manager = manager
        self.tiles = load_tiles()
        self.level = [row[:] for row in random.choice(levels)]

        self.GAME_W = 160
        self.GAME_H = 144

        player_sprites = {
            "up": [load_png_matrix("assets/player/player_tras1.png"), load_png_matrix("assets/player/player_tras2.png"),
                     load_png_matrix("assets/player/player_tras3.png"), load_png_matrix("assets/player/player_tras4.png")],
            "down": [load_png_matrix("assets/player/player_frente1.png"), load_png_matrix("assets/player/player_frente2.png"),
                    load_png_matrix("assets/player/player_frente3.png"), load_png_matrix("assets/player/player_frente4.png")],
            "left": [load_png_matrix("assets/player/player_esquerda1.png"), load_png_matrix("assets/player/player_esquerda2.png"),
                     load_png_matrix("assets/player/player_esquerda3.png"), load_png_matrix("assets/player/player_esquerda4.png")],
            "right": [load_png_matrix("assets/player/player_direita1.png"), load_png_matrix("assets/player/player_direita2.png"),
                      load_png_matrix("assets/player/player_direita3.png"), load_png_matrix("assets/player/player_direita4.png")],
        }
        self.ore_sprite, self.trap_sprite = load_png_matrix("assets/ore/ore-01.png"), load_png_matrix("assets/trap/trap.png")
        
        self.player = Player(16, 16, player_sprites)
        self.ores = []
        self.crystals = []
        self.traps = []
        #Matriz mapping dos triggers
        self.trigger_map = [[0 for _ in range(len(self.level[0]))] for _ in range(len(self.level))]
        self.level, self.ores, self.traps, self.trigger_map = check_ore_trap_chest_tiles(self.level, self.ores, self.traps, self.trigger_map, self.ore_sprite)
    
    def handle_event(self, event):
        pass

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys, self.level, self.ores)

        trigger_id = check_trigger(
            self.player.x, 
            self.player.y, 
            self.player.hitbox_w, 
            self.player.hitbox_h, 
            self.player.offset_x, 
            self.player.offset_y, 
            self.trigger_map
        )
        if trigger_id == 11:
            self.manager.go_to("dead") #DAVID: Trocar para a cena de morte quando ela for implementada

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
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        camera_x = (self.player.x + 8) - (self.GAME_W / 2)
        camera_y = (self.player.y + 8) - (self.GAME_H / 2)
        draw_level(screen, self.level, self.tiles, camera_x, camera_y)
        for trap_x, trap_y in self.traps:
            screen_x = int(trap_x - camera_x)
            screen_y = int(trap_y - camera_y)
            draw_sprite(screen, self.trap_sprite, screen_x, screen_y)
        for ore in self.ores:
            ore.draw(screen, camera_x, camera_y)
        for crystal in self.crystals:
            crystal.draw(screen, camera_x, camera_y)
        current_sprite = self.player.get_current_sprite()
        centro_x = int((self.GAME_W / 2) - 8) # Subtrai metade da largura do sprite para centralizar
        centro_y = int((self.GAME_H / 2) - 8) # Subtrai metade da altura do sprite para centralizar
        draw_sprite(screen, current_sprite, centro_x, centro_y)