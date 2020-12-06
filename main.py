import pygame
import sys
import states

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

game = states.Manager(screen.get_size())

while True:
    clock.tick(60) # 60fps
    if pygame.event.get(pygame.QUIT):
        pygame.quit()
        sys.exit()

    game.handle_input(pygame.event.get())
    game.draw(screen)
    pygame.display.update()