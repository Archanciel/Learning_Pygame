import pygame
import math
import random
import os
from particledisplaypos import ParticleDisplayPos

PN = 500
DIST_MIN = 1

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

if os.name == 'posix':
	circleX = w / 2
	circleY = h / 2
	circleR = (h / 3) - 100
else:
	circleX = w / 2
	circleY = w / 2
	circleR = (h / 2) - 105

#my_particles = []
#my_particles2 = []
my_particles3 = []

angleTwelth = 360 / 12

if os.name == 'posix':
	for i in range(1, 13):
		angleDeg = i * angleTwelth
#		my_particles.append(ParticleDisplayPos(screen = screen, x=circleX, y=circleY, radius=25, thickness=3, angleDeg=angleDeg, speed=2))
#		my_particles2.append(ParticleDisplayPos(screen = screen, x=circleX, y=circleY, radius=15, thickness=3, angleDeg=angleDeg, speed=1))
		my_particles3.append(ParticleDisplayPos(screen = screen, x=circleX, y=circleY, radius=100, thickness=3, angleDeg=angleDeg, speed=0.8))
else:
	for i in range(1, 13):
		angleDeg = i * angleTwelth
#		my_particles.append(ParticleDisplayPos(screen = screen, x=circleX, y=circleY, radius=25, thickness=1, angleDeg=angleDeg, speed=0.2))
#		my_particles2.append(ParticleDisplayPos(screen = screen, x=circleX, y=circleY, radius=15, thickness=1, angleDeg=angleDeg, speed=0.1))
		my_particles3.append(ParticleDisplayPos(screen = screen, x=circleX, y=circleY, radius=70, thickness=1, angleDeg=angleDeg, speed=0.08))

running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
	screen.fill(background_colour)
	if os.name == 'posix':
		pygame.draw.circle(screen, (0, 0, 255), (circleX, circleY), circleR, 10)
	else:
		pygame.draw.circle(screen, (0, 0, 255), (round(circleX), round(circleY)), round(circleR), 1)

#	for particle in my_particles:
#		particle.move()
#		particle.display()	

#	for particle in my_particles2:
#		particle.move_tuto()
#		particle.display()	

	for particle in my_particles3:
		particle.my_move()
		#particle.move()
		#particle.move_tuto()
		particle.display()	
	
	pygame.display.flip()
pygame.quit()