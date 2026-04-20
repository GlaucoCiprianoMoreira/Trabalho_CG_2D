import sys
import pygame
from engine.SetPixel import setPixel
from loader.LoadMap import draw_level, level
from constants import load_tiles
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Diamond Rush")
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.tiles = load_tiles()
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    running = False
            self.screen.fill((0,0,0))   
            draw_level(self.screen, level, self.tiles)
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()