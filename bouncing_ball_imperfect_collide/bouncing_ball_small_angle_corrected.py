import pygame, sys, math
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((1000, 800))
pygame.display.set_caption('Bouncing Ball with position and angle')

# Set our color constants
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Create the ball class
class Ball():
    def __init__(self,
                 screen,
                 color,
                 radius,
                 startX,
                 startY,
                 speed,
                 angle=45,
                 noRounding=False):
        super().__init__()
        self.screen = screen
        self.color = color
        rectSize = radius * 2
        self.rect = pygame.Rect(startX, startY, rectSize, rectSize)
        self.speed = speed
        self.angle = math.radians(angle)
        self.circleCenter = self.rect.center
        self.noRounding = noRounding
        
    def update(self):
        delta_x = self.speed * math.cos(self.angle)
        delta_y = self.speed * math.sin(self.angle)
        
        newCenterX = self.circleCenter[0] + delta_x
        newCenterY = self.circleCenter[1] + delta_y
        self.circleCenter = (newCenterX, newCenterY)
        
        # rounding the coordinates of self.circleCenter is woong and causes
        # the circle with small angle to stay on its horizontal moving line
        # instead of going up 1 degree at each bound cycle
        #self.circleCenter = (round(newCenterX), round(newCenterY))
        
        if self.noRounding:
        	self.rect.center = (self.circleCenter[0], self.circleCenter[1])
        else:
        	self.rect.center = (round(self.circleCenter[0]), round(self.circleCenter[1]))
 
        if self.rect.right >= self.screen.get_width() or self.rect.left <= 0:
            self.angle = math.pi - self.angle

        if self.rect.top <= 0 or self.rect.bottom >= self.screen.get_height():
            self.angle = -self.angle

    def draw(self):
        '''
    	Draw our ball to the screen with position information.
    	'''
        pygame.draw.circle(self.screen, self.color, self.rect.center, int(self.rect.width / 2))

# Create a new Ball instance named 'myball'
myball = Ball(screen=DISPLAYSURF, color=RED, startX=100, startY=100, radius=150, speed=12, angle=-1, noRounding=True)
mySmaLlAngleball = Ball(screen=DISPLAYSURF, color=YELLOW, startX=100, startY=105, radius=150, speed=12, angle=-1)

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
    mySmaLlAngleball.update()
    
    # Draw screen
    DISPLAYSURF.fill(BLACK)
    myball.draw()
    mySmaLlAngleball.draw()
    pygame.display.update()
    clock.tick(100)
