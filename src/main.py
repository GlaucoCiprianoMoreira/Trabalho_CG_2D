import sys
import pygame
import game.audio.Audio_manager as audio_manager

from game.scene_manager.Scene_manager import SceneManager
from game.scene_manager.scenes.Menu import MenuScene
from game.scene_manager.scenes.Gameplay import GameplayScene
from game.scene_manager.scenes.Cutscene import CutsceneScene
from game.scene_manager.scenes.Victory import VictoryScene
from game.scene_manager.scenes.Death import DeathScene

class Game:
    def __init__(self):
        pygame.init()
        audio_manager.init()
        pygame.display.set_caption("Cave Game")
        GAME_W, GAME_H, SCALE = 160, 144, 5
        self.WIN_W, self.WIN_H = GAME_W * SCALE, GAME_H * SCALE
        self.window = pygame.display.set_mode((self.WIN_W, self.WIN_H))
        self.window = pygame.display.set_mode((self.WIN_W, self.WIN_H))
        self.screen = pygame.Surface((GAME_W, GAME_H))

        self.manager = SceneManager()
        self.manager.register("menu",     MenuScene(self.manager))
        self.manager.register("cutscene", CutsceneScene(self.manager))
        self.manager.register("gameplay", GameplayScene(self.manager))
        self.manager.register("victory", VictoryScene(self.manager))
        self.manager.register("death", DeathScene(self.manager))

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
                audio_manager.handle_event(event)

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