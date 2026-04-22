import pygame
import math

from engine.SetPixel import setPixel
from engine.Bresenham import bresenham
from engine.ScanlineFill import scanline_fill
from engine.Circle import fill_circle

from engine.HUD.text import draw_text
from engine.HUD.button import draw_floodfill_button

from global_variables import config

from constants import DARKEST, DARK, LIGHT, LIGHTEST

from scene_manager.scene import Scene

class MenuScene(Scene):
    def __init__(self, manager):
        self.manager = manager

        self.n_button = 2
        self.n_button_max = 2
        self.open_config = False

        self._bg_cache = pygame.Surface((160, 144))
        self.angulo = 0
        self.t = math.radians(self.angulo)
        self.clock = pygame.Clock()
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP) and self.n_button < 2:
                self.n_button += 1
            if event.key in (pygame.K_s, pygame.K_DOWN) and self.n_button > 0:
                self.n_button -= 1

            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.open_config:
                    if self.n_button == 2:
                        config.sound_on = not config.sound_on
                    elif self.n_button == 1:
                        config.music_on = not config.music_on
                    elif self.n_button == 0:
                        self.n_button = 1
                        self.open_config = False
                else:
                    if self.n_button == 2:
                        self.manager.go_to("cutscene")
                    elif self.n_button == 1:
                        self.open_config = True
                        self.n_button = 2
                    elif self.n_button == 0:
                        pygame.quit()
                        quit()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


    def _draw_gradient(self, surf, cx=80, cy=72, max_r=70):
        """
        Gradiente radial verdadeiro: cada pixel tem sua cor
        calculada individualmente pela distância ao centro.
        
        t = 0.0 → centro (mais claro)
        t = 1.0 → borda  (mais escuro)
        """
        PALETTE = [LIGHTEST, LIGHT, DARK, DARKEST]  # claro → escuro
        n = len(PALETTE) - 1                        # 3 intervalos entre 4 cores

        max_r = 70 + 2*math.sin(self.t)

        for y in range(144):
            for x in range(160):
                dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                t    = min(dist / max_r, 1.0)       # normaliza: 0=centro, 1+=borda
                idx  = round(t * n)                 # mapeia para o índice da paleta
                setPixel(surf, x, y, PALETTE[idx])

    def _draw_stalactites(self, surf):
        """Alguns triângulos no topo — decoração de caverna."""
        points = [
            [[20,   0],   [40,  50]],
            [[40,  50],   [60,   0]],
            [[70,   0],   [80,  30]],
            [[80,  30],   [90,   0]],
            [[100,  0],   [120, 40]],
            [[120, 40],   [140,  0]]
        ]
        for (x1, y1), (x2, y2) in points:
            bresenham(surf, x1, y1, x2, y2, DARKEST)
    
        points_to_scanline = [
            [(20, 0), (40, 50), (60, 0)],
            [(70, 0), (80, 30), (90, 0)],
            [(100, 0), (120, 40), (140, 0)]
        ]
        for pts in points_to_scanline:
            scanline_fill(surf, pts, DARKEST)

    def _draw_airbone_dust(self, surf, xc, yc, r, mode=1, dir=1):
        match mode:
            case 1:
                x = xc + math.cos(self.t * dir) * r * 2
                y = yc + math.sin(self.t * dir) * r
                fill_circle(surf, int(x), int(y), r, LIGHTEST)
            case 2:
                x = xc + math.sin(self.t * dir * 1 + 5) * 2 + math.cos(self.t * 1.5) * 3
                y = yc + math.cos(self.t * dir * 2 + 5) * 4
                fill_circle(surf, int(x), int(y), r, LIGHTEST)
            

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


    def draw(self, screen):
        # Fundo + decoração: renderiza UMA vez e guarda em cache
        #if self._bg_cache is None:

        self.dt = self.clock.tick(60) / 1000
        self.t += self.dt
        self.angulo += self.dt
        self.angulo %= (2 * math.pi)

        self._draw_gradient(self._bg_cache)
        self._draw_stalactites(self._bg_cache)

        self._draw_airbone_dust(self._bg_cache, 30, 120, 4, mode=1)
        self._draw_airbone_dust(self._bg_cache, 140, 40, 5, mode=2)
        self._draw_airbone_dust(self._bg_cache, 115, 80, 2, mode=1, dir=-1)
        self._draw_airbone_dust(self._bg_cache, 40, 65, 6, mode=2, dir=-1)
        # Título
        draw_text(self._bg_cache, "cave game", 80, 5, LIGHTEST, scale=2, mode="center")

        screen.blit(self._bg_cache, (0, 0))  # cola o fundo

        # Botões: redesenhados todo frame (estado de seleção muda)
        if self.open_config:
            if config.sound_on:
                sound_status = "SOUND ON"
            else:
                sound_status = "SOUND OFF"
            if config.music_on:
                music_status = "MUSIC ON"
            else:
                music_status = "MUSIC OFF"
            draw_floodfill_button(screen, 60, 10, sound_status, 80, 85,  self.n_button == 2)
            draw_floodfill_button(screen, 60, 10, music_status, 80, 100,  self.n_button == 1)
            draw_floodfill_button(screen, 60, 10, "BACK", 80, 115,  self.n_button == 0)
        else:
            draw_floodfill_button(screen, 40, 10, "PLAY", 80, 85,  self.n_button == 2)
            draw_floodfill_button(screen, 40, 10, "CONFIG", 80, 100,  self.n_button == 1)
            draw_floodfill_button(screen, 40, 10, "QUIT", 80,  115, self.n_button == 0)