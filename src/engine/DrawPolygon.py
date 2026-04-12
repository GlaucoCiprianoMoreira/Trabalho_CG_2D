from engine.Bresenham import bresenham

def drawPolygon(surface, points, color):
    n = len(points)
    for i in range(n):
        x0, y0 = points[i]
        x1, y1 = points[(i + 1) % n]
        bresenham(surface, x0, y0, x1, y1, color)