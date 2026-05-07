import pygame
import random

import audio_manager
from scene_manager.scene import Scene
from constants import load_tiles
from loader.LoadMap import draw_level, levels, check_ore_trap_chest_tiles
from loader.LoadMatrix import load_png_matrix, draw_sprite
from mechanics.Player import Player
from mechanics.Viewport import PlayerViewport
from mechanics.Ore import Ore
from engine.Crystal import Crystal
from global_variables import variables
from mechanics.Physics import check_trigger
from engine.HUD.text import draw_text
from engine.HUD.PopupManager import PopupManager
from constants import LIGHTEST
from mechanics.Darkness import apply_darkness

class GameplayScene(Scene):
    def __init__(self, manager):
        self.manager = manager
        self.tiles = load_tiles()

        self.GAME_W = 160
        self.GAME_H = 144

        self.player_sprites = {
            "up":    [load_png_matrix("assets/sprites/player/player_tras1.png"),     load_png_matrix("assets/sprites/player/player_tras2.png"),
                      load_png_matrix("assets/sprites/player/player_tras3.png"),     load_png_matrix("assets/sprites/player/player_tras4.png")],
            "down":  [load_png_matrix("assets/sprites/player/player_frente1.png"),   load_png_matrix("assets/sprites/player/player_frente2.png"),
                      load_png_matrix("assets/sprites/player/player_frente3.png"),   load_png_matrix("assets/sprites/player/player_frente4.png")],
            "left":  [load_png_matrix("assets/sprites/player/player_esquerda1.png"), load_png_matrix("assets/sprites/player/player_esquerda2.png"),
                      load_png_matrix("assets/sprites/player/player_esquerda3.png"), load_png_matrix("assets/sprites/player/player_esquerda4.png")],
            "right": [load_png_matrix("assets/sprites/player/player_direita1.png"),  load_png_matrix("assets/sprites/player/player_direita2.png"),
                      load_png_matrix("assets/sprites/player/player_direita3.png"),  load_png_matrix("assets/sprites/player/player_direita4.png")],
        }

        self.player_viewport = PlayerViewport(size=24, margin=4, screen_w=self.GAME_W)
        self.ore_sprite = load_png_matrix("assets/sprites/ore/ore-01.png")
        self.trap_sprite = load_png_matrix("assets/sprites/trap/trap.png")
        self.chest_sprites = [load_png_matrix(f"assets/sprites/chest/chest-0{i}.png") for i in range(1, 5)]
        self.mimic_sprites = [load_png_matrix(f"assets/sprites/mimic/mimic{i}.png") for i in range(1, 17)]

        self.popup = PopupManager()
    
    def on_enter(self):
        self.level = [row[:] for row in random.choice(levels)]
        variables.inventory_ore = 0
        self.player = Player(16, 16, self.player_sprites)
        
        self.ores = []
        self.crystals = []
        self.traps = []
        self.chests = []
        self.mimics = []
        audio_manager.play_music_queue(['moss-lit-caverns', 'quest', 'resonance'])
        #Matriz mapping dos triggers
        self.trigger_map = [[0 for _ in range(len(self.level[0]))] for _ in range(len(self.level))]
        self.level, self.ores, self.traps, self.chests, self.mimics, self.trigger_map = check_ore_trap_chest_tiles(
            self.level, self.ores, self.traps, self.trigger_map, self.ore_sprite, self.chest_sprites, self.mimic_sprites
        )
        self.popup.state = "idle"
        self.popup.alpha = 0.0
    
    def on_exit(self):
        pass
    
   
    def handle_event(self, event):
        pass

    def load_HUD(self, screen):
        draw_text(screen, '<' + str(variables.health), 3, 3, LIGHTEST, 2)
        draw_text(screen, '$' + str(variables.inventory_ore), 33, 3, LIGHTEST, 2)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        solid_entities = self.ores + self.chests + self.mimics
        self.player.update(dt, keys, self.level, solid_entities)
        if variables.health <= 0:
            self.manager.go_to("death")

        trigger_id = check_trigger(
            self.player.x, 
            self.player.y, 
            self.player.hitbox_w, 
            self.player.hitbox_h, 
            self.player.offset_x, 
            self.player.offset_y, 
            self.trigger_map
        )
        if trigger_id == 11 and self.player.invincible_timer <= 0:
            variables.health = 0

        elif trigger_id == 4:
            self.manager.go_to("victory")

        # --- LÓGICA DE INTERAÇÃO ---
        if self.player.is_mining:
            self.player.is_mining = False # Consome o input
            fx, fy = self.player.get_facing_point()
            #Checa Ores
            for ore in self.ores:
                if (ore.x <= fx <= ore.x + 16) and (ore.y <= fy <= ore.y + 16):
                    ore.hit()
                    if ore.health <= 0:
                        self.ores.remove(ore)
                        self.crystals.append(Crystal(ore.x, ore.y+4))
                    break
            # Checa Baús
            for chest in self.chests:
                if (chest.x <= fx <= chest.x + 16) and (chest.y <= fy <= chest.y + 16):
                    chest.interact()
                    audio_manager.play_sfx('chest_open')
            # Checa Mimics
            for mimic in self.mimics:
                if (mimic.x <= fx <= mimic.x + 16) and (mimic.y <= fy <= mimic.y + 16):
                    mimic.interact()
                    audio_manager.play_sfx('chest_mimic')
        
        # --- UPDATES DAS ENTIDADES DINÂMICAS ---
        for ore in self.ores:
            ore.update(dt)
        for crystal in self.crystals[:]:
            crystal.update(dt)
            if crystal.check_collection(self.player.x, self.player.y):
                single_crystal = 3
                variables.inventory_ore += single_crystal
                self.popup.trigger(f"PEGOU {single_crystal} MINERIOS!")
                audio_manager.play_sfx('colect')
                self.crystals.remove(crystal)
        for chest in self.chests:
            old_state = chest.state
            chest.update(dt)
            # Acabou de abrir neste frame exato?
            if old_state == "opening" and chest.state == "opened":
                ganho = random.randint(1, 5)
                variables.inventory_ore += ganho
                audio_manager.play_sfx('colect')
                self.popup.trigger(f"PEGOU {ganho} MINERIOS!")
        for mimic in self.mimics:
            old_state = mimic.state
            mimic.update(dt)
            # Acabou de atacar neste frame exato?
            if old_state == "attacking" and mimic.state == "revealed":
                self.player.take_damage()
        self.popup.update(dt)
    

    def draw(self, screen):
        screen.fill((0, 0, 0))
        camera_x = (self.player.x + 8) - (self.GAME_W / 2)
        camera_y = (self.player.y + 6) - (self.GAME_H / 2)
        draw_level(screen, self.level, self.tiles, camera_x, camera_y)

        current_sprite = self.player.get_current_sprite()
        centro_x = int((self.GAME_W / 2) - 8)
        centro_y = int((self.GAME_H / 2) - 8)

        for trap_x, trap_y in self.traps:
            screen_x = int(trap_x - camera_x)
            screen_y = int(trap_y - camera_y)
            draw_sprite(screen, self.trap_sprite, screen_x, screen_y)
        for chest in self.chests:
            chest.draw(screen, camera_x, camera_y)
        for mimic in self.mimics:
            mimic.draw(screen, camera_x, camera_y)
        for ore in self.ores:
            ore.draw(screen, camera_x, camera_y)
        for crystal in self.crystals:
            crystal.draw(screen, camera_x, camera_y)
        if self.player.is_visible:
            current_sprite = self.player.get_current_sprite()
            centro_x = int((self.GAME_W / 2) - 8) # Subtrai metade da largura do sprite para centralizar
            centro_y = int((self.GAME_H / 2) - 8) # Subtrai metade da altura do sprite para centralizar
            draw_sprite(screen, current_sprite, centro_x, centro_y)
        apply_darkness(screen)
        self.player_viewport.draw(screen, current_sprite)
        self.load_HUD(screen)
        text_x = self.GAME_W / 2
        text_y = self.GAME_H - 20 
        self.popup.draw(screen, text_x, text_y, LIGHTEST)
