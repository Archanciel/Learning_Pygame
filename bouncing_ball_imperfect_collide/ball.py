import pygame as pg
import math
from collections import deque
import os
import copy

from settings import *

class Ball():
	def __init__(self,
				 game,
				 allBalls,
				 color,
				 radius,
				 startX,
				 startY,
				 speed,
				 angle=45):
		self.game = game
		self.screen = game.screen
		self.allBalls = allBalls
		self.color = color
		self.radius = radius

		# will store the exact baLl center float tuple. Pygame rect only stores
		# integers
		self.ballCenterFloat = (startX + radius, startY + radius)
		
		self.speed = speed
		self.angleRadian = math.radians(angle)

		self.currentX = 0
		self.currentY = 0
		self.previousX = 0
		self.previousY = 0
		self.currentMoveRight = None
		self.currentMoveDown = None
		self.previousMoveRight = None
		self.previousMoveDown = None

	def update(self):
		deltaX = self.speed * math.cos(self.angleRadian)
		deltaY = self.speed * math.sin(self.angleRadian)

		# minus deltaY since the y coordinate of screen top is 0 !
		self.ballCenterFloat = (self.ballCenterFloat[0] + deltaX, self.ballCenterFloat[1] - deltaY)

		hit_bounds = False

		if self.ballCenterFloat[0] + self.radius >= self.screen.get_width():
			self.angleRadian = math.pi - self.angleRadian
			if self.angleRadian > 2 * math.pi:
				# if not done, angleRadian continue to increase, which corrupts the display of ball
				# angle in degree
				self.angleRadian = self.angleRadian - (2 * math.pi)
			hit_bounds = True

			# storing bounce mark location coordinates
			self.storeBounceLocationData(self.screen.get_width(), self.ballCenterFloat[1], BOUNCE_ARROW_RIGHT)

		if self.ballCenterFloat[0] - self.radius <= 0:
			self.angleRadian = math.pi - self.angleRadian
			if self.angleRadian > 2 * math.pi:
				# if not done, angleRadian continue to increase, which corrupts the display of ball
				# angle in degree
				self.angleRadian = self.angleRadian - (2 * math.pi)
			hit_bounds = True

			# storing bounce mark location coordinates
			self.storeBounceLocationData(0, self.ballCenterFloat[1], BOUNCE_ARROW_LEFT)

		if self.ballCenterFloat[1] - self.radius <= 0:
			self.angleRadian = -self.angleRadian
			hit_bounds = True

			# storing bounce mark location coordinates
			self.storeBounceLocationData(self.ballCenterFloat[0], 0, BOUNCE_ARROW_TOP)

		if self.ballCenterFloat[1] + self.radius >= self.screen.get_height():
			self.angleRadian = -self.angleRadian
			hit_bounds = True

			# storing bounce mark location coordinates
			self.storeBounceLocationData(self.ballCenterFloat[0], self.screen.get_height(), BOUNCE_ARROW_BOTTOM)

		for ball in self.allBalls:
			if not hit_bounds and not ball is self and self.collideBall(ball):
				self.angleRadian = self.computeCollideAngleOpposite()
				if self.angleRadian < (-2 * math.pi):
					# if not done, angleRadian continue to increase, which corrupts the display of ball
					# angle in degree
					self.angleRadian = self.angleRadian + (2 * math.pi)
				if PAUSE_ON_COLLIDE:
					self.game.pause = True
				break

	def storeBounceLocationData(self, bounceX, bounceY, bounceDirection):
		# storing bounce mark location coordinates, implemented by sub classes
		pass

	def computeCollideAngleOpposite(self):
		return self.angleRadian - math.pi
		
	def collideBall(self, ball):
		xDiff = self.ballCenterFloat[0] - ball.ballCenterFloat[0]
		yDiff = self.ballCenterFloat[1] - ball.ballCenterFloat[1]
		hSquare = xDiff * xDiff + yDiff * yDiff
		radiuses = self.radius + ball.radius

		return hSquare <= radiuses * radiuses

	# Draw our ball to the screen
	def draw(self):
		if os.name == 'posix':
			pg.draw.circle(self.screen, self.color, (self.ballCenterFloat[0], self.ballCenterFloat[1]), self.radius)
		else:
			pg.draw.circle(self.screen, self.color, (round(self.ballCenterFloat[0]), round(self.ballCenterFloat[1])), self.radius)

		self.currentX = self.ballCenterFloat[0]
		self.currentY = self.ballCenterFloat[1]

		self.currentMoveRight = self.previousMoveRight
		self.currentMoveDown = (self.currentY - self.previousY) > 0

		if (self.currentX - self.previousX) == 0 and (self.currentY - self.previousY) == 0:
			# the case after double click to stop the balls
			self.currentMoveDown = self.previousMoveDown
		else:
			self.currentMoveRight = (self.currentX - self.previousX) > 0

			self.previousX = self.currentX
			self.previousY = self.currentY
