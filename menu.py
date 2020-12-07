import sys, pygame
import ui

names = 'Grupo 5:\nJoaquin Pino\nRenzo Gallegos\nSelinne Carlin\nVictor Calvo\nMixel Corrido'

class State:
    def __init__(self, size):
        w, h = size
        self.title = ui.Picture('assets/title.png', (w/3, h/4), (w/3, h/4))
        self.sound = pygame.mixer.Sound('sound/bip.wav')
        self.play = ui.Label('Jugar', (2*w/5, 9*h/16))
        self.tutorial = ui.Label('¿Cómo jugar?', (2*w/5, 10*h/16))
        self.exit = ui.Label('Salir', (2*w/5, 11*h/16))
        self.names = ui.BigLabel(names, (0, 0), size)
        self.names.font = pygame.font.Font('assets/Goldman-Regular.ttf', 24)

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
    
    def draw(self, screen):
        self.title.draw(screen)
        self.play.draw(screen)
        self.tutorial.draw(screen)
        self.exit.draw(screen)
        self.names.draw(screen)