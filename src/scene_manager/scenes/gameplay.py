import pygame

from scene_manager.scene import Scene

class GameplayScene(Scene):
    def __init__(self, manager):
        self.manager = manager
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.manager.go_to("cutscene")
            if event.key == pygame.K_ESCAPE:
                quit()
    
    def draw(self, screen):
        pass