import random
import pygame
import config.Variables as variables

MUSIC_END = pygame.USEREVENT + 1
_queue:        list[str] = []
_queue_source: list[str] = []

_ui_channel  : pygame.mixer.Channel = None
_step_channel: pygame.mixer.Channel = None

_MUSIC_VOLUME = 0.3
_SFX_VOLUME = 1

_SFX_INDIVIDUAL_VOLUME = {
    "step":        0.3,
    "mining":      0.7,
    "mine_hit":    0.6,
    "mine_break":  0.9,
    "collect":     0.5,
    "damage":      1.0,
    "chest_open":  0.7,
    "chest_mimic": 1.0,
    "trap":        0.9,
    "select":      0.5,
    "click":       0.6,
}

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
    pygame.mixer.music.set_endevent(MUSIC_END)

    global _ui_channel, _step_channel
    _ui_channel   = pygame.mixer.Channel(0)
    _step_channel = pygame.mixer.Channel(1)

    _load_sfx()

_sfx: dict[str, pygame.mixer.Sound] = {}

def _load_sfx():
    sounds = {
        "click":       "assets/audio/sfx/clicando-algo.ogg",
        "select":      "assets/audio/sfx/selecionando-algo.ogg",
        "colect":      "assets/audio/sfx/coleta-item.ogg",
        "game_over":   "assets/audio/sfx/game-over.ogg",
        "game_win":    "assets/audio/sfx/game-win.ogg",
        "chest_open":  "assets/audio/sfx/clicando-algo.ogg",
        "chest_mimic": "assets/audio/sfx/mimic.ogg",
        "mining":      "assets/audio/sfx/minerando.ogg",
        "steps":       "assets/audio/sfx/passos.ogg",
        "trap":        "assets/audio/sfx/pisou-na-armadilha.ogg",
    }
    for name, path in sounds.items():
        try:
            sfx = pygame.mixer.Sound(path)
            vol = _SFX_INDIVIDUAL_VOLUME.get(name, _SFX_VOLUME)
            sfx.set_volume(vol)
            _sfx[name] = sfx
        except FileNotFoundError:
            print(f"[audio] SFX não encontrado: {path}")

_current_music: str = ""

def play_music(name: str, loop: bool = True):
    global _current_music, _queue, _queue_source

    _queue        = []
    _queue_source = []

    # Nada a fazer se já é a música atual
    if name == _current_music:
        return

    _current_music = name

    if not variables.music_on:
        return

    _start_track(f"assets/audio/music/{name}.ogg", loop)

def play_music_queue(tracks: list[str]):
    global _queue_source

    _queue_source = tracks[:]   # guarda a lista original
    _refill_queue()             # monta a fila embaralhada e toca a primeira

def _refill_queue():
    global _queue

    _queue = _queue_source[:]
    random.shuffle(_queue)
    _play_next_in_queue()

def _play_next_in_queue():
    global _current_music, _queue

    if not _queue:
        _refill_queue()
        return

    name           = _queue.pop(0)
    _current_music = name

    if not variables.music_on:
        return

    _start_track(f"assets/audio/music/{name}.ogg", loop=False)

def handle_event(event):
    if event.type == MUSIC_END and _queue_source:
        _play_next_in_queue()

def _start_track(path: str, loop: bool):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(_MUSIC_VOLUME)
        pygame.mixer.music.play(-1 if loop else 0)
    except FileNotFoundError:
        print(f"[audio] Música não encontrada: {path}")

def stop_music():
    global _current_music, _queue, _queue_source
    _current_music = ""
    _queue        = []
    _queue_source = []
    pygame.mixer.music.stop()


def set_music_on(value: bool):
    variables.music_on = value
    if value and _current_music:
        if _queue_source:
            _start_track(f"assets/audio/music/{_current_music}.ogg", loop=False)
        else:
            _start_track(f"assets/audio/music/{_current_music}.ogg", loop=True)
    elif not value:
        pygame.mixer.music.stop()

def play_sfx(name: str, ui: bool = False):
    if not variables.sound_on:
        return
    sound = _sfx.get(name)
    if not sound:
        print(f"[audio] SFX desconhecido: '{name}'")
        return
    
    if ui:
        _ui_channel.stop()
        _ui_channel.play(sound)
    else:
        sound.play()


def set_sound_on(value: bool):
    variables.sound_on = value
    if not value:
        # Para todos os canais de SFX imediatamente
        pygame.mixer.stop()

# volumes
def set_music_volume(vol: float):
    global _MUSIC_VOLUME
    _MUSIC_VOLUME = max(0.0, min(1.0, vol))
    pygame.mixer.music.set_volume(_MUSIC_VOLUME)

def set_sfx_volume(vol: float):
    global _SFX_VOLUME
    _SFX_VOLUME = max(0.0, min(1.0, vol))
    for name, sound in _sfx.items():
        individual = _SFX_INDIVIDUAL_VOLUME.get(name, 1.0)
        sound.set_volume(individual * _SFX_VOLUME)

# steps
def play_steps():
    if not variables.sound_on:
        return
    sound = _sfx.get("steps")
    if sound and not _step_channel.get_busy():
        _step_channel.play(sound, loops=-1)

def stop_steps():
    _step_channel.stop()