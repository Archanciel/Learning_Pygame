import pygame
import math
import random
from particle import Particle

DIST_MIN = 10

def overlap(my_particles, radius, x, y):
	for particle in my_particles:
		if math.hypot(particle.x - x, particle.y - y) < particle.radius + radius + DIST_MIN:
			return True
			
	return False

PN = 100
background_colour = (255,255,255)
(width, height) = (1300, 2000)
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption('Tutorial 1')
screen.fill(background_colour)
(h, w) = screen.get_size()
circleX = h / 2
circleY = w / 2
circleR = (w / 3) - 100
pygame.draw.circle(screen, (0, 0, 255), (circleX, circleY), circleR, 10)

my_particles = []

radius = random.randint(10,40)
pos_x = random.randint(radius, w - radius)
pos_y = random.randint(radius, h - radius)

for i in range(PN):
	while math.hypot(circleX - pos_x, circleY - pos_y) > circleR - radius \
			or overlap(my_particles, radius, pos_x, pos_y):
		radius = random.randint(10,40)
		pos_x = random.randint(radius, w - radius)
		pos_y = random.randint(radius, h - radius)
	p = Particle(screen, pos_x, pos_y, radius)
	my_particles.append(p)
	radius = random.randint(10,40)
	pos_x = random.randint(radius, w - radius)
	pos_y = random.randint(radius, h - radius)

	
for p in my_particles:
	p.display()
		
pygame.display.flip()

running = True

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

pygame.quit()