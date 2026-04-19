from engine.SetPixel import setPixel

def boundaryFillIterative(surface, x, y, fill_color, boundary_color):
    width = surface.get_width()
    height = surface.get_height()

    stack = [(x, y)]

    while stack:
        x, y = stack.pop()

        if not (0 <= x < width and 0 <= y < height):
            continue

        current_color = surface.get_at((x, y))[:3]

        if current_color == boundary_color or current_color == fill_color:
            continue

        setPixel(surface, x, y, fill_color)

        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))

def boundaryFill(surface, x, y, fill_color, boundary_color):
    width = surface.get_width()
    height = surface.get_height()

    if not (0 <= x < width and 0 <= y < height):
        return

    current_color = surface.get_at((x, y))[:3]

    if current_color == boundary_color or current_color == fill_color:
        return

    setPixel(surface, x, y, fill_color)

    boundaryFill(surface, x + 1, y, fill_color, boundary_color)
    boundaryFill(surface, x - 1, y, fill_color, boundary_color)
    boundaryFill(surface, x, y + 1, fill_color, boundary_color)
    boundaryFill(surface, x, y - 1, fill_color, boundary_color)