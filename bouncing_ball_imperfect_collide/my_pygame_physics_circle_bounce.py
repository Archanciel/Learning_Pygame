import pygame
import random
import math
import os

background_colour = (255,255,255)
(width, height) = (0, 0)
drag = 0.999
elasticity = 1
gravity = (math.pi, 0.002)

def addVectors(angle1, length1, angle2, length2):
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    angle = 0.5 * math.pi - math.atan2(y, x)
    length  = math.hypot(x, y)

    return (angle, length)

def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.centerX - x, p.centerY - y) <= p.radius:
            return p
    return None

def collide(p1, p2):
    dx = p1.centerX - p2.centerX
    dy = p1.centerY - p2.centerY
    
    dist = math.hypot(dx, dy)
    if dist < p1.radius + p2.radius:
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent

        angle1 = 2*tangent - p1.angle
        angle2 = 2*tangent - p2.angle
        speed1 = p2.speed*elasticity
        speed2 = p1.speed*elasticity

        (p1.angle, p1.speed) = (angle1, speed1)
        (p2.angle, p2.speed) = (angle2, speed2)

        p1.centerX += math.sin(angle)
        p1.centerY -= math.cos(angle)
        p2.centerX -= math.sin(angle)
        p2.centerY += math.cos(angle)

class Particle():
    
    def __init__(self, centerX, centerY, radius, boundaryCircleCenterX, boundaryCircleCenterY, boundaryCircleRadius):
        self.boundaryCircleCenterX = boundaryCircleCenterX
        self.boundaryCircleCenterY = boundaryCircleCenterY
        self.boundaryCircleRadius = boundaryCircleRadius

        self.centerX = centerX
        self.centerY = centerY
        self.radius = radius
        self.colour = (0, 0, 255)
        self.thickness = 0
        self.speed = 0
        self.angle = 0

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.centerX), int(self.centerY)), self.radius, self.thickness)

    def move(self):
        #(self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.centerX += math.sin(self.angle) * self.speed
        self.centerY -= math.cos(self.angle) * self.speed
        self.speed *= drag

    def bounce(self):
        dx = self.boundaryCircleCenterX - self.centerX
        dy = self.boundaryCircleCenterY - self.centerY
        overlap = math.hypot(dx, dy) - (self.boundaryCircleRadius - self.radius)

        if overlap >= 0:
            tangent = math.atan2(dy, dx)
            self.angle = 2 * tangent - self.angle
            self.speed *= elasticity

            angle = 0.5 * math.pi + tangent
            self.centerX += math.sin(angle) * overlap
            self.centerY -= math.cos(angle) * overlap
            
        if self.centerX > width - self.radius:
            self.centerX = 2 * (width - self.radius) - self.centerX
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.centerX < self.radius:
            self.centerX = 2 * self.radius - self.centerX
            self.angle = - self.angle
            self.speed *= elasticity

        if self.centerY > height - self.radius:
            self.centerY = 2 * (height - self.radius) - self.centerY
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.centerY < self.radius:
            self.centerY = 2 * self.radius - self.centerY
            self.angle = math.pi - self.angle
            self.speed *= elasticity

if os.name == 'posix':
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
else:
    WINDOWS_LOCATION = '100,25'
    os.environ['SDL_VIDEO_WINDOW_POS'] = WINDOWS_LOCATION
    screen = pygame.display.set_mode((800, 800))

width, height = screen.get_size()
pygame.display.set_caption('Tutorial 8')
boundaryCircleCenterX = width / 2
boundaryCircleCenterY = height / 2
boundaryCircleRadius = width / 2.1
number_of_particles = 2
my_particles = []

for n in range(number_of_particles):
    radius = random.randint(50, 80)
    centerX = random.randint(radius, width - radius)
    centerY = random.randint(radius, height - radius)

    particle = Particle(centerX, centerY, radius, boundaryCircleCenterX, boundaryCircleCenterY, boundaryCircleRadius)
    particle.speed = random.random()
    particle.angle = random.uniform(0, math.pi*2)

    my_particles.append(particle)

clock = pygame.time.Clock()
selected_particle = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = findParticle(my_particles, mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None

    if selected_particle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.centerX
        dy = mouseY - selected_particle.centerY
        selected_particle.angle = 0.5*math.pi + math.atan2(dy, dx)
        selected_particle.speed = math.hypot(dx, dy) * 0.1

    screen.fill(background_colour)
    if os.name == 'posix':
        pygame.draw.circle(screen, (0,0,0), (boundaryCircleCenterX, boundaryCircleCenterY), boundaryCircleRadius, 1)
    else:
        pygame.draw.circle(screen, (0, 0, 0), (int(round(boundaryCircleCenterX)), int(round(boundaryCircleCenterY))), int(round(boundaryCircleRadius)), 1)

    for i, particle in enumerate(my_particles):
        particle.move()
        particle.bounce()
        for particle2 in my_particles[i+1:]:
            collide(particle, particle2)
        particle.display()

    pygame.display.flip()
    clock.tick(200)
