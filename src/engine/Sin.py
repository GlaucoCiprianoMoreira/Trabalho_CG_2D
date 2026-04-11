from engine.SetPixel import setPixel
import math

def drawSin(surface, height, width, color):
    amplitude = height // 4
    centro_y = height // 2
    frequency = 2*math.pi / width
    
    for x in range(width):
        y = centro_y - int(math.sin(x*frequency)*amplitude)
        setPixel(surface, x, y, (0, 0, 0), color)