# http://predicate.us/journey/asteroids/3/

import pygame, sys, math
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('Bouncing Ball with position and angle')

# Set our color constants

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Create the ball class

class Ball():
    def __init__(self,
                 screen,
                 color,
                 radius,
                 startX,
                 startY,
                 speed,
                 angle=45):
        super().__init__()
        self.screen = screen
        self.color = color
        rectSize = radius * 2
        self.rect = pygame.Rect(startX, startY, rectSize, rectSize)
        self.speed = speed
        self.angle = math.radians(angle)
        
        # position related instance variables
        self.font = pygame.font.Font(None, 32)
        self.font_height = self.font.get_linesize()
        self.textLeftMargin = self.rect.width / 4
        self.textTopMargin = radius - self.font_height / 2
        self.textColor = BLACK

    def update(self):
        delta_x = self.speed * math.cos(self.angle)
        delta_y = self.speed * math.sin(self.angle)
        self.rect = self.rect.move(delta_x, delta_y)

        if self.rect.right >= self.screen.get_width() or self.rect.left <= 0:
            self.angle = math.pi - self.angle

        if self.rect.top <= 0 or self.rect.bottom >= self.screen.get_height():
            self.angle = -self.angle

    # Draw our ball to the screen with position information
    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.rect.center, int(self.rect.width / 2))
        
        textLines = []
        textLines.append('x: ' + str(int(self.rect.centerx)) + ' y: ' + str(int(self.rect.centery)))
        textLines.append('angle: ' + str(int(math.degrees(self.angle))))

        self.images = []  # The text surfaces.

        for line in textLines:
            surf = self.font.render(line, True, self.textColor)
            self.images.append(surf)

        for y, surf in enumerate(self.images):
            self.screen.blit(surf, (
            self.rect.x + self.textLeftMargin, self.rect.y + self.textTopMargin + y * self.font_height))


# Create a new Ball instance named 'myball'
myball = Ball(screen=DISPLAYSURF, color=YELLOW, startX=100, startY=100, radius=100, speed=5)

run = True
clock = pygame.time.Clock()

# Display loop
while run:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update ball position
    myball.update()

    # Draw screen
    DISPLAYSURF.fill(BLACK)
    myball.draw()
    pygame.display.update()
    clock.tick(60)
