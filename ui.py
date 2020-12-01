import pygame

class BigLabel:
    def __init__(self, text, pos, size):
        self.size = size
        self.pos = pos
        self.font = pygame.font.Font('assets/Goldman-Regular.ttf', 36)
        self.words = [word.split(' ') for word in text.splitlines()]
        self.space = self.font.size(' ')[0]
    
    def draw(self, screen):
        x, y = self.pos
        for line in self.words:
            for word in line:
                word_surface = self.font.render(word, True, (255, 255, 255))
                word_width, word_height = word_surface.get_size()
                if x + word_width >= self.size[0]:
                    x = self.pos[0]  # Resetea x
                    y += word_height  # Inicia nueva fila
                screen.blit(word_surface, (x, y))
                x += word_width + self.space
            x = self.pos[0] # Resetea x
            y += word_height # Inicia nueva fila

class Label:
    def __init__(self, text):
        font = pygame.font.Font('assets/Goldman-Regular.ttf', 36)
        self.text = font.render(text, True, (255, 255, 255))
        self.rect = self.text.get_rect()
    
    def draw(self, screen):
        screen.blit(self.text, self.rect)

class Picture:
    def __init__(self, img, pos, size):
        self.img = pygame.image.load(img).convert_alpha()
        self.img = pygame.transform.scale(self.img, (int(size[0]), int(size[1])))
        self.pos = pos

    def draw(self, screen):
        screen.blit(self.img, self.pos)