from engine.SetPixel import setPixel
import math

def Circle(surface, xc, yc, r, color):
    x =0
    y = r
    p = 3 - 2 * r

    def drawCirclePoints(xc, yc, x, y):
        setPixel(surface, xc + x, yc + y, color)
        setPixel(surface, xc - x, yc + y, color)
        setPixel(surface, xc + x, yc - y, color)
        setPixel(surface, xc - x, yc - y, color)
        setPixel(surface, xc + y, yc + x, color)
        setPixel(surface, xc - y, yc + x, color)
        setPixel(surface, xc + y, yc - x, color)
        setPixel(surface, xc - y, yc - x, color)
    
    drawCirclePoints(xc, yc, x, y)
    while x <= y:
        x += 1
        if p > 0:
            y -= 1
            p = p + 4 * (x - y) + 10
        else:
            p = p + 4 * x + 6
        drawCirclePoints(xc, yc, x, y)

def fill_circle(surface, xc, yc, r, color):
    for y in range(yc - r, yc + r + 1):
        dy = y - yc
        dx = int(math.sqrt(r*r - dy*dy))

        x_start = xc - dx
        x_end   = xc + dx

        for x in range(x_start, x_end + 1):
            setPixel(surface, x, y, color)