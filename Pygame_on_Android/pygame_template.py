import pygame
from pygame.locals import *


pygame.init()

display_width = 800
display_height = 600

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Our Game')


def handleEvents():
    for event in pygame.event.get():
        if (event.type == QUIT or 
            event.type == MOUSEBUTTONDOWN or (
            event.type == KEYDOWN and (
            event.key == K_ESCAPE or
            event.key == K_q))):
            pygame.quit()
            quit()

while True:
    handleEvents()

    pygame.display.update()
 