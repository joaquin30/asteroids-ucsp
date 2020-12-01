import pygame, random, math
import ui

def deg(angle):
    while angle >= 2*math.pi:
        angle -= 2*math.pi
    return (180 * angle) / math.pi

def rad(angle):
    angle %= 360
    return (math.pi * angle) / 180

class Bullet:
    def __init__(self, size, angle, pos):
        self.img = pygame.image.load('assets/bullet.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, size)
        self.rect = self.img.get_rect(center = pos)
        self.speed = (10 * math.cos(angle), 10 * math.sin(angle))
    
    def draw(self, screen):
        screen.blit(self.img, self.rect)
        self.rect.centerx += self.speed[0]
        self.rect.centery += self.speed[1]

class Ship:
    def __init__(self, screen):
        w,h = screen.get_size()
        self.origin = pygame.image.load('assets/ship.png').convert_alpha()
        self.origin = pygame.transform.scale(self.origin, (w//24, w//24))
        self.origin = pygame.transform.rotate(self.origin, -90)
        self.bullet_size = (w//100, w//100)
        self.img = self.origin
        self.rect = self.img.get_rect(center = (w/2,h/2))
        self.angle = 0.0
        self.bullets = []
        self.shoot_sound = pygame.mixer.Sound('sound/shoot.wav')

    def rotate(self, pos):
        x, y = pos[0] - self.rect.centerx, -pos[1] + self.rect.centery
        if y >= 0:
            self.angle = math.acos(x / math.sqrt(x**2 + y**2))
        else:
            self.angle = -math.acos(x / math.sqrt(x**2 + y**2))

        self.img = pygame.transform.rotate(self.origin, deg(self.angle))
        self.rect = self.img.get_rect(center = self.rect.center)
    
    def shoot(self, pos):
        tmp = Bullet(self.bullet_size, -self.angle, self.rect.center)
        self.bullets.append(tmp)
        self.shoot_sound.play()

    def draw(self, screen):
        i = 0
        while i < len(self.bullets):
            if self.bullets[i].rect.center < (0,0) or self.bullets[i].rect.center > screen.get_size():
                del self.bullets[i]
            else:
                self.bullets[i].draw(screen)
                i += 1
        screen.blit(self.img, self.rect)

class Asteroid:
    def __init__(self, pos, angle, size):
        self.origin = pygame.image.load('assets/meteor.png').convert_alpha()
        self.origin = pygame.transform.scale(self.origin, size)
        self.img = self.origin
        self.rect = self.img.get_rect(topleft = pos)
        self.speed = (5 * math.cos(angle), 5 * math.sin(angle))
        self.angle = 0

    def draw(self, screen):
        screen.blit(self.img, self.rect)
        self.rect.centerx += self.speed[0]
        self.rect.centery += self.speed[1]
        self.img = pygame.transform.rotate(self.origin, self.angle)
        self.rect = self.img.get_rect(center = self.rect.center)
        self.angle += 2
        self.angle %= 360
        

class State:
    def __init__(self, screen):
        w, h = screen.get_size()
        self.percentage = 0
        self.timer = 0
        self.timer2 = 0
        self.text = ui.Label(str(self.percentage) + '%')
        self.text.rect.center = (w/2, 7*h/8)
        self.ship = Ship(screen)
        self.asteroids = []
        self.asteroid_size = (w//12, w//12)

    def handle_input(self, input):
        if self.timer >= 100 and self.percentage > 0:
            self.percentage -= 1
            self.timer = 0
            tmp = ui.Label(str(self.percentage) + '%')
            tmp.rect.center = self.text.rect.center
            self.text = tmp

        for event in input:
            pos = pygame.mouse.get_pos()
            self.ship.rotate(pos)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                tmp = random.randrange(0,100)
                for i in range(self.percentage):
                    if i == tmp:
                        return 'MENU'
                self.ship.shoot(pos)
                self.percentage += 1
                self.timer = 0
                tmp = ui.Label(str(self.percentage) + '%')
                tmp.rect.center = self.text.rect.center
                self.text = tmp

        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_w]:
            self.ship.rect.centery -= 3
        elif key_input[pygame.K_s]:
            self.ship.rect.centery += 3
        if key_input[pygame.K_a]:
            self.ship.rect.centerx -= 3
        elif key_input[pygame.K_d]:
            self.ship.rect.centerx += 3
            
        i = 0
        while i < len(self.asteroids):
            if self.ship.rect.colliderect(self.asteroids[i].rect):
                return 'MENU'

            j = 0
            while j < len(self.ship.bullets):
                if self.asteroids[i].rect.colliderect(self.ship.bullets[j].rect):
                    del self.asteroids[i]
                    del self.ship.bullets[j]
                    if i < len(self.asteroids):
                        break
                else:
                    j += 1

            i += 1
        
        self.timer += 1
        return 'NONE'

    def draw(self, screen):
        self.text.draw(screen)
        self.ship.draw(screen)
        tmp = random.randrange(0, 4)
        
        if self.timer2 == 10:
            self.timer2 = 0

            if tmp == 0:
                y = 0 - self.asteroid_size[1]
                x = random.randrange(0, screen.get_size()[0] - self.asteroid_size[0])
                angle = rad(random.randrange(225, 315))
                speed = (5 * math.cos(angle), 5 * math.sin(angle))
                self.asteroids.append(Asteroid((x, y), angle, self.asteroid_size))
            elif tmp == 1:
                x = 0 - self.asteroid_size[0]
                y = random.randrange(0, screen.get_size()[1] - self.asteroid_size[1])
                angle = rad(random.randrange(315, 405))
                speed = (5 * math.cos(angle), 5 * math.sin(angle))
                self.asteroids.append(Asteroid((x, y), angle, self.asteroid_size))
            elif tmp == 2:
                y = screen.get_size()[1]
                x = random.randrange(0, screen.get_size()[0]- - self.asteroid_size[0])
                angle = rad(random.randrange(45, 135))
                speed = (5 * math.cos(angle), 5 * math.sin(angle))
                self.asteroids.append(Asteroid((x, y), angle, self.asteroid_size))
            else:
                x = screen.get_size()[0]
                y = random.randrange(0, screen.get_size()[1] - self.asteroid_size[1])
                angle = rad(random.randrange(135, 225))
                speed = (5 * math.cos(angle), 5 * math.sin(angle))
                self.asteroids.append(Asteroid((x, y), angle, self.asteroid_size))

        i = 0
        inf = (-self.asteroid_size[0], -self.asteroid_size[1])
        sup = (screen.get_size()[0] + self.asteroid_size[0], screen.get_size()[1] + self.asteroid_size[1])
        while i < len(self.asteroids):
            if self.asteroids[i].rect.center < inf or self.asteroids[i].rect.center > sup:
                del self.asteroids[i]
            else:
                self.asteroids[i].draw(screen)
                i += 1

        self.timer2 += 1