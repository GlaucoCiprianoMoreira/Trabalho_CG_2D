import audio_manager

from loader.LoadMatrix import draw_sprite

class Chest:
    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        self.sprites = sprites
        self.state = "closed" # closed, opening, opened
        self.frame = 0
        self.anim_timer = 0.0
        self.anim_speed = 0.005
        
    def interact(self):
        if self.state == "closed":
            self.state = "opening"

    def update(self, dt):
        if self.state == "opening":
            self.anim_timer += dt
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0.0
                self.frame += 1
                if self.frame >= len(self.sprites) - 1:
                    self.frame = len(self.sprites) - 1
                    self.state = "opened" # Terminou de abrir

    def draw(self, screen, camera_x, camera_y):
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        draw_sprite(screen, self.sprites[self.frame], screen_x, screen_y)