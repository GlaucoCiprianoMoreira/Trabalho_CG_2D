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
        self.rock = load_png_matrix("assets/rock/rock_01.png")
        self.player = load_png_matrix("assets/player/player_01.png")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
               for i in range(0, self.width, 16):
                   draw_sprite(self.screen, self.rock, i, 300)
               if event.type == pygame.QUIT:
                    running = False

                    
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()