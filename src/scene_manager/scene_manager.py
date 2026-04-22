class SceneManager:
    def __init__(self):
        self._scenes = {}
        self._current = None
    
    def register(self, name, scene):
        self._scenes[name] = scene
    
    def go_to(self, name):
        self._current = self._scenes[name]
    
    def handle_event(self, event):
        self._current.handle_event(event)
    
    def update(self, dt):
        self._current.update(dt)
    
    def draw(self, screen):
        self._current.draw(screen)