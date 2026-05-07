from engine.render.SetPixel import setPixel

def midpointEllipse(surface, xc, yc, rx, ry, color):
    x = 0
    y = ry
    rx2 = rx * rx
    ry2 = ry * ry
    p1 = ry2 - (rx2 * ry) + (0.25 * rx2)

    def drawEllipsePoints(xc, yc, x, y):
        setPixel(surface, xc + x, yc + y, color)
        setPixel(surface, xc - x, yc + y, color)
        setPixel(surface, xc + x, yc - y, color)
        setPixel(surface, xc - x, yc - y, color)

    drawEllipsePoints(xc, yc, x, y)
    
    while (ry2 * x) < (rx2 * y):
        x += 1
        if p1 < 0:
            p1 += 2 * ry2 * x + ry2
        else:
            y -= 1
            p1 += 2 * ry2 * x - 2 * rx2 * y + ry2
        drawEllipsePoints(xc, yc, x, y)

    p2 = (ry2 * (x + 0.5) ** 2) + (rx2 * (y - 1) ** 2) - (rx2 * ry2)
    
    while y >= 0:
        y -= 1
        if p2 > 0:
            p2 += rx2 - 2 * rx2 * y
        else:
            x += 1
            p2 += 2 * ry2 * x - 2 * rx2 * y + rx2
        drawEllipsePoints(xc, yc, x, y)