import pygame
import math
import random
import os
from particle import Particle

DIST_MIN = 1

def randomParticleParm():
	radius = random.randint(10,40)
	pos_x = random.randint(radius, w)
	pos_y = random.randint(radius, h)
	
	return (radius, pos_x, pos_y)

	
def outsideCircle(circleX, circleY, radius, x, y):
	return math.hypot(circleX - x, circleY - y) > circleR - radius - DIST_MIN

def overlap(my_particles, radius, x, y):
	# Returns True if a new particle with values radius, x, y would
	# overlap an existing particle referenced in the list my_particles
	for particle in my_particles:
		if math.hypot(particle.x - x, particle.y - y) < particle.radius + radius + DIST_MIN:
			return True
			
	return False

background_colour = (255,255,255)

if os.name == 'posix':
	PN = 500
	THICKNESS = 1
	(width, height) = (1300, 2000)
	screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
else:
	PN = 200
	THICKNESS = 1
	(width, height) = (800, 1000)
	os.environ['SDL_VIDEO_WINDOW_POS'] = '100,15'
	screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Tutorial 1')
screen.fill(background_colour)
(w, h) = screen.get_size()

if os.name == 'posix':
	circleX = w / 2
	circleY = h / 2
	circleR = (h / 3) - 100
	pygame.draw.circle(screen, (0, 0, 255), (circleX, circleY), circleR, 10)
else:
	circleX = w / 2
	circleY = w / 2
	circleR = (h / 2) - 105
	pygame.draw.circle(screen, (0, 0, 255), (round(circleX), round(circleY)), round(circleR), 1)

my_particles = []

# initialising the new particle size and position values
radius, pos_x, pos_y = randomParticleParm()

for i in range(PN):
	while outsideCircle(circleX, circleY, radius, pos_x, pos_y) or overlap(my_particles, radius, pos_x, pos_y):
		radius, pos_x, pos_y = randomParticleParm()

	p = Particle(screen=screen, x=pos_x, y=pos_y, radius=radius, thickness=THICKNESS, angle=100, speed=2)
	my_particles.append(p)
	radius, pos_x, pos_y = randomParticleParm()

for p in my_particles:
	p.display()
		
pygame.display.flip()

running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

pygame.quit()