from .text import draw_text
class PopupManager:
    """Gerencia a máquina de estados e o desenho de popups de texto na tela."""
    def __init__(self):
        self.state = "idle" # idle, delay, fade_in, show, fade_out
        self.timer = 0.0
        self.text = ""
        self.alpha = 0.0

    def trigger(self, text, delay=0.02):
        """Inicia um novo popup."""
        self.text = text
        self.state = "delay"
        self.timer = delay
        self.alpha = 0.0

    def update(self, dt):
        """Processa a máquina de estados e o cálculo matemático do alpha."""
        if self.state == "idle":
            return

        self.timer -= dt
        
        if self.state == "delay" and self.timer <= 0:
            self.state = "fade_in"
            self.timer = 0.12
            
        elif self.state == "fade_in":
            self.alpha = 1.0 - (max(self.timer, 0) / 0.1)
            if self.timer <= 0:
                self.state = "show"
                self.timer = 0.02
                self.alpha = 1.0
                
        elif self.state == "show" and self.timer <= 0:
            self.state = "fade_out"
            self.timer = 0.04
            
        elif self.state == "fade_out":
            self.alpha = max(self.timer, 0) / 0.1
            if self.timer <= 0:
                self.state = "idle"
                self.alpha = 0.0

    def draw(self, surface, center_x, y, color):
        """Chama o draw_text se o popup estiver visível."""
        if self.state not in ["idle", "delay"]:
            draw_text(
                surface, 
                self.text, 
                center_x, 
                y, 
                color, 
                scale=1, 
                mode="center", 
                alpha=self.alpha
            )