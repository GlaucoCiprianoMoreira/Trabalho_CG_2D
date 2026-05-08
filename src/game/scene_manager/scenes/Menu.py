import pygame
import math
import game.audio.Audio_manager as audio_manager

from engine.render.SetPixel import setPixel
from engine.geometry.Bresenham import bresenham
from engine.render.ScanlineFill import scanline_fill
from engine.geometry.Circle import fill_circle

from engine.HUD.Text import draw_text
from engine.HUD.Button import draw_floodfill_button

import config.Variables as variables

from config.Constants import DARKEST, DARK, LIGHT, LIGHTEST

from game.scene_manager.Scene import Scene

class MenuScene(Scene):
    def __init__(self, manager):
        self.manager = manager

        self.n_button = 2
        self.n_button_max = 2
        self.open_config = False

        self.angulo = 0
        self.t = math.radians(self.angulo)
        self.clock = pygame.Clock()

    def on_enter(self):
        audio_manager.play_music('hide-menu')
    
    def on_exit(self):
        pass
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP) and self.n_button < 2:
                self.n_button += 1
                audio_manager.play_sfx('select', ui=True)
            if event.key in (pygame.K_s, pygame.K_DOWN) and self.n_button > 0:
                self.n_button -= 1
                audio_manager.play_sfx('select', ui=True)

            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                audio_manager.play_sfx('click', ui=True)
                if self.n_button == 2:
                    if not self.open_config:
                        self.manager.go_to("cutscene")
                    else:
                        audio_manager.set_sound_on(not variables.sound_on)

                elif self.n_button == 1:
                    if not self.open_config:
                        self.open_config = True
                        self.n_button = 0
                    else:
                        audio_manager.set_music_on(not variables.music_on)

                elif self.n_button == 0:
                    if not self.open_config:
                        pygame.quit()
                        quit()
                    else:
                        self.n_button = 1
                        self.open_config = False

    def _draw_gradient(self, surf, cx=80, cy=72, max_r=70):
        PALETTE = [LIGHTEST, LIGHT, DARK, DARKEST]
        n = len(PALETTE) - 1

        max_r = 70 + 2*math.sin(self.t)

        for y in range(144):
            for x in range(160):
                dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                t    = min(dist / max_r, 1.0)
                idx  = round(t * n)
                setPixel(surf, x, y, PALETTE[idx])

    def _draw_stalactites(self, surf):
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

    def draw(self, screen):
        self.dt = self.clock.tick(60) / 1000
        self.t += self.dt
        self.angulo += self.dt
        self.angulo %= (2 * math.pi)

        self._draw_gradient(screen)
        self._draw_stalactites(screen)

        self._draw_airbone_dust(screen, 30, 120, 4, mode=1)
        self._draw_airbone_dust(screen, 140, 40, 5, mode=2)
        self._draw_airbone_dust(screen, 115, 80, 2, mode=1, dir=-1)
        self._draw_airbone_dust(screen, 40, 65, 6, mode=2, dir=-1)
        
        draw_text(screen, "cave game", 80, 5, LIGHTEST, scale=2, mode="center")

        if self.open_config:
            if variables.sound_on:
                sound_status = "EFEITO ON"
            else:
                sound_status = "EFEITO OFF"
            if variables.music_on:
                music_status = "MUSICA ON"
            else:
                music_status = "MUSICA OFF"
            draw_floodfill_button(screen, 70, 10, sound_status, 80, 85,  self.n_button == 2)
            draw_floodfill_button(screen, 70, 10, music_status, 80, 100,  self.n_button == 1)
            draw_floodfill_button(screen, 70, 10, "VOLTAR", 80, 115,  self.n_button == 0)
        else:
            draw_floodfill_button(screen, 40, 10, "JOGAR", 80, 85,  self.n_button == 2)
            draw_floodfill_button(screen, 40, 10, "CONFIG", 80, 100,  self.n_button == 1)
            draw_floodfill_button(screen, 40, 10, "SAIR", 80,  115, self.n_button == 0)