import pygame, random, math
import ui, table

def deg(angle): # radianes a grados
    while angle >= 2*math.pi:
        angle -= 2*math.pi
    return (180 * angle) / math.pi

def rad(angle): # grados a radianes
    while angle >= 360:
        angle -= 360
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
    def __init__(self, size):
        w,h = size
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
        #self.angle = math.acos(x / math.sqrt(x**2 + y**2))
        if x == 0:
            self.angle = math.pi/2 if y >= 0 else 3*math.pi/2
        elif x > 0 and y > 0: # I
            self.angle = math.atan(y/x)
        elif x < 0 and y > 0: # II
            self.angle = (math.pi/2 - math.atan(y/-x)) + math.pi/2
        elif x < 0 and y <= 0: # III
            self.angle = math.atan(y/x) + math.pi
        elif x > 0 and y <= 0: # IV
            self.angle = (math.pi/2 - math.atan(-y/x)) + 3*math.pi/2

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
        self.origin = pygame.image.load('assets/asteroids.png').convert_alpha()
        self.origin = pygame.transform.scale(self.origin, size)
        self.img = self.origin
        self.rect = self.img.get_rect(topleft = pos)
        self.speed = (5 * math.cos(angle), 5 * math.sin(angle))
        self.angle = 0

    def draw(self, screen):
        screen.blit(self.img, self.rect)
        self.rect.centerx += self.speed[0]
        self.rect.centery += self.speed[1]
        # rotar asteroide
        self.img = pygame.transform.rotate(self.origin, self.angle)
        self.rect = self.img.get_rect(center = self.rect.center)
        self.angle += 2
        if self.angle >= 360:
            self.angle = 0
        

class State:
    def __init__(self, size):
        self.size = w, h = size
        self.percentage = 0
        self.timer = 0
        self.timer2 = 0
        self.text = ui.Label(str(self.percentage) + '%')
        self.text.rect.center = (w/2, 7*h/8)
        self.ship = Ship(size)
        self.asteroids = []
        self.asteroid_size = (w//12, w//12)
        self.score = 0

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
                tmp = random.randrange(1, 100) #[1, 99]
                for i in range(self.percentage):
                    if i == tmp:
                        return 'TABLE'
                self.ship.shoot(pos)
                self.score += self.percentage
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
        # si un asteroid choca con la nave
        while i < len(self.asteroids):
            if self.ship.rect.colliderect(self.asteroids[i].rect):
                return 'TABLE'
            i += 1
        
        self.timer += 1

    def draw(self, screen):
        self.text.draw(screen)
        self.ship.draw(screen)
        tmp = random.randrange(0, 4)
        
        if self.timer2 == 10:
            self.timer2 = 0
            # 0: arriba, 1: izq, 2: abajo, 3: der
            if tmp == 0:
                y = 0 - self.asteroid_size[1]
                x = random.randrange(0, screen.get_size()[0])
                angle = rad(random.randrange(225, 315))
                self.asteroids.append(Asteroid((x, y), angle, self.asteroid_size))
            elif tmp == 1:
                x = 0 - self.asteroid_size[0]
                y = random.randrange(0, screen.get_size()[1])
                angle = rad(random.randrange(315, 405))
                self.asteroids.append(Asteroid((x, y), angle, self.asteroid_size))
            elif tmp == 2:
                y = screen.get_size()[1]
                x = random.randrange(0, screen.get_size()[0])
                angle = rad(random.randrange(45, 135))
                self.asteroids.append(Asteroid((x, y), angle, self.asteroid_size))
            else:
                x = screen.get_size()[0]
                y = random.randrange(0, screen.get_size()[1])
                angle = rad(random.randrange(135, 225))
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

        # si una bala choca con un asteroide
        if len(self.ship.bullets) > 0:
            tmp1 = self.ship.bullets[:]
            tmp2 = self.asteroids[:]
            for bullet in tmp1:
                for asteroid in tmp2:
                    if bullet.rect.colliderect(asteroid.rect):
                        tmp1.remove(bullet)
                        tmp2.remove(asteroid)
                        self.score += 5
            self.ship.bullets = tmp1[:]
            self.asteroids = tmp2[:]

        self.timer2 += 1