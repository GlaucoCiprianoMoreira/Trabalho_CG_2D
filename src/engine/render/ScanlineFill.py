from engine.render.SetPixel import setPixel

def scanline_fill(surface, points, filling_color):
    ys = [p[1] for p in points]
    y_min = min(ys)
    y_max = max(ys)

    n = len(points)

    for y in range(y_min, y_max):
        intersections_x = []

        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % n]

            if y0 == y1:
                continue

            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0

            if y < y0 or y >= y1:
                continue

            x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            intersections_x.append(x)

        intersections_x.sort()

        for i in range(0, len(intersections_x), 2):
            if i + 1 < len(intersections_x):
                x_init = int(round(intersections_x[i]))
                x_end = int(round(intersections_x[i + 1]))

                for x in range(x_init, x_end + 1):
                    setPixel(surface, x, y, filling_color)