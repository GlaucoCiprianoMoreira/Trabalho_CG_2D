import math
from engine.render.Transformations import identity, translation, rotation, scale, multiply, apply
from engine.render.DrawPolygon import drawPolygon
from engine.render.ScanlineFill import scanline_fill
from config.constants import DARKEST, LIGHTEST

class Crystal:
    def __init__(self, x, y):
        self.world_x = x
        self.world_y = y
        self.time = 0.0

        self.vertices = [
            (0, -4),
            (3, 0),
            (0, 4),
            (-3, 0)
        ]
        
    def update(self, dt):
        self.time += dt

    def check_collection(self, player_x, player_y):
        dist = math.hypot((self.world_x) - (player_x + 8), (self.world_y) - (player_y + 8))
        return dist < 8 # Raio de coleta

    def draw(self, screen, camera_x, camera_y):
        anim_angle = self.time * 15.0
        anim_y_offset = math.sin(self.time * 10.0) * 1.5
        
        R = rotation(anim_angle)
        
        screen_x = self.world_x - camera_x + 8
        screen_y = self.world_y - camera_y + 8 + anim_y_offset
        T = translation(screen_x, screen_y)
        
        M = multiply(T, R)
        
        transformed_points = []
        for v in self.vertices:
            pt = apply(v, M)
            transformed_points.append(pt)
            
        scanline_fill(screen, transformed_points, LIGHTEST)
        drawPolygon(screen, transformed_points, DARKEST)