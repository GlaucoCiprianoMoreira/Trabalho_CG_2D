from config.Constants import DARKEST, DARK, LIGHT, LIGHTEST
from engine.geometry.Bresenham import bresenham
from engine.fill.FloodFill import floodFill
from engine.render.ScanlineFill import scanline_fill

from engine.HUD.Text import draw_text

def draw_floodfill_button(surf, width, height, label,x, y, selected):
    """Botão centralizado. Se selecionado, coloca '>' na frente."""
    color     = LIGHT if selected else DARKEST
    scale     = 1
    
    points_button = [
        [[x + (width // 2), y + (height // 2)], [x - (width // 2), y + (height // 2)]],
        [[x - (width // 2), y + (height // 2)], [x - (width // 2), y - (height // 2)]],
        [[x - (width // 2), y - (height // 2)], [x + (width // 2), y - (height // 2)]],
        [[x + (width // 2), y - (height // 2)], [x + (width // 2), y + (height // 2)]],
    ]
    for (x0, y0), (x1, y1) in points_button:
        bresenham(surf, x0, y0, x1, y1, DARKEST)
    
    floodFill(surf, x, y, LIGHTEST, DARKEST)

    draw_text(surf, label, x, y-2, color, scale=scale, mode="center")

def draw_floodfill_button_alt(surf, width, height, label,x, y, selected):
    """Botão centralizado. Se selecionado, coloca '>' na frente."""
    color     = LIGHT if selected else DARKEST
    scale     = 1

    points_button = [
        [[x + (width // 2), y + (height // 2)], [x - (width // 2), y + (height // 2)]],
        [[x - (width // 2), y + (height // 2)], [x - (width // 2), y - (height // 2)]],
        [[x - (width // 2), y - (height // 2)], [x + (width // 2), y - (height // 2)]],
        [[x + (width // 2), y - (height // 2)], [x + (width // 2), y + (height // 2)]],
    ]
    for (x0, y0), (x1, y1) in points_button:
        bresenham(surf, x0, y0, x1, y1, DARK)
    
    floodFill(surf, x, y, LIGHTEST, DARK)

    draw_text(surf, label, x, y-2, color, scale=scale, mode="center")

def draw_floodfill_button_alt_alt(surf, width, height, label,x, y, selected):
    """Botão centralizado. Se selecionado, coloca '>' na frente."""
    color     = LIGHTEST if selected else DARKEST
    scale     = 1

    points_button = [
        [[x + (width // 2), y + (height // 2)], [x - (width // 2), y + (height // 2)]],
        [[x - (width // 2), y + (height // 2)], [x - (width // 2), y - (height // 2)]],
        [[x - (width // 2), y - (height // 2)], [x + (width // 2), y - (height // 2)]],
        [[x + (width // 2), y - (height // 2)], [x + (width // 2), y + (height // 2)]],
    ]
    for (x0, y0), (x1, y1) in points_button:
        bresenham(surf, x0, y0, x1, y1, DARKEST)
    
    floodFill(surf, x, y, DARK, DARKEST)

    draw_text(surf, label, x, y-2, color, scale=scale, mode="center")
    
def draw_scanline_button(surf, width, height, label,x, y, selected):
    """Botão centralizado. Se selecionado, coloca '>' na frente."""
    color     = LIGHTEST if selected else LIGHT
    scale     = 1
    
    points_scanline = [
        (x + (width // 2), y + (height // 2)),
        (x - (width // 2), y + (height // 2)),
        (x - (width // 2), y - (height // 2)),
        (x + (width // 2), y - (height // 2))
    ]
    scanline_fill(surf, points_scanline, DARK)
    
    points_button = [
        [(x + (width // 2), y + (height // 2)), (x - (width // 2), y + (height // 2))],
        [(x - (width // 2), y + (height // 2)), (x - (width // 2), y - (height // 2))],
        [(x - (width // 2), y - (height // 2)), (x + (width // 2), y - (height // 2))],
        [(x + (width // 2), y - (height // 2)), (x + (width // 2), y + (height // 2))],
    ]
    for (x0, y0), (x1, y1) in points_button:
        bresenham(surf, x0, y0, x1, y1, DARKEST)

    draw_text(surf, label, x, y-2, color, scale=scale, mode="center")