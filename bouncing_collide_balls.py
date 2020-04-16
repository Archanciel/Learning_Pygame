import pygame, sys, math, random

from pygame.locals import *


pygame.init()

DISPLAYSURF = pygame.display.set_mode((640, 480))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
COLORS = [WHITE, RED, GREEN, BLUE, YELLOW]

pygame.display.set_caption('Bouncing Ball with classes')

# Create the ball class

class Ball():

    # This code gets executed as soon as we create a new instance

    def __init__(self, color, x, y, radius, speed, angle=-45):

        self.color = color

        self.rect = pygame.Rect(x, y, radius * 2, radius * 2)

        self.speed = speed
        
        self.angle = math.radians(-angle)


    # Update our game state by moving and bouncing if needed

    def update(self):

        delta_x = self.speed*math.cos(self.angle)

        delta_y = self.speed*math.sin(self.angle)

        self.rect = self.rect.move(delta_x, delta_y)

        hit_bounds = False

        if self.rect.right >= DISPLAYSURF.get_width() or self.rect.left <= 0:

            self.angle = math.pi - self.angle
            
            hit_bounds = True

        if self.rect.top <= 0 or self.rect.bottom >= DISPLAYSURF.get_height():

            self.angle = -self.angle
            
            hit_bounds = True

        for ball in ball_list:

            if not hit_bounds and not ball is self and self.rect.colliderect(ball.rect):

                self.angle = self.angle - math.pi
                
                break


    # Draw our ball to the screen

    def draw(self):

        pygame.draw.circle(DISPLAYSURF, self.color, self.rect.center, int(self.rect.width / 2))


## Make our list variable

ball_list = []


# Create a list of 10 Ball instances

for i in range(10):

    colIdx = random.randrange(0, 4)
    
    ball_list.append(Ball(COLORS[colIdx], i * 60, i * 45, max(i * 3, 20), min(i * 2, 8)))

# Game loop

while True:

    # Handle events

    for event in pygame.event.get():

        if event.type == QUIT:

            pygame.quit()

            sys.exit()


# Update game state

    for ball in ball_list:
    	ball.update()


    # Draw screen

    DISPLAYSURF.fill(BLACK)

    for ball in ball_list:
    	ball.draw()

    pygame.display.update()