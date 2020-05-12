import pygame
import math
import random
from particle import Particle

PN = 500
DIST_MIN = 0

def randomParticleParm():
	radius = random.randint(10,40)
	pos_x = random.randint(radius, w - radius)
	pos_y = random.randint(radius, h - radius)
	
	return (radius, pos_x, pos_y)

	
def outsideCircle(circleX, circleY, radius, x, y):
	if y < circleY:
		return math.hypot(circleX - x, circleY - y) > circleR - radius - DIST_MIN
	else:
		return math.hypot(circleX - x, y - circleY) > circleR - radius - DIST_MIN
	
def overlap(my_particles, radius, x, y):
	# Returns True if a new particle with values radius, x, y would
	# overlap an existing particle referenced in the list my_particles
	for particle in my_particles:
		if math.hypot(particle.x - x, particle.y - y) < particle.radius + radius + DIST_MIN:
			return True
			
	return False

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

# initialising the new particle size and position values
radius, pos_x, pos_y = randomParticleParm()

for i in range(PN):
	while outsideCircle(circleX, circleY, radius, pos_x, pos_y) \
		or overlap(my_particles, radius, pos_x, pos_y):
		radius, pos_x, pos_y = randomParticleParm()

	p = Particle(screen, pos_x, pos_y, radius)
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