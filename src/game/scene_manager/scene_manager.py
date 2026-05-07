class SceneManager:
    def __init__(self):
        self._scenes = {}
        self._current = None
    
    def register(self, name, scene):
        self._scenes[name] = scene
    
    def go_to(self, name):
        if self._current:
            self._current.on_exit()
        self._current = self._scenes[name]
        self._current.on_enter()

    def handle_event(self, event):
        self._current.handle_event(event)
    
    def update(self, dt):
        self._current.update(dt)
    
    def draw(self, screen):
        self._current.draw(screen)