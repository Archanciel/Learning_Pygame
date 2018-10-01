# Pygame template - skeleton for a new pygame project
import math

import pygame

WIDTH = 800
HEIGHT = 600
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
allSprites = pygame.sprite.Group()

class Trigo:
    def __init__(self, startCoord, endCoord):
        self.startCoord = startCoord
        self.endCoord = endCoord
        self.opposite = abs(endCoord[1] - startCoord[1])
        self.hypo = math.sqrt(((endCoord[0] - startCoord[0]) ** 2) + (self.opposite) ** 2)
        self.angle = math.degrees(math.asin(self.opposite / self.hypo))

    def draw(self, surface):
        pygame.draw.line(surface, RED, self.startCoord, self.endCoord)
        font = pygame.font.SysFont(name='comicsans', size=20)
        hypoTxtSurface = font.render("LENGTH: {0:3.0f} px".format(self.hypo), True, RED)
        textHeight = hypoTxtSurface.get_height()
        angleTxtSurface = font.render("ANGLE: {0:3.2f} °".format(self.angle), True, RED)
        surface.blit(hypoTxtSurface, self.endCoord)
        surface.blit(angleTxtSurface, (self.endCoord[0], self.endCoord[1] + textHeight * 1.3))

trigo = None
startCoord = None
endCoord = None
trigos = []

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            startCoord = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            endCoord = pygame.mouse.get_pos()

    # Update
    allSprites.update()

    if startCoord and endCoord and (sorted(startCoord) != sorted(endCoord)):
        trigos.append(Trigo(startCoord=startCoord, endCoord=endCoord))
        startCoord = None
        endCoord = None
    elif startCoord and endCoord and sorted(startCoord) == sorted(endCoord):
        startCoord = None
        endCoord = None

    # Draw / render
    screen.fill(BLACK)
    allSprites.draw(screen)

    for trigo in trigos:
        trigo.draw(screen)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()