import pygame
from constants import DARKEST, LIGHTEST


class PlayerViewport:
    def __init__(self, size: int = 20, margin: int = 4, screen_w: int = 160, padding: int = 3):
        """
        size    : lado do quadrado da viewport em pixels
        margin  : distância da borda da tela
        screen_w: largura da superfície de jogo
        padding : espaço interno entre a borda da viewport e o sprite
        """
        self.size = size
        self.margin = margin
        self.screen_w = screen_w
        self.padding = padding

        self.x = screen_w - size - margin
        self.y = margin

        self.color_bg     = (0, 0, 0)
        self.color_border = LIGHTEST

    def draw(self, screen: pygame.Surface, player_sprite) -> None:
        size = self.size
        ox = self.x  # offset X da viewport na tela
        oy = self.y  # offset Y da viewport na tela

        # --- fundo: preenche o quadrado pixel a pixel ---
        bg_rect = pygame.Rect(ox, oy, size, size)
        pygame.draw.rect(screen, self.color_bg, bg_rect)

        sprite_draw_size = size - self.padding * 2

        if sprite_draw_size > 0 and player_sprite is not None:
            rows = len(player_sprite)
            cols = len(player_sprite[0]) if rows > 0 else 0

            if rows > 0 and cols > 0:
                pixel_w = sprite_draw_size / cols
                pixel_h = sprite_draw_size / rows

                for row_i, row in enumerate(player_sprite):
                    for col_i, color in enumerate(row):
                        if color is None:
                            continue
                        px = ox + self.padding + round(col_i * pixel_w)
                        py = oy + self.padding + round(row_i * pixel_h)
                        pw = max(1, round((col_i + 1) * pixel_w) - round(col_i * pixel_w))
                        ph = max(1, round((row_i + 1) * pixel_h) - round(row_i * pixel_h))
                        pygame.draw.rect(screen, color, (px, py, pw, ph))

        border_rect = pygame.Rect(ox - 1, oy - 1, size + 2, size + 2)
        pygame.draw.rect(screen, self.color_border, border_rect, 1)