import pygame
import math
import random
import os
import time
from particledisplayposandtraject import ParticleDisplayPosAndTraject
#from particledisplayposandtrajectanglefromxaxis import ParticleDisplayPosAndTrajectAngleFromXAxis
from particledisplayposfromxaxis import ParticleDisplayPosFromXAxis
from particledisplayposandtraject import ParticleDisplayPosAndTraject
from particle import Particle
from textonscreen import TextOnScreen

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

SECOND_PARTICLE_X_SHIFT = 180

# gravity related constants are defined here simply to facilitate their 
# modification while experimenting

GRAVITY_VALUE = 9.80665

if os.name == 'posix':
	FPS = 1
	GRAVITY_VALUE_BY_FPS = GRAVITY_VALUE / FPS
	GRAVITY = (3 * math.pi / 2, GRAVITY_VALUE_BY_FPS) # ok on Android
else:
	FPS = 1
	GRAVITY_VALUE_BY_FPS = GRAVITY_VALUE / FPS
	GRAVITY = (3 * math.pi / 2, GRAVITY_VALUE_BY_FPS) # ok on Windows

#DRAG = 0.999
DRAG = 1
ELASTICITY = 0.85
HALF_GRAVITY_BY_FPS = GRAVITY_VALUE_BY_FPS / 2

def handleDoubleClick():
	global timerDC
	global pause
	global t0
	global tt0
	
	if timerDC == 0:
		timerDC = 0.01
		# Click again before 0.1 seconds to double click.
	elif timerDC < 0.1:
		# Double click happened
		if not pause:
			pause = True
		else:
			pause = False
			t0 = time.time()
			tt0 = t0
			
		'''
		if self.playing:
			self.playing = False
				
		self.running = False
		'''
		
def updateTimerForDoubleClick():
	# Increase timerDC after mouse was pressed the first time.
	global timerDC
	global dt

	if timerDC != 0:
		timerDC += dt

	# Reset after 0.5 seconds.
	if timerDC >= 0.1:
		timerDC = 0

	# dt == time in seconds since last tick.
	# / 1000 to convert milliseconds to 10th of seconds.
	dt = clock.tick(FPS) / 10000

background_color = WHITE
pygame.init()

if os.name == 'posix':
	(width, height) = (1600, 2560)
	screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
else:
	(width, height) = (800, 800)
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
	radius = 120
	for i in range(9, 10):
		angleDeg = i * angleTwelth
		my_particles.append(
			ParticleDisplayPosFromXAxis(screen=screen, x=circleX, y=radius
			, radius=radius, color=BLUE, thickness=3, angleDeg=angleDeg, speed=-HALF_GRAVITY_BY_FPS))
else:
	radius = 70
	for i in range(9, 10):
		# example: angle of 60 degrees Y axis based (i = 2) corresponds to
		# angle of 30 degrees X axis based (i = 1)
		angleDeg = i * angleTwelth
		my_particles.append(
			ParticleDisplayPosFromXAxis(screen=screen, x=circleX, y=radius, radius=radius, color=BLUE,
													   thickness=1, angleDeg=angleDeg, speed=-HALF_GRAVITY_BY_FPS))

running = True
clock = pygame.time.Clock()
timerDC = 0
dt = 0
pause = True # if True, starts by pausing the particle at screen top

screen.fill(background_color)

if os.name == 'posix':
	pygame.draw.circle(screen, BLUE, (circleX, circleY), circleR, 1)
else:
	pygame.draw.circle(screen, BLUE, (round(circleX), round(circleY)), round(circleR), 1)

# if pause == True, display the particle at screen top before looping without
# moving the particle
if pause:
	for particle in my_particles:
		particle.display()
	
pygame.display.flip()

t0 = time.time()
tt0 = t0
total = 0

if os.name == 'posix':
	textOnScreen = TextOnScreen(screen, 1100, 120, [])
	textOnScreenBounce = TextOnScreen(screen, 1100, 2450, [])
else:
	textOnScreen = TextOnScreen(screen, 550, 20, [])
	textOnScreenBounce = TextOnScreen(screen, 550, 750, [])

while running:
	if os.name == 'posix':
		clock.tick_busy_loop(FPS)
	else:
		clock.tick(FPS)
		
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN: #on Android, tap the sreen to quit
			handleDoubleClick()

	if not pause:	
		screen.fill(background_color)
		if os.name == 'posix':
			pygame.draw.circle(screen, BLUE, (circleX, circleY), circleR, 10)
		else:
			pygame.draw.circle(screen, BLUE, (round(circleX), round(circleY)), round(circleR), 1)

		#for particle in my_particles:
		particle = my_particles[0]  # currently, we investigate gravity with only
									# one particle !
		particle.moveGravity()
		#particle.bounce()
		if particle.bounceElasticity():
			pause = True
			t1 = time.time()
			total = t1-t0
			timingText = "Fall time: " + "{:.2f}".format(total) + " s"
			textLines = [timingText]
			textOnScreenBounce.addTextLines(textLines)
			t0 = t1
				
		tt1 = time.time()
		elapsedTime = tt1-tt0 + 1 / FPS
		timingText = "{:.1f}".format(elapsedTime) + " s / {:.2f}".format(particle.speed + HALF_GRAVITY_BY_FPS) + " m/s / {:.2f}".format(particle.y - radius) + " m"
		textOnScreen.addTextLine(timingText)
		particle.display()
		textOnScreen.display()
		textOnScreenBounce.display()
	
		pygame.display.flip()

		
pygame.quit()