import pygame
import math
import random
import os
from particle import Particle

PN = 500
DIST_MIN = 1

background_colour = (255,255,255)

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
	my_particle_1 = Particle(screen = screen, x=400, y=1000, radius=25, thickness=3, angleDeg=100, speed=2)
	my_particle_2 = Particle(screen = screen, x=400, y=1000, radius=25, thickness=3, angleDeg=90, speed=1)
	my_particle_3 = Particle(screen = screen, x=400, y=1200, radius=25, thickness=3, angleDeg=90, speed=1)
else:
	my_particle_1 = Particle(screen = screen, x=100, y=300, radius=25, thickness=1, angleDeg=100, speed=0.2)
	my_particle_2 = Particle(screen = screen, x=100, y=300, radius=25, thickness=1, angleDeg=90, speed=0.1)
	my_particle_3 = Particle(screen = screen, x=100, y=500, radius=25, thickness=1, angleDeg=90, speed=0.1)



running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
	screen.fill(background_colour)
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
	
	my_particle_1.move(angleDeg=100)
	my_particle_2.move(angleDeg=90)
	my_particle_3.move_tuto(angleRad=math.pi / 2)

	my_particle_1.display()
	my_particle_2.display()
	my_particle_3.display()

	pygame.display.flip()
pygame.quit()