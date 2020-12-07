import pygame
import menu, tutorial, game, table

class Background:
    def __init__(self, width): # ancho
        self.w = width
        self.bg = pygame.image.load('assets/background.png').convert()
        self.bg = pygame.transform.scale(self.bg, (self.w, self.w))
        self.x = 0

    def draw(self, screen):
        screen.blit(self.bg, (self.x, 0))
        screen.blit(self.bg, (self.w + self.x, 0))
        self.x -= 1
        if self.w <= -self.x:
            self.x = 0

class Manager:
    def __init__(self, size):
        self.size = size
        self.state = menu.State(size)
        self.bg = Background(size[0])
        pygame.mixer.music.load('sound/title.wav')
        pygame.mixer.music.play(-1)

    def handle_input(self, input):
        s = self.state.handle_input(input)
        if s == 'GAME':
            self.state = game.State(self.size)
            pygame.mixer.music.load('sound/background.wav')
            pygame.mixer.music.play(-1)
        elif s == 'TUTORIAL':
            self.state = tutorial.State(self.size)
        elif s == 'MENU':
            self.state = menu.State(self.size)
        elif s == 'TABLE':
            self.state = table.State(self.size, self.state.score)
            pygame.mixer.music.load('sound/title.wav')
            pygame.mixer.music.play(-1)
    
    def draw(self, screen):
        self.bg.draw(screen)
        self.state.draw(screen)
