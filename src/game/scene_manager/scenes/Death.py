import pygame
import random
import game.audio.Audio_manager as audio_manager
import config.Variables as variables

from engine.geometry.Circle import fill_circle
from engine.HUD.Text import draw_text
from engine.geometry.Bresenham import bresenham
from engine.HUD.Button import draw_floodfill_button_alt
from engine.render.Clipping import cohen_sutherland_clip
from loader.LoadMatrix import load_png_matrix, draw_sprite

from game.scene_manager.Scene import Scene
from config.Constants import DARKEST, LIGHTEST, DARK, LIGHT


class DeathScene(Scene):
    def __init__(self, manager):
        self.manager = manager
        
        self.player_sprite = load_png_matrix("assets/sprites/player/player_frente1.png")
        
        self.state = "waiting"
        self.timer = 0.0
        
        self.light_radius = 24.0
        
        self.player_x = 72 
        self.player_y = 64 
        self.vy = 0.0
        self.gravity = 0.0
        
        self.n_button = 1

    def on_enter(self):
        audio_manager.stop_steps()
        audio_manager.stop_music()
        audio_manager.play_sfx('game_over')
        
        self.state = "waiting"
        self.timer = 0.03
        
        self.light_radius = 24.0 
        
        self.player_x = 72
        self.player_y = 64

        self.vy = -1000.0
        self.gravity = 16000.0
        
        self.n_button = 1

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state in ["waiting", "fading", "falling"]:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.state = "selection"
                    
            elif self.state == "selection":
                if event.key in (pygame.K_w, pygame.K_UP, pygame.K_s, pygame.K_DOWN):
                    self.n_button = 1 - self.n_button 
                    audio_manager.play_sfx('select', ui=True)

                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    audio_manager.play_sfx('click', ui=True)
                    if self.n_button == 1:
                        self.manager.go_to("gameplay")
                    else:
                        self.manager.go_to("menu")
                    variables.health = 3

    def update(self, dt):
        if self.state == "waiting":
            self.timer -= dt
            if self.timer <= 0:
                self.state = "fading"
                
        elif self.state == "fading":
            self.light_radius -= 180.0 * dt
            if self.light_radius <= 0:
                self.light_radius = 0
                self.state = "falling" 
                
        elif self.state == "falling":
            self.vy += self.gravity * dt
            self.player_y += self.vy * dt
            
            if self.player_y > 160:
                self.state = "selection"

    def draw(self, screen):
        if self.state == "waiting":
            draw_sprite(screen, self.player_sprite, int(self.player_x), int(self.player_y))
            
        elif self.state == "fading":
            screen.fill(DARKEST)
            if self.light_radius > 0:
                fill_circle(screen, 80, 72, int(self.light_radius), LIGHTEST)
            draw_sprite(screen, self.player_sprite, int(self.player_x), int(self.player_y))

        elif self.state == "falling":
            screen.fill(DARKEST)
            draw_sprite(screen, self.player_sprite, int(self.player_x), int(self.player_y))
            
        elif self.state == "selection":
            screen.fill(DARKEST)

            clip_xmin = 0
            clip_ymin = 0
            clip_xmax = 160
            clip_ymax = 22

            draw_text(screen, "VOCE MORREU", 80, 30, LIGHTEST, scale=1, mode="center")

            ore_text = f"${variables.inventory_ore} MINERIOS"
            draw_text(screen, ore_text, 80, 50, LIGHTEST, scale=1, mode="center")

            draw_floodfill_button_alt(screen, 95, 12, "JOGAR NOVAMENTE", 80, 90, self.n_button == 1)
            draw_floodfill_button_alt(screen, 115, 12, "VOLTAR PARA O MENU", 80, 110, self.n_button == 0)

            target_lines = [
                (0, 0, 80, 30),
                (160, 0, 80, 30)
            ]

            for (x1, y1, x2, y2) in target_lines:
                accept, cx1, cy1, cx2, cy2 = cohen_sutherland_clip(
                    x1, y1, x2, y2, clip_xmin, clip_ymin, clip_xmax, clip_ymax
                )
                if accept:
                    bresenham(screen, int(cx1), int(cy1), int(cx2), int(cy2), DARK)