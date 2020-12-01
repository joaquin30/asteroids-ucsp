import pygame, sys
import ui

class State:
    def __init__(self, screen):
        w, h = screen.get_size()
        self.title = ui.Picture('assets/title.png', (w/3, h/4), (w/3, h/4))
        self.sound = pygame.mixer.Sound('sound/bip.wav')
        self.play = ui.Label('Jugar')
        self.play.rect.topleft = (2*w/5, 9*h/16)
        self.tutorial = ui.Label('¿Cómo jugar?')
        self.tutorial.rect.topleft = (2*w/5, 10*h/16)
        self.exit = ui.Label('Salir')
        self.exit.rect.topleft = (2*w/5, 11*h/16)

    def handle_input(self, input):
        for event in input:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.play.rect.collidepoint(pos):
                    self.sound.play()
                    return 'GAME'
                elif self.tutorial.rect.collidepoint(pos):
                    self.sound.play()
                    return 'TUTORIAL'
                elif self.exit.rect.collidepoint(pos):
                    pygame.quit()
                    sys.exit()
        return 'NONE'
    
    def draw(self, screen):
        self.title.draw(screen)
        self.play.draw(screen)
        self.tutorial.draw(screen)
        self.exit.draw(screen)