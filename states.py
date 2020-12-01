import pygame
import menu, tutorial, game

class Background:
    def __init__(self, screen):
        self.w = screen.get_size()[0]
        self.bg = pygame.image.load('assets/background.png').convert()
        self.bg = pygame.transform.scale(self.bg, (self.w, self.w))
        self.sound = pygame.mixer.Sound('sound/background.wav')
        self.sound.play(-1)
        self.x = 0

    def draw(self, screen):
        screen.blit(self.bg, (self.x, 0))
        screen.blit(self.bg, (self.w + self.x, 0))
        self.x -= 1
        if self.w <= -self.x:
            self.x = 0

class Manager:
    def __init__(self, screen):
        self.state = menu.State(screen)
        self.bg = Background(screen)
    
    def handle_input(self, screen, input):
        s = self.state.handle_input(input)
        if s == 'GAME':
            self.state = game.State(screen)
        elif s == 'TUTORIAL':
            self.state = tutorial.State(screen)
        elif s == 'MENU':
            self.state = menu.State(screen)
    
    def draw(self, screen):
        self.bg.draw(screen)
        self.state.draw(screen)
