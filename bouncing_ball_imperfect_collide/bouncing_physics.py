# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 1
# Video link: https://www.youtube.com/watch?v=uWvb3QzA48c
# Project setup

import pygame as pg
import os, random

from ball_no_sprite_explore import Ball
from settings import *
import math

COLORS = [WHITE, RED, GREEN, BLUE, YELLOW]

firstBall = True
secondBall = False

class Game:	 
	def __init__(self):
		'''
		Initializes game window, etc.
		'''
		# setting Pygame window position
		self.clock = pg.time.Clock()
		self.timerDC = 0
		self.dt = 0

		if os.name == 'posix':
			self.fps = FPS
		else:
			self.fps = FPS / 2

		os.environ['SDL_VIDEO_WINDOW_POS'] = WINDOWS_LOCATION

		pg.init()

		width = 0
		height = 0

		if os.name == 'posix':
			width = TABLET_WIDTH
			height = TABLET_HEIGHT
		else:
			width = PC_WIDTH
			height = PC_HEIGHT

		self.screen = pg.display.set_mode((width, height))
		pg.display.set_caption(TITLE)
		self.playing = False
		self.running = True

		self.allBalls = None
		self.trajectPoints = []
		self.previousX = 0
		self.previousY = 0

	def new(self):
		'''
		Starts a new game.
		'''

		# Create multiple sprite Ball instances
		self.allBalls = []

		# first ball

		if firstBall:

			if os.name == 'posix':
				ball = Ball(screen=self.screen,
							allBalls=self.allBalls,
							color=YELLOW,
							bouncePointColor=RED,
							radius=200,
							startX=550,
							startY=600,
							speed=1,
							angle=1)
			else:
				ball = Ball(screen=self.screen,
							allBalls=self.allBalls,
							color=YELLOW,
							bouncePointColor=RED,
							radius=70,
							startX=200,
							startY=500,
							speed=2,
							angle=45)

			self.allBalls.append(ball)

		# second ball

		if secondBall:
			if os.name == 'posix':
				ball = Ball(screen=self.screen,
							allBalls=self.allBalls,
							color=GREEN,
							bouncePointColor=CYAN,
							radius=30,
							startX=100,
							startY=1700,
							speed=8,
							angle=45)
			else:
				ball = Ball(screen=self.screen,
							allBalls=self.allBalls,
							color=GREEN,
							bouncePointColor=CYAN,
							radius=70,
							startX=150,
							startY=100,
							speed=2,
							angle=-15)

			self.allBalls.append(ball)

	def run(self):
		'''
		Is the game loop.
		'''
		self.playing = True
		self.pause = False

		while self.playing:
			self.clock.tick(self.fps)
			self.handleEvents()

			if not self.pause:
				self.update()

			self.draw()
			self.updateTimerForDoubleClick()

	def handleEvents(self):
		'''
		Acquires and handles events.
		'''
		for event in pg.event.get():
			# check for closing window
			if event.type == pg.QUIT:
				if self.playing:
					self.playing = False
				self.running = False
			elif event.type == pg.MOUSEBUTTONDOWN: #on Android, tap the sreen to quit
				self.handleDoubleClick()

	def updateTimerForDoubleClick(self):
		# Increase timerDC after mouse was pressed the first time.
		if self.timerDC != 0:
			self.timerDC += self.dt

		# Reset after 0.5 seconds.
		if self.timerDC >= 0.1:
			self.timerDC = 0

		# dt == time in seconds since last tick.
		# / 1000 to convert milliseconds to 10th of seconds.
		self.dt = self.clock.tick(FPS) / 10000

	def handleDoubleClick(self):
		if self.timerDC == 0:
			self.timerDC = 0.01
			# Click again before 0.1 seconds to double click.
		elif self.timerDC < 0.1:
			# Double click happened
			if not self.pause:
				self.pause = True
			else:
				self.pause = False
			'''
			if self.playing:
				self.playing = False
				
			self.running = False
			'''
	def update(self):
		'''
		Updates all game objects.
		'''
		for ball in self.allBalls:
			ball.update()

	def draw(self):
		'''
		Redraws all game objects.
		'''
		self.screen.fill(BLACK)

		for ball in self.allBalls:
			ball.draw()
			
		pg.draw.line(self.screen, RED, (0, self.screen.get_height() - 20), 
					(57, self.screen.get_height() - 21), 1)

		# *after* drawing everything, flip the display
		pg.display.flip()

	def show_start_screen(self):
		'''
		Shows game splash/start screen.
		'''
		pass

	def show_go_screen(self):
		'''
		Shows game over screen.
		'''
		pass

g = Game()
g.show_start_screen()

while g.running:
	g.new()
	g.run()
	g.show_go_screen()

pg.quit()