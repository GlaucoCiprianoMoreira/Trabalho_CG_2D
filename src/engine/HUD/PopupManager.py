from engine.HUD.Text import draw_text

class PopupManager:
    def __init__(self):
        self.state = "idle"
        self.timer = 0.0
        self.text = ""
        self.alpha = 0.0

    def trigger(self, text, delay=0.02):
        self.text = text
        self.state = "delay"
        self.timer = delay
        self.alpha = 0.0

    def update(self, dt):
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