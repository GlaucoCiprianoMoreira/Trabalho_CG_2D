import pygame
import audio_manager

from engine.Circle import fill_circle
from engine.HUD.text import draw_text
from engine.Bresenham import bresenham
from engine.HUD.button import draw_floodfill_button_alt
from loader.LoadMatrix import load_png_matrix, draw_sprite

from global_variables import variables

from scene_manager.scene import Scene
from constants import DARKEST, LIGHTEST, DARK, LIGHT


class DeathScene(Scene):
    def __init__(self, manager):
        self.manager = manager
        
        # Carrega o sprite do jogador olhando para frente
        self.player_sprite = load_png_matrix("assets/sprites/player/player_frente1.png")
        
        # Inicia no novo estado de espera
        self.state = "waiting"
        self.timer = 0.0
        
        self.light_radius = 24.0 # Começa no tamanho original da lamparina
        
        self.player_x = 72 
        self.player_y = 64 
        self.vy = 0.0
        self.gravity = 0.0
        
        self.n_button = 1

    def on_enter(self):
        audio_manager.stop_steps()
        
        # Reseta as variáveis de animação
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

    def update(self, dt):
        if self.state == "waiting":
            self.timer -= dt
            if self.timer <= 0:
                self.state = "fading"
                
        elif self.state == "fading":
            self.light_radius -= 180.0 * dt # Velocidade que a luz apaga
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
            draw_text(screen, "VOCE MORREU", 80, 30, LIGHTEST, scale=1, mode="center")

            ore_text = f"${variables.inventory_ore} MINERIOS"
            draw_text(screen, ore_text, 80, 50, LIGHTEST, scale=1, mode="center")

            draw_floodfill_button_alt(screen, 95, 12, "JOGAR NOVAMENTE", 80, 90, self.n_button == 1)
            draw_floodfill_button_alt(screen, 115, 12, "VOLTAR PARA O MENU", 80, 110, self.n_button == 0)