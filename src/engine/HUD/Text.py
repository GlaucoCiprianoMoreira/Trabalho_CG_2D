from engine.render.SetPixel import setPixel
from config.Constants import FONT

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
        cx = x
        
    for ch in text:
        glyph = FONT.get(ch, FONT[' '])
        for row, bits in enumerate(glyph):
            for col, bit in enumerate(bits):
                if bit == '1':
                    base_x = cx + col * scale
                    base_y = y + row * scale
                    for sy in range(scale):
                        for sx in range(scale):
                            setPixel(surface, base_x + sx, base_y + sy, fade_color)
        cx += (len(glyph[0]) + 1) * scale