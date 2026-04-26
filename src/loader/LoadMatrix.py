import pygame
import numpy as np
from engine.SetPixel import setPixel

def load_png_matrix(path):
    img = pygame.image.load(path).convert_alpha()
    w, h = img.get_width(), img.get_height()

    matrix = np.zeros((h, w, 4), dtype=np.uint8)

    for y in range(h):
        for x in range(w):
            matrix[y][x] = img.get_at((x, y))

    return matrix


def draw_sprite(surface, matrix, posX, posY):
    h, w, _ = matrix.shape

    surf_w = surface.get_width()
    surf_h = surface.get_height()

    # CLIPPING DE CAIXA: Define onde começar e onde terminar de ler a matriz (NÃO É O CLIPPING PASSADO EM AULA).
    start_x = max(0, -posX)
    start_y = max(0, -posY)
    
    # Se o sprite ultrapassar a largura da tela, paramos de ler antes do final dele.
    end_x = min(w, surf_w - posX)
    end_y = min(h, surf_h - posY)

    # Agora o loop só roda nos pixels que ESTÃO GARANTIDAMENTE DENTRO da tela!
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            color = matrix[y][x]

            if color[3] == 0:
                continue

            setPixel(surface, posX + x, posY + y, color)

