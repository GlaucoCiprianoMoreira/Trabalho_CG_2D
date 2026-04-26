import pygame

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

    def update(self, dt, keys):
        self.is_moving = False
        
        # Movimentação e Atualização de Direção
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed * dt
            self.direction = "up"
            self.is_moving = True
            
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed * dt
            self.direction = "down"
            self.is_moving = True
            
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed * dt
            self.direction = "left"
            self.is_moving = True
            
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed * dt
            self.direction = "right"
            self.is_moving = True

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