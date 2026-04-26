import pygame

from engine.HUD.text import draw_text
from engine.LoadMatrix import load_png_matrix, draw_sprite

from constants import LIGHTEST

from scene_manager.scene import Scene

class CutsceneScene(Scene):
    def __init__(self, manager):
        self.manager = manager
        self.n_frame = 1
        self._bg_cache = pygame.Surface((160, 144))
    
    def handle_event(self, event):
        #n_frame = 0
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                self.n_frame += 1
        if self.n_frame == 10:
            self.n_frame = 1
            self.manager.go_to("gameplay")
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        self._bg_cache.fill((0, 0, 0))

        path = "assets/cutscene/frame-scene-0" + str(self.n_frame) + ".png"
        matrix = load_png_matrix(path)
        draw_sprite(self._bg_cache, matrix, 0, 0)

        draw_text(self._bg_cache, "SPACE I ENTER", 80, 10, LIGHTEST, 1, mode="center")

        screen.blit(self._bg_cache, (0, 0))  # cola o fundo