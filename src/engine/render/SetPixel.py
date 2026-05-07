import pygame

def setPixel(surface, x, y, color):
        if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
                surface.set_at((x, y), color)

def getPixel(surface, x, y):
        if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
                return surface.get_at((x, y))
        return None