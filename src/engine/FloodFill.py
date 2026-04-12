from engine.SetPixel import setPixel

def floodFillIterative(surface, x, y, filling_color, edge_color):
    width = surface.get_width()
    height = surface.get_height()

    stack = [(x, y)]

    while stack:
        x, y = stack.pop()

        if not (0 <= x < width and 0 <= y < height):
            continue

        current_color = surface.get_at((x, y))[:3]

        if current_color == edge_color or current_color == filling_color:
            continue

        setPixel(surface, x, y, filling_color)

        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))