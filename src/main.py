import sys
import pygame
from engine.SetPixel import setPixel
from loader.LoadMap import draw_level, level
from constants import load_tiles
from constants import PALETTE

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Diamond Rush")
        GAME_W, GAME_H, SCALE = 160, 144, 5
        self.WIN_W, self.WIN_H = GAME_W * SCALE, GAME_H * SCALE
        self.window = pygame.display.set_mode((self.WIN_W, self.WIN_H))
        self.screen = pygame.Surface((GAME_W, GAME_H))
        self.tiles = load_tiles()
    def run(self):
        running = True
        while running:
            scaled = pygame.transform.scale(self.screen, (self.WIN_W, self.WIN_H))
            self.window.blit(scaled, (0, 0))

            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    running = False
            self.screen.fill((0,0,0))   
            draw_level(self.screen, level, self.tiles)
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()