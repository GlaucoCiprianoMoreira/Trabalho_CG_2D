import pygame
import game.audio.Audio_manager as audio_manager

from loader.LoadMatrix import load_png_matrix, draw_sprite

from config.Constants import LIGHTEST

from game.scene_manager.Scene import Scene

class CutsceneScene(Scene):
    def __init__(self, manager):
        self.manager = manager
        self.n_frame = 0
        self.time_frame = [4000, 2800, 4000, 2000, 2000, 2000, 6000, 2000, 8000]
        self.last_time = 0
        self.clock = pygame.time.Clock()
    
    def on_enter(self):
        audio_manager.play_music('space-ii-cutscene')
    
    def on_exit(self):
        pass
    
    def handle_event(self, event):
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
    
    def update(self, dt):
        self.roll_film(dt)

    def draw(self, screen):
        path = "assets/sprites/cutscene/frame-scene-0" + str(self.n_frame + 1) + ".png"
        matrix = load_png_matrix(path)
        draw_sprite(screen, matrix, 0, 0)