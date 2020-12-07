import pygame, sys, datetime
import ui

'''
Guia Score:
 - El porcentaje de la pantalla se suma al disparar
 - Por cada asteroide destruido se suma 5
'''

class State:
    def __init__(self, size, score):
        sound = pygame.mixer.Sound('sound/expl1.wav')
        sound.play()
        w, h = size
        self.lnames = [datetime.datetime.now().strftime(r'%d/%m/%y-%H:%M')]
        self.lscore = [score]
        with open('score.txt') as f:
            tmp = 0
            for line in f:
                if tmp > 9:
                    break
                n, s = line.split()
                self.lnames.append(n)
                self.lscore.append(int(s))
                tmp += 1

        self.isort(self.lscore, self.lnames)
        self.names = ui.BigLabel('', (5*w/16, h/8), size)
        self.names.words = [['FECHA']]
        for i in self.lnames:
            self.names.words.append([i])

        self.score = ui.BigLabel('', (9*w/16, h/8), size)
        self.score.words = [['PUNTUACIÓN']]
        for i in self.lscore:
            self.score.words.append([str(i)])

        self.back = ui.Label('Volver')
        self.back.rect.center = (w/2, 7*h/8)
        self.sound = pygame.mixer.Sound("sound/bip.wav")
    
    def write(self):
        f = open('score.txt', 'w')
        for i in range(len(self.lnames)):
            f.write(self.lnames[i] + ' ' + str(self.lscore[i]) + '\n')

    def isort(self, arr, lt):
        for i in range(1, len(arr)):
            key1 = arr[i]
            key2 = lt[i]
            j = i-1
            while j >= 0 and key1 > arr[j] :
                arr[j+1] = arr[j]
                lt[j+1] = lt[j]
                j -= 1
            arr[j+1] = key1
            lt[j+1] = key2
    
    def handle_input(self, input):
        for event in input:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.back.rect.collidepoint(pos):
                    self.sound.play()
                    self.write()
                    return 'MENU'

    def draw(self, screen):
        self.names.draw(screen)
        self.score.draw(screen)
        self.back.draw(screen)
  
        


