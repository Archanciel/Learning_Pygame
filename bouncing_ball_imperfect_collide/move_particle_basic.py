import pygame
import math
import random
import os
from particledisplaypos import ParticleDisplayPos
from particledisplayposandtraject import ParticleDisplayPosAndTraject
from particle import Particle

PN = 30
DIST_MIN = 1

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (2, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

PARTICLE_FOR_ANGLE_START_NUMBER = 2
PARTICLE_FOR_ANGLE_END_NUMBER = 3

background_colour = WHITE
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

my_particles = []


angleTwelth = 360 / 12

if os.name == 'posix':
	for i in range(PARTICLE_FOR_ANGLE_START_NUMBER, PARTICLE_FOR_ANGLE_END_NUMBER):
		angleDeg = i * angleTwelth
		my_particles.append(ParticleDisplayPosAndTraject(screen=screen, x=circleX, y=circleY, radius=100, colour=BLUE, thickness=3, angleDeg=angleDeg, speed=1.8))
else:
	for i in range(PARTICLE_FOR_ANGLE_START_NUMBER, PARTICLE_FOR_ANGLE_END_NUMBER):
		angleDeg = i * angleTwelth
		my_particles.append(ParticleDisplayPosAndTraject(screen=screen, x=circleX, y=circleY, radius=70, colour=BLUE, thickness=1, angleDeg=angleDeg, speed=0.18))
		
running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
	screen.fill(background_colour)
	if os.name == 'posix':
		pygame.draw.circle(screen, BLUE, (circleX, circleY), circleR, 10)
	else:
		pygame.draw.circle(screen, BLUE, (round(circleX), round(circleY)), round(circleR), 1)


	for particle in my_particles:
		#particle.my_move()
		#particle.move()
		particle.move_tuto()
		particle.bounce()
		particle.display()	
	
	pygame.display.flip()
pygame.quit()