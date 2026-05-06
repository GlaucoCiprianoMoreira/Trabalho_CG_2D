import pygame
import audio_manager
from mechanics.Physics import check_grid_collision, check_aabb_collision
from loader.LoadMap import levels

class Player:
    def __init__(self, start_x, start_y, sprites_dict):
        # Vida
        self.health = 3
        self.invincible_timer = 0.0 # Timer de Dano
        self.is_visible = True      # Controle do Blinking


        
        # Posição no Espaço do Mundo
        self.x = start_x
        self.y = start_y
        self.speed = 700.0 # Pixels por segundo
        self.space_pressed = False
        
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

    def take_damage(self):
        if self.invincible_timer <= 0:
            self.health -= 1
            self.invincible_timer = 0.2
            print(f"AAAAAI! Vida restante: {self.health}")

    def update(self, dt, keys, level, solid_entities):
        was_moving = self.is_moving
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
            new_x = self.x + dx
            if not check_grid_collision(new_x, self.y, self.hitbox_w, self.hitbox_h, self.offset_x, self.offset_y, level):
                hit_solid = False
                for entity in solid_entities:
                    hx, hy = new_x + self.offset_x, self.y + self.offset_y
                    if check_aabb_collision(hx, hy, self.hitbox_w, self.hitbox_h, entity.x, entity.y, 16, 16):
                        hit_solid = True
                        break
                if not hit_solid: self.x += dx
        # Eixo Y
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
        
        # Trava para o botão SPACE (Edge Detection)
        if keys[pygame.K_SPACE]:
            if not self.space_pressed:
                self.space_pressed = True
                self.is_mining = True
                audio_manager.play_sfx('mining')
        else:
            self.space_pressed = False
            self.is_mining = False

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
        
        if self.is_moving and not was_moving:
            audio_manager.play_steps()
        elif not self.is_moving and was_moving:
            audio_manager.stop_steps()

        # Lógica de Invencibilidade
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
            self.is_visible = int(self.invincible_timer * 80) % 2 == 0
        else:
            self.is_visible = True

    def get_current_sprite(self):
        """Retorna a matriz de pixels correta para o momento atual."""
        return self.sprites[self.direction][self.current_frame]
    
    def get_facing_point(self):
        """Retorna as coordenadas x, y imediatamente à frente do jogador."""
        px = self.x + 8
        py = self.y + 8
        
        if self.direction == "up": py -= 16
        elif self.direction == "down": py += 16
        elif self.direction == "left": px -= 16
        elif self.direction == "right": px += 16
            
        return px, py