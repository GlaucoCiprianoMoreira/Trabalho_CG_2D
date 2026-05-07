from engine.render.SetPixel import setPixel

def reta_ingenua(surface, x0, y0, x1, y1, color):
    # Garantir x crescente
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0

    # Evita divisão por zero (reta vertical não é tratada aqui)
    if dx == 0:
        return

    m = (y1 - y0) / dx
    b = y0 - m * x0

    for x in range(x0, x1 + 1):
        y = m * x + b
        setPixel(surface, x, round(y), color)

def dda(surface, x0, y0, x1, y1, color):
    dx = x1 - x0
    dy = y1 - y0

    steps = max(abs(dx), abs(dy))

    if steps == 0:
        setPixel(surface, x0, y0, color)
        return

    x_inc = dx / steps
    y_inc = dy / steps

    x = x0
    y = y0

    for _ in range(steps + 1):
        setPixel(surface, round(x), round(y), color)
        x += x_inc
        y += y_inc