from loader.LoadMatrix import load_png_matrix

PALETTE = {
    "DARKEST"  : (8, 24, 32),
    "DARK"     : (52, 104, 86),
    "LIGHT"    : (136, 192, 112),
    "LIGHTEST" : (224, 248, 208)
}

def load_tiles():
    return {
        1: load_png_matrix("assets/rock/rock_01.png"),
        2: load_png_matrix("assets/floor/floor_01.png"),
    }