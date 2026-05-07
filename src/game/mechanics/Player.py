import pygame

import config.Variables as variables

import game.audio.Audio_manager as audio_manager
from game.mechanics.Physics import check_grid_collision, check_aabb_collision

class Player:
    def __init__(self, start_x, start_y, sprites_dict):
        self.invincible_timer = 0.0
        self.is_visible = True

        self.x = start_x
        self.y = start_y
        self.speed = 700.0
        self.space_pressed = False
        
        self.sprites = sprites_dict
        
        self.direction = "down"
        self.is_moving = False
        
        self.current_frame = 0
        self.anim_timer = 0.0
        self.anim_speed = 0.01

        self.hitbox_w = 14
        self.hitbox_h = 14
        self.offset_x = 2
        self.offset_y = 1

    def take_damage(self):
        if self.invincible_timer <= 0:
            variables.health -= 1
            self.invincible_timer = 0.2

    def update(self, dt, keys, level, solid_entities):
        was_moving = self.is_moving
        self.is_moving = False
        dx = 0
        dy = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed * dt
            self.direction = "up"
            
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed * dt
            self.direction = "down"
            
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed * dt
            self.direction = "left"
            
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed * dt
            self.direction = "right"

        if dx != 0:
            self.is_moving = True
            new_x = self.x + dx
            if not check_grid_collision(new_x, self.y, self.hitbox_w, self.hitbox_h, self.offset_x, self.offset_y, level):
                hit_solid = False
                for entity in solid_entities:
                    hx, hy = new_x + self.offset_x, self.y + self.offset_y
                    if check_aabb_collision(hx, hy, self.hitbox_w, self.hitbox_h, entity.x, entity.y, 16, 16):
                        hit_solid = True
                        break
                if not hit_solid: self.x += dx

        if dy != 0:
            self.is_moving = True
            new_y = self.y + dy
            if not check_grid_collision(self.x, new_y, self.hitbox_w, self.hitbox_h, self.offset_x, self.offset_y, level):
                hit_solid = False
                for entity in solid_entities:
                    hx, hy = self.x + self.offset_x, new_y + self.offset_y
                    if check_aabb_collision(hx, hy, self.hitbox_w, self.hitbox_h, entity.x, entity.y, 16, 16):
                        hit_solid = True
                        break
                if not hit_solid: self.y += dy
        
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            if not self.space_pressed:
                self.space_pressed = True
                self.is_mining = True
                audio_manager.play_sfx('mining')
        else:
            self.space_pressed = False
            self.is_mining = False

        if self.is_moving:
            self.anim_timer += dt
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0.0
                self.current_frame = (self.current_frame + 1) % 4
        else:
            self.current_frame = 0
            self.anim_timer = 0.0
        
        if self.is_moving and not was_moving:
            audio_manager.play_steps()
        elif not self.is_moving and was_moving:
            audio_manager.stop_steps()

        if self.invincible_timer > 0:
            self.invincible_timer -= dt
            self.is_visible = int(self.invincible_timer * 80) % 2 == 0
        else:
            self.is_visible = True

    def get_current_sprite(self):
        return self.sprites[self.direction][self.current_frame]
    
    def get_facing_point(self):
        px = self.x + 8
        py = self.y + 8
        
        if self.direction == "up": py -= 16
        elif self.direction == "down": py += 16
        elif self.direction == "left": px -= 16
        elif self.direction == "right": px += 16
            
        return px, py