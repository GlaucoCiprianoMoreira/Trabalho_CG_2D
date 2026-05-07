from engine.render.SetPixel import setPixel
from config.constants import FONT

def get_text_width(text: str, scale=1):
    width = 0
    text_len = len(text)
    for i, ch in enumerate(text):
        glyph = FONT.get(ch, FONT[' '])
        glyph_width = len(glyph[0])

        width += glyph_width * scale

        if i < text_len - 1:
            width += scale

    return width

def draw_text(surface, text: str, x, y, color, scale=1, mode="left", alpha=1.0):
    """Renderiza string com a fonte bitmap 3×5."""
    if alpha <= 0.0: 
        return
    
    fade_color = (
        int(color[0] * alpha),
        int(color[1] * alpha),
        int(color[2] * alpha)
    )

    text = text.upper()

    if mode != "left":
        text_width = get_text_width(text, scale)
        if mode == "center":
            cx = int(x - (text_width // 2))
        else:
            cx = int(x - text_width)
    else:
        cx = x                                                                  # pos inicial da letra atual
        
    for ch in text:                                                             # converte o texto pra maiúsculo. itera letra por letra
        glyph = FONT.get(ch, FONT[' '])                                         # procura a letra na fonte. se nao existir, retorna ' '
        for row, bits in enumerate(glyph):                                      # row é o índice. bits são os bits da linha: ("10001")
            for col, bit in enumerate(bits):                                    # col é a coluna do bit da letra. bit é o valor: 0 ou 1
                if bit == '1':                                                  # se for 1, deve pintar
                    base_x = cx + col * scale
                    base_y = y + row * scale
                    for sy in range(scale):                                     # (y) aplicando um zoom usando escala
                        for sx in range(scale):                                 # (x) aplicando um zoom usando escala
                            setPixel(surface, base_x + sx, base_y + sy, fade_color)     # desenha
        cx += (len(glyph[0]) + 1) * scale                                       # largura do glyph + espaço