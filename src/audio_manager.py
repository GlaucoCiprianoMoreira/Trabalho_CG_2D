# audio_manager.py  (raiz do projeto, ao lado do main.py)
import pygame
from global_variables import config

# ─────────────────────────────────────────────────────────────────
#  INICIALIZAÇÃO
# ─────────────────────────────────────────────────────────────────

def init():
    """
    Chame uma vez no main.py antes do loop.
    Inicializa o mixer com configurações adequadas para chiptune:
      - frequency 44100 Hz (padrão CD)
      - size -16         (16-bit signed)
      - channels 2       (estéreo)
      - buffer 512       (pequeno → menos latência nos SFX)
    """
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    _load_sfx()

# ─────────────────────────────────────────────────────────────────
#  TABELA DE SFX
#  Carregamos todos na memória uma vez. Assim não há disco I/O
#  durante o jogo — só na inicialização.
# ─────────────────────────────────────────────────────────────────

_sfx: dict[str, pygame.mixer.Sound] = {}

def _load_sfx():
    sounds = {
        "click":         "assets/audio/sfx/clicando-algo.ogg",
        "select":         "assets/audio/sfx/selecionando-algo.ogg",
        "colect":         "assets/audio/sfx/coleta-item.ogg",
        "game_over":       "assets/audio/sfx/game-over.ogg",
        "game_win":         "assets/audio/sfx/game-win.ogg",
        "chest_open":   "assets/audio/sfx/clicando-algo.ogg",
        "chest_mimic":  "assets/audio/sfx/mimic.ogg",
        "mining":       "assets/audio/sfx/minerando.ogg",
        "steps":         "assets/audio/sfx/passos.ogg",
        "trap":         "assets/audio/sfx/pisou-na-armadilha.ogg",
    }
    for name, path in sounds.items():
        try:
            _sfx[name] = pygame.mixer.Sound(path)
        except FileNotFoundError:
            print(f"[audio] SFX não encontrado: {path}")

# ─────────────────────────────────────────────────────────────────
#  MÚSICA DE FUNDO
# ─────────────────────────────────────────────────────────────────

_current_music: str = ""   # guarda qual música está tocando

def play_music(name: str, loop: bool = True):
    """
    Toca uma música de fundo.

    - Se a mesma música já estiver tocando, não faz nada
      (evita reiniciar a faixa a cada troca de cena).
    - Respeita config.music_on: se estiver desligado, só
      registra o nome mas não toca.
    - loop=True → repete indefinidamente (-1 no pygame).
    """
    global _current_music

    # Nada a fazer se já é a música atual
    if name == _current_music:
        return

    _current_music = name

    if not config.music_on:
        return

    path = f"assets/audio/music/{name}.ogg"
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1 if loop else 0)
    except FileNotFoundError:
        print(f"[audio] Música não encontrada: {path}")


def stop_music():
    global _current_music
    _current_music = ""
    pygame.mixer.music.stop()


def set_music_on(value: bool):
    """
    Chamado quando o usuário altera config.music_on no menu.
    Liga ou desliga a música mantendo o estado de qual faixa
    deveria estar tocando.
    """
    config.music_on = value
    if value:
        # Retoma a música que estava registrada
        if _current_music:
            path = f"assets/audio/music/{_current_music}.ogg"
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.play(-1)
            except FileNotFoundError:
                pass
    else:
        pygame.mixer.music.stop()

# ─────────────────────────────────────────────────────────────────
#  EFEITOS SONOROS
# ─────────────────────────────────────────────────────────────────

def play_sfx(name: str):
    """
    Toca um efeito sonoro pelo nome registrado em _load_sfx.
    Respeita config.sound_on.
    Vários SFX podem tocar ao mesmo tempo (mixer aloca canais).
    """
    if not config.sound_on:
        return
    sound = _sfx.get(name)
    if sound:
        sound.play()
    else:
        print(f"[audio] SFX desconhecido: '{name}'")


def set_sound_on(value: bool):
    """Chamado quando o usuário altera config.sound_on no menu."""
    config.sound_on = value
    if not value:
        # Para todos os canais de SFX imediatamente
        pygame.mixer.stop()