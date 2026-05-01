import pygame
from mechanics.Physics import check_grid_collision
from loader.LoadMap import levels

class Player:
    def __init__(self, start_x, start_y, sprites_dict):
        # Posição no Espaço do Mundo
        self.x = start_x
        self.y = start_y
        self.speed = 700.0 # Pixels por segundo
        
        self.sprites = sprites_dict
        
        # Estado da Animação
        self.direction = "down"
        self.is_moving = False
        
        self.current_frame = 0
        self.anim_timer = 0.0
        self.anim_speed = 0.01 # Tempo em segundos para trocar de frame

        self.hitbox_w = 14
        self.hitbox_h = 14
        self.offset_x = 2
        self.offset_y = 1

    def update(self, dt, keys, level):
        self.is_moving = False
        dx = 0
        dy = 0

        # Movimentação e Atualização de Direção
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

        # Lógica de Colisão
        # Eixo X
        if dx != 0:
            self.is_moving = True
            if not check_grid_collision(self.x + dx, self.y, self.hitbox_w, self.hitbox_h, self.offset_x, self.offset_y, level):
                self.x += dx

        # Eixo Y
        if dy != 0:
            self.is_moving = True
            if not check_grid_collision(self.x, self.y + dy, self.hitbox_w, self.hitbox_h, self.offset_x, self.offset_y, level):
                self.y += dy

        # Lógica de Animação
        if self.is_moving:
            self.anim_timer += dt
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0.0
                self.current_frame = (self.current_frame + 1) % 4
        else:
            # Se parou de andar, reseta para o frame de "descanso"
            # Assumindo que o frame 0 é o personagem parado
            self.current_frame = 0
            self.anim_timer = 0.0

    def get_current_sprite(self):
        """Retorna a matriz de pixels correta para o momento atual."""
        return self.sprites[self.direction][self.current_frame]