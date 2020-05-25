import pygame
import random
import math
import os

background_colour = (255,255,255)
pygame.init()

if os.name == 'posix':
	(width, height) = (1300, 2000)
	screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
else:
	(width, height) = (800, 1000)
	os.environ['SDL_VIDEO_WINDOW_POS'] = '100,15'
	screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Move particle basic')
(w, h) = screen.get_size()

drag = 0.999
elasticity = 0.75
#drag = 1
#elasticity = 1
gravity = (math.pi, 0.002)

def addVectors(v1, v2):
    angle1 = v1[0]
    angle2 = v2[0]
    length1 = v1[1]
    length2 = v2[1]
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    angle = 0.5 * math.pi - math.atan2(y, x)
    length  = math.hypot(x, y)

    return (angle, length)

class Particle():
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 2
        self.speed = 0
        self.angle = 0

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= drag

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

number_of_particles = 1
my_particles = []

for n in range(number_of_particles):
    size = random.randint(50, 100)
    x = random.randint(size, width-size)
    y = random.randint(size, height-size)

    particle = Particle(x, y, size)
    #particle.speed = random.random()
    particle.speed = 2
    particle.angle = random.uniform(0, math.pi*2)

    my_particles.append(particle)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_colour)

    for particle in my_particles:
        particle.move()
        particle.bounce()
        particle.display()

    pygame.display.flip()