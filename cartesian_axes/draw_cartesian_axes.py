import pygame as pg
import math
import os
import time
from cartesianaxes import CartesianAxes

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

FPS = 10

def handleDoubleClick():
	global timerDC
	global running
	
	if timerDC == 0:
		timerDC = 0.01
		# Click again before 0.1 seconds to double click.
	elif timerDC < 0.1:
		# Double click happened
		running = False
		
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
pg.init()

if os.name == 'posix':
	(width, height) = (1600, 2560)
	screen = pg.display.set_mode((width, height), pg.FULLSCREEN)
else:
	(width, height) = (800, 800)
	os.environ['SDL_VIDEO_WINDOW_POS'] = '100,15'
	screen = pg.display.set_mode((width, height))

pg.display.set_caption('Cartesian axis')
(w, h) = screen.get_size()

running = True
clock = pg.time.Clock()
timerDC = 0
dt = 0

screen.fill(background_color)
cartesianAxesLst = []

if os.name == 'posix':
	cartesianAxesLst.append(CartesianAxes(screen=screen, origin=(100,500), xLength=200, yLength=500, xRange=(-5, 15), yRange=(50, -3)))
	cartesianAxesLst.append(CartesianAxes(screen=screen, origin=(400,500), xLength=200, yLength=500, xRange=(-5, 15), yRange=(20, -50), xLabel='Time', yLabel='Speed'))
	cartesianAxesLst.append(CartesianAxes(screen=screen, origin=(120,1100), xLength=200, yLength=500, xRange=(25, 55), yRange=(50, -3)))
	cartesianAxesLst.append(CartesianAxes(screen=screen, origin=(420,1100), xLength=200, yLength=500, xRange=(-55, -5), yRange=(50, -3)))
	cartesianAxesLst.append(CartesianAxes(screen=screen, origin=(780,1100), xLength=200, yLength=500, xRange=(0, 15), yRange=(50, 3)))
#origin, xLength, yLength, xRange, yRange, xLabel='X', yLabel='Y', color=BLACK, thickness=2, leftMargin=0, topMargin=0):
else:
	cartesianAxesLst.append(CartesianAxes(screen=screen, origin=(80,300), xLength=200, yLength=300, xRange=(-5, 15), yRange=(50, -3)))
	cartesianAxesLst.append(CartesianAxes(screen=screen, origin=(500,300), xLength=200, yLength=300, xRange=(-5, 15), yRange=(50, -3), xLabel='Time', yLabel='Speed'))
	cartesianAxesLst.append(CartesianAxes(screen=screen, origin=(40,700), xLength=200, yLength=300, xRange=(25, 55), yRange=(50, -3)))
	cartesianAxesLst.append(CartesianAxes(screen=screen, origin=(550,720), xLength=200, yLength=300, xRange=(0, 15), yRange=(50, 9)))

while running:
	clock.tick(FPS)
		
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		elif event.type == pg.MOUSEBUTTONDOWN: #on Android, tap the sreen to quit
			handleDoubleClick()

	screen.fill(background_color)
	
	for cartesianAxes in cartesianAxesLst:
		cartesianAxes.draw()
	
	pg.display.flip()

		
pg.quit()