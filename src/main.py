import sys
import pygame
import audio_manager

from scene_manager.scene_manager import SceneManager
from scene_manager.scenes.menu import MenuScene
from scene_manager.scenes.gameplay import GameplayScene
from scene_manager.scenes.cutscene import CutsceneScene

class Game:
    def __init__(self):
        pygame.init()
        audio_manager.init()
        pygame.display.set_caption("Diamond Rush")
        GAME_W, GAME_H, SCALE = 160, 144, 5
        self.WIN_W, self.WIN_H = GAME_W * SCALE, GAME_H * SCALE
        self.window = pygame.display.set_mode((self.WIN_W, self.WIN_H))
        self.window = pygame.display.set_mode((self.WIN_W, self.WIN_H))
        self.screen = pygame.Surface((GAME_W, GAME_H))

        self.manager = SceneManager()
        self.manager.register("menu",     MenuScene(self.manager))
        self.manager.register("cutscene", CutsceneScene(self.manager))
        self.manager.register("gameplay", GameplayScene(self.manager))

        self.manager.go_to("menu")

        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 10000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.manager.handle_event(event)

            self.manager.update(dt)
            self.manager.draw(self.screen)
            self.window.blit
            scaled = pygame.transform.scale(self.screen, (self.WIN_W, self.WIN_H))
            self.window.blit(scaled, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()