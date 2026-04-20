import sys
import pygame

from engine.SetPixel import setPixel
from engine.LoadMatrix import load_png_matrix, draw_sprite

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Diamond Rush")
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    running = False

                    
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()