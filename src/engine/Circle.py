from engine.SetPixel import setPixel

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