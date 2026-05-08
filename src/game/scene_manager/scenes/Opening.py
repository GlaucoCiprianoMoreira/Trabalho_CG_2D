import pygame
import math

from engine.geometry.Bresenham import bresenham
from engine.render.ScanlineFill import scanline_fill

from engine.render.SetPixel   import setPixel
from engine.geometry.Ellipse  import midpointEllipse

from config.Constants import DARKEST, DARK, LIGHT, LIGHTEST
from game.scene_manager.Scene import Scene


class OpeningScene(Scene):
    """
    Cena de abertura animada exibida uma única vez antes do menu principal.

    Fluxo em duas fases:
      Fase 1 — Elipse DARKEST nasce do centro, gira e cresce até cobrir
               a tela inteira (fundo vai de LIGHTEST para totalmente DARKEST).
               O contorno da elipse é desenhado com midpointEllipse().

      Fase 2 — Com a tela toda DARKEST, o gradiente radial do menu cresce
               do centro (raio 0) até o tamanho padrão e então a cena
               transiciona automaticamente para o menu.

    Qualquer tecla pula a abertura diretamente para o menu.
    """

    # ── Configurações de animação ─────────────────────────────────────────────
    _CX, _CY       = 80, 72       # centro da tela (160×144)
    _GROW_SPEED    = 34.0         # px/s — velocidade de crescimento dos raios
    _ROT_SPEED     = 1.9          # rad/s — velocidade de rotação da elipse
    _RY_RATIO      = 0.68         # ry cresce mais devagar → elipse visivelmente achatada
    _COVER_R       = 128.0        # raio a partir do qual a tela está completamente coberta
    _GRAD_MAX_R    = 70.0         # raio máximo do gradiente (igual ao do menu)
    _GRAD_SPEED    = 58.0         # px/s — velocidade de crescimento do gradiente
    _GRAD_EXTRA    = 18.0         # margem extra após _GRAD_MAX_R para garantir cobertura total

    # Paleta de cores do gradiente (mesma ordem do menu)
    _PALETTE = [LIGHTEST, LIGHT, DARK, DARKEST]

    # ─────────────────────────────────────────────────────────────────────────

    def __init__(self, manager):
        self.manager = manager
        self.clock   = pygame.Clock()
        self._reset()

    def _reset(self):
        """Reinicia todos os estados da animação."""
        self.phase   = 1
        self.rx      = 1.0          # semi-eixo horizontal (cresce com o tempo)
        self.ry      = 0.68         # semi-eixo vertical   (cresce mais devagar)
        self.angle   = 0.0          # ângulo atual de rotação (radianos)
        self.grad_r  = 0.0          # raio atual do gradiente (fase 2)

    # ── Ciclo de vida da cena ─────────────────────────────────────────────────

    def on_enter(self):
        self._reset()

    def on_exit(self):
        pass

    def handle_event(self, event):
        """Qualquer tecla pressionada pula a abertura."""
        if event.type == pygame.KEYDOWN:
            self.manager.go_to("menu")

    # ── Renderização por fase ─────────────────────────────────────────────────

    def _draw_phase1(self, screen, dt):
        """
        Fase 1: elipse DARKEST rotacionada cresce do centro até cobrir toda a tela.

        Para cada pixel da tela verifica se está dentro da elipse rotacionada
        usando a equação canônica após aplicar a rotação inversa:
            (x'²/rx² + y'²/ry²) ≤ 1
        onde (x', y') são as coordenadas do pixel no referencial da elipse.

        O contorno da elipse atual é desenhado com midpointEllipse() (eixo-alinhado)
        em LIGHTEST, criando uma borda luminosa sobre o preenchimento escuro.
        """
        # Atualiza os parâmetros de animação
        self.rx    = min(self.rx  + dt * self._GROW_SPEED,               self._COVER_R)
        self.ry    = min(self.ry  + dt * self._GROW_SPEED * self._RY_RATIO, self._COVER_R)
        self.angle = (self.angle  + dt * self._ROT_SPEED) % (2 * math.pi)

        # Pré-calcula para o loop de pixels
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)
        rx2   = self.rx * self.rx
        ry2   = self.ry * self.ry

        # Pinta cada pixel conforme esteja dentro ou fora da elipse rotacionada
        for y in range(144):
            for x in range(160):
                dx =  x - self._CX
                dy =  y - self._CY
                # Coordenadas no referencial local da elipse (rotação inversa)
                xr =  dx * cos_a + dy * sin_a
                yr = -dx * sin_a + dy * cos_a
                if (xr * xr) / rx2 + (yr * yr) / ry2 <= 1.0:
                    setPixel(screen, x, y, DARKEST)
                else:
                    setPixel(screen, x, y, LIGHTEST)

        # Contorno da elipse desenhado com o algoritmo de ponto médio
        # (eixo-alinhado sobre o preenchimento rotacionado → borda luminosa)
        midpointEllipse(screen, self._CX, self._CY,
                        int(self.rx), int(self.ry), LIGHTEST)

        # Verifica se a elipse já cobre a tela inteira
        if self.rx >= self._COVER_R and self.ry >= self._COVER_R:
            self.phase = 2
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

    def _draw_phase2(self, screen, dt):
        """
        Fase 2: gradiente radial (idêntico ao do menu) cresce do centro
        sobre um fundo totalmente DARKEST, revelando o visual do menu.
        Ao atingir o tamanho máximo, transiciona automaticamente para o menu.
        """
        n = len(self._PALETTE) - 1

        self.grad_r  = min(self.grad_r + dt * self._GRAD_SPEED,
                           self._GRAD_MAX_R + self._GRAD_EXTRA)
        clip_r2 = self.grad_r * self.grad_r

        for y in range(144):
            for x in range(160):
                dx = x - self._CX
                dy = y - self._CY
                d2 = dx * dx + dy * dy

                if d2 <= clip_r2:
                    # Dentro do raio de corte: aplica o gradiente do menu
                    dist = math.sqrt(d2)
                    t    = min(dist / self._GRAD_MAX_R, 1.0)
                    idx  = round(t * n)
                    setPixel(screen, x, y, self._PALETTE[idx])
                else:
                    # Fora do raio: mantém o fundo escuro
                    setPixel(screen, x, y, DARKEST)

        if self.grad_r >= self._GRAD_MAX_R + self._GRAD_EXTRA:
            self.manager.go_to("menu")

    # ── Loop principal ────────────────────────────────────────────────────────

    def draw(self, screen):
        dt = self.clock.tick(60) / 1000   # delta time em segundos

        if self.phase == 1:
            self._draw_phase1(screen, dt)
        elif self.phase == 2:
            self._draw_phase2(screen, dt)
            self._draw_stalactites(screen)