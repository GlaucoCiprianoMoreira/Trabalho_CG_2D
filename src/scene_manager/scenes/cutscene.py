import pygame

from engine.HUD.text import draw_text
from engine.LoadMatrix import load_png_matrix, draw_sprite

from constants import LIGHTEST

from scene_manager.scene import Scene

class CutsceneScene(Scene):
    def __init__(self, manager):
        self.manager = manager
        self.n_frame = 0
        self.time_frame = [2000, 1400, 2000, 1000, 1000, 1000, 3000, 1000, 4000]
        self.last_time = 0
        self.clock = pygame.time.Clock()

    def handle_event(self, event):
        #n_frame = 0
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN) and self.n_frame > 0:
                self.n_frame = 0
                self.manager.go_to("gameplay")

    def roll_film(self, dt):
        self.last_time += (dt * 100000) / 2
        
        if self.last_time >= self.time_frame[self.n_frame]:
            if self.n_frame < len(self.time_frame) - 1:
                self.n_frame += 1
                self.last_time = 0
            else:
                self.n_frame = 0
                self.manager.go_to("gameplay")

        self.clock.tick(60)
    
    def update(self, dt):
        self.roll_film(dt)

    def draw(self, screen):
        path = "assets/cutscene/frame-scene-0" + str(self.n_frame + 1) + ".png"
        matrix = load_png_matrix(path)
        draw_sprite(screen, matrix, 0, 0)