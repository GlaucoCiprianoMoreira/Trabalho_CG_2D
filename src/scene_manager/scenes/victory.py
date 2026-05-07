import pygame
import math
import audio_manager

from engine.Circle import fill_circle
from engine.HUD.text import draw_text
from engine.HUD.button import draw_floodfill_button_alt_alt

from global_variables import variables

from scene_manager.scene import Scene
from constants import LIGHTEST, DARKEST, DARK

class VictoryScene(Scene):
    def __init__(self, manager):
        self.manager = manager
        
        self.state = "waiting"
        self.timer = 0.0
        
        # Variáveis da animação do círculo
        self.circle_radius = 0
        self.max_radius = 110
        
        # Variáveis dos Créditos
        self.credits_y = 150
        self.credits_speed = 250.0
        self.credits_text = [
            "PARABENS JOGADOR",
            "POR TER FINALIZADO O JOGO!",
            "",
            "OBRIGADO POR JOGAR",
            "ESPERO QUE TENHA",
            "SE DIVERTIDO!",
            "",
            "CRIADORES:",
            "DAVID",
            "GLAUCO",
            "GUILHERME"
        ]
        
        # Variáveis dos Botões
        self.n_button = 1
        self.clock = pygame.Clock()

    def on_enter(self):
        # Para a música da caverna e pode tocar um tema de vitória aqui
        audio_manager.stop_steps()
        audio_manager.stop_music()
        audio_manager.play_sfx('game_win')

        self.state = "waiting"
        self.timer = 0.01 # 0.01 segundo de delay inicial
        self.circle_radius = 0
        self.credits_y = 150
        self.n_button = 1

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "credits":
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    audio_manager.play_sfx('click', ui=True)
                    self.state = "selection"
            elif self.state == "selection":
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_w, pygame.K_UP, pygame.K_s, pygame.K_DOWN):
                        self.n_button = 1 - self.n_button # Alterna entre 0 e 1
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
                self.state = "transition"

        elif self.state == "transition":
            self.circle_radius += 320 * dt # Velocidade da expansão
            if self.circle_radius >= self.max_radius:
                self.circle_radius = self.max_radius
                self.state = "credits"

        elif self.state == "credits":
            audio_manager.play_music('kokiri-forest--the-end')
            self.credits_y -= self.credits_speed * dt
            if self.credits_y < -(len(self.credits_text) * 12):
                self.state = "selection"

    def draw(self, screen):
        if self.state in ["waiting", "transition"]:
            if self.circle_radius > 0:
                fill_circle(screen, 80, 72, int(self.circle_radius), LIGHTEST)
        else:
            screen.fill(LIGHTEST)

        if self.state == "credits":
            for i, line in enumerate(self.credits_text):
                y_pos = int(self.credits_y + (i * 12))
                if -10 < y_pos < 150:
                    draw_text(screen, line, 80, y_pos, DARKEST, scale=1, mode="center")

        if self.state == "selection":
            draw_text(screen, "FIM DE JOGO", 80, 30, DARK, scale=1, mode="center")

            ore_text = f"${variables.inventory_ore} MINERIOS"
            draw_text(screen, ore_text, 80, 50, DARKEST, scale=1, mode="center")
            
            draw_floodfill_button_alt_alt(screen, 80, 12, "JOGAR DE NOVO", 80, 90, self.n_button == 1)
            draw_floodfill_button_alt_alt(screen, 90, 12, "VOLTAR AO MENU", 80, 110, self.n_button == 0)