from loader.LoadMatrix import draw_sprite, draw_sprite_transformed

class Ore:
    def __init__(self, x, y, sprite_matrix):
        self.x = x
        self.y = y
        self.sprite = sprite_matrix
        self.health = 3
        
        self.current_scale = 1.0
        self.hit_timer = 0.0
        self.anim_duration = 0.01

    def hit(self):
        if self.health > 0:
            self.health -= 1
            self.hit_timer = self.anim_duration

    def update(self, dt):
        if self.hit_timer > 0:
            self.hit_timer -= dt
            half_time = self.anim_duration / 2.0
            if self.hit_timer > half_time:
                progress = (self.anim_duration - self.hit_timer) / half_time
                self.current_scale = 1.0 - (0.3 * progress)
            else:
                progress = (half_time - self.hit_timer) / half_time
                self.current_scale = 0.7 + (0.3 * progress)
                
            if self.hit_timer <= 0:
                self.current_scale = 1.0

    def draw(self, screen, camera_x, camera_y):
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        if self.current_scale != 1.0:
            draw_sprite_transformed(screen, self.sprite, screen_x, screen_y, self.current_scale)
        else:
            draw_sprite(screen, self.sprite, screen_x, screen_y)