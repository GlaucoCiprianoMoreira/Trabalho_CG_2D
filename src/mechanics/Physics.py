def check_grid_collision(x, y, hitbox_w, hitbox_h, offset_x, offset_y, level):
    """
    Verifica se uma hitbox genérica colide com os blocos sólidos do mapa.
    Pode ser usada por jogadores, inimigos ou projéteis.
    """
    TILE_SIZE = 16
    
    left = x + offset_x
    right = left + hitbox_w - 0.1
    top = y + offset_y
    bottom = top + hitbox_h - 0.1
    
    corners = [
        (int(top // TILE_SIZE), int(left // TILE_SIZE)),
        (int(top // TILE_SIZE), int(right // TILE_SIZE)),
        (int(bottom // TILE_SIZE), int(left // TILE_SIZE)),
        (int(bottom // TILE_SIZE), int(right // TILE_SIZE))
    ]
    
    for row, col in corners:
        if 0 <= row < len(level) and 0 <= col < len(level[0]):
            if level[row][col] == 1: # 1 é bloco sólido
                return True
                
    return False

def check_trigger(x, y, hitbox_w, hitbox_h, offset_x, offset_y, trigger_map):
    """
    Verifica colisões de área entre a hitbox do jogador e zonas específicas de blocos.
    Retorna o ID do bloco (ex: ID da porta, espinho) ou None.
    """
    TILE_SIZE = 16

    px = x + offset_x
    py = y + offset_y
    pw = hitbox_w
    ph = hitbox_h

    left = px
    right = px + pw - 0.1
    top = py
    bottom = py + ph - 0.1

    col_start = int(left // TILE_SIZE)
    col_end = int(right // TILE_SIZE)
    row_start = int(top // TILE_SIZE)
    row_end = int(bottom // TILE_SIZE)

    for row in range(row_start, row_end + 1):
        for col in range(col_start, col_end + 1):
            if 0 <= row < len(trigger_map) and 0 <= col < len(trigger_map[0]):
                tile_id = trigger_map[row][col]
                
                if tile_id > 10: 
                    if tile_id == 11:
                        up_tolerance = 4
                        down_tolerance = 12
                        side_tolerance = 8
                        tile_x = col * TILE_SIZE
                        tile_y = row * TILE_SIZE
                        
                        if (px < tile_x + TILE_SIZE - side_tolerance) and (px + pw > tile_x + side_tolerance):
                            if (py + ph > tile_y + up_tolerance) and (py < tile_y + TILE_SIZE - down_tolerance):
                                return tile_id
                            
                    else:
                        return tile_id
                        
    return None


def check_interaction(x, y, hitbox_w, hitbox_h, offset_x, offset_y, direction, interact_map):
    """
    Projeta um ponto à frente do jogador baseado na direção que ele olha.
    Usado quando o jogador aperta um botão de ação (Enter/Espaço).
    """
    TILE_SIZE = 16
    
    # Começa no centro da Hitbox
    target_x = x + offset_x + (hitbox_w / 2)
    target_y = y + offset_y + (hitbox_h / 2)
    
    # Empurra o ponto de checagem 1 bloco inteiro para a frente
    if direction == "up":
        target_y -= TILE_SIZE
    elif direction == "down":
        target_y += TILE_SIZE
    elif direction == "left":
        target_x -= TILE_SIZE
    elif direction == "right":
        target_x += TILE_SIZE
        
    row = int(target_y // TILE_SIZE)
    col = int(target_x // TILE_SIZE)
    
    if 0 <= row < len(interact_map) and 0 <= col < len(interact_map[0]):
        tile_id = interact_map[row][col]
        # Assumindo que IDs entre 20 e 30 são coisas interativas (ex: 21=Placa, 22=Baú)
        if tile_id >= 20:
            return tile_id
            
    return None

def check_aabb_collision(px, py, pw, ph, ox, oy, ow, oh):
    """
    Verifica matematicamente a intersecção entre dois retângulos AABB.
    P = Player, O = Objeto (Minério)
    """
    if (px < ox + ow) and (px + pw > ox) and (py < oy + oh) and (py + ph > oy):
        return True
    return False