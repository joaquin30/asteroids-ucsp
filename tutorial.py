import pygame
import ui

text = 'Controlas una nave (WASD) que tiene que sobrevivir el mayor tiempo posible hasta que venga la ayuda. Para lograrlo, tienes que esquivar o destruir los asteroides que se aproximan. Puedes disparar una bala de tu cañon (Click izq.), pero la munición que llevas es altamente inestable, asi que la probabilidad de explotar aumenta con cada disparo. Espera unos segundos y la probabilidad de suicidarse bajará. Buena suerte.'

class State:
    def __init__(self, screen):
        w, h = screen.get_size()
        self.sound = pygame.mixer.Sound("sound/bip.wav")
        self.tutorial = ui.BigLabel(text, (w/4, h/8), (3*w/4, 3*h/4))
        self.back = ui.Label('Volver')
        self.back.rect.center = (w/2, 7*h/8)
    
    def handle_input(self, input):
        for event in input:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.back.rect.collidepoint(pos):
                    self.sound.play()
                    return 'MENU'
        return 'NONE'
    
    def draw(self, screen):
        self.tutorial.draw(screen)
        self.back.draw(screen)
