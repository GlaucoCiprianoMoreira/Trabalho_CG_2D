import pygame

from scene_manager.scene import Scene

class CutsceneScene(Scene):
    def __init__(self, manager):
        self.manager = manager
        self.n_frame = 0
        self.frames = [
            "o homem anda pelos corredores",
            "ele está destraído com seu celular",
            "mandando mensagens para o seu amor",
            "ele não percebeu que havia um buraco em sua frente...",
            "ele cai",
            "tudo escuro",
            "ele acorda e não vê nada além de uma lamparina iluminando um esqueleto e uma picareta",
            "ele pega a lamparina e a picareta",
            "'preciso sair daqui'"
        ]
    
    def handle_event(self, event):
        #n_frame = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.n_frame += 1
                if self.n_frame < 10: print(self.frames[self.n_frame-1])
        if self.n_frame == 10:
            self.manager.go_to("gameplay")
            print("iniciando jogo...")
    
    def draw(self, screen):
        pass

    