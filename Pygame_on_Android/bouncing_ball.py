# http://predicate.us/journey/asteroids/3/

import pygame, sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Bouncing Ball with classes')

# Set our color constants

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create the ball class

class Ball():
    # This code gets executed as soon as we create a new instance
    def __init__(self, color, x, y, radius, speed):
        self.color = color
        self.rect = pygame.Rect(x, y, radius * 2, radius * 2)
        self.speed = [speed, speed]

    # Update our game state by moving and bouncing if needed

    def update(self):
        self.rect = self.rect.move(self.speed)

        if self.rect.right >= DISPLAYSURF.get_width() or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]

        if self.rect.top <= 0 or self.rect.bottom >= DISPLAYSURF.get_height():
            self.speed[1] = -self.speed[1]

    # Draw our ball to the screen

    def draw(self):
        pygame.draw.circle(DISPLAYSURF, self.color, self.rect.center, self.rect.width / 2)


# Create a new Ball instance named 'myball'

myball = Ball(WHITE, 100, 100, 25, 15)
run = True
clock = pygame.time.Clock()
timer = 0
dt = 0

# Game loop

while run:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if timer == 0:
            	timer = 0.001
                # Click again before 0.5 seconds to double click.
            elif timer < 0.5:
                # Double click happened
                run = False

    # Update game state

    myball.update()

    # Draw screen

    DISPLAYSURF.fill(BLACK)
    myball.draw()
    pygame.display.update()
    
    # Increase timer after mouse was pressed the first time.
    if timer != 0:
        timer += dt
        # Reset after 0.5 seconds.
        if timer >= 0.5:
             timer = 0
        
    # dt == time in seconds since last tick.
    # / 1000 to convert milliseconds to seconds.
    dt = clock.tick(30) / 1000
    