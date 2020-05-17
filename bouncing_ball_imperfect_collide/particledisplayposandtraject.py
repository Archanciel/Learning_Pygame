import pygame as pg
import math
from collections import deque

from particledisplaypos import ParticleDisplayPos

BLACK = (0, 0, 0)
RED = (255, 0, 0)

#bounce tracing constants

MAX_BOUNCE_TRAJECTS = 4 # number of ball trajects to display
BALL_TRACING_POINT_SIZE = 2
BALL_TRACING_STEP_SIZE = 10 # defines the number of pixels after which a tracing point is drawned on screen

#bounce mark constants

DRAW_BOUNCE_LOCATION = False
BOUNCE_ARROW_TOP = 2
BOUNCE_ARROW_RIGHT = 3
BOUNCE_ARROW_BOTTOM = 4
BOUNCE_ARROW_LEFT = 5

ARROW_DIM_1 = 7
ARROW_DIM_2 = 14
ARROW_WIDTH = 1

class ParticleDisplayPosAndTraject(ParticleDisplayPos):
	def __init__(self, screen, x, y, radius, colour, thickness, angleDeg, speed, bouncePointColor=RED):
		# angleDeg is the clockwise angle with 0 deg corresponding to 12 hour
		super().__init__(screen, x, y, radius, colour, thickness, angleDeg, speed)

		# Traject tracing instance variables
		self.previousX = 0
		self.previousY = 0
		self.previousMoveRight = None
		self.previousMoveDown = None
		self.multipleBounceTrajectPointLists = deque(maxlen=MAX_BOUNCE_TRAJECTS)
		self.previousTraceX = 0
		self.previousTraceY = 0
		self.currentBounceTrajectIndex = -1

		# Bounce mark instance variables
		self.bouncePointColor = bouncePointColor
		self.bounceMarkX = None
		self.bounceMarkY = None
		self.bounceMarkDirection = None

	def display(self):
		super().display()

		self.storeBallTrajectData()

		# handling ball bounce location tracing

		if DRAW_BOUNCE_LOCATION:
			self.storeBallBounceMarkData()

		self.drawBallTrajectAndBounceMark()

	def drawBallTrajectAndBounceMark(self):
		for oneBouncesTrajectPointList in self.multipleBounceTrajectPointLists:
			for point in oneBouncesTrajectPointList:
				if point.width > 1:
					# indicates that this point is a bounce mark location on the screen limits.
					# The bounce mark direction is coded in the point.width !
					self.drawBounceMark(bounceLocX=point.x, bounceLocY=point.y, bounceMarkDirection=point.width)
				else:
					# ball traject is drawned using 1 pixel points, i.e circles
					pg.draw.circle(self.screen, self.colour, point.center, BALL_TRACING_POINT_SIZE)

	def storeBallBounceMarkData(self):
		if self.bounceMarkDirection != None:
			# we use the Rect.width (and height) property to code the type of draw bounce mark type
			self.multipleBounceTrajectPointLists[self.currentBounceTrajectIndex].append(
				pg.Rect(round(self.bounceMarkX), round(self.bounceMarkY), self.bounceMarkDirection,
						self.bounceMarkDirection))

	def storeBallTrajectData(self):
		'''
		This method stores ball traject tracing data.

		:return:
		'''
		currentMoveDown = (self.y - self.previousY) > 0
		currentMoveRight = (self.x - self.previousX) > 0

		self.previousX = self.x
		self.previousY = self.y

		if self.previousMoveRight != currentMoveRight or self.previousMoveDown != currentMoveDown:
			# ball direction changed
			self.previousMoveRight = currentMoveRight
			self.previousMoveDown = currentMoveDown

			# add a new traject point list to the deque. This will remove the oldest
			# traject point list if the number of traject point list exceeds
			# MAX_BOUNCE_TRAJECTS
			self.multipleBounceTrajectPointLists.append([])
			self.currentBounceTrajectIndex += 1

			if self.currentBounceTrajectIndex >= MAX_BOUNCE_TRAJECTS:
				# since the new traject points list is added at the right of the deque,
				# the currentBounceTrajectIndex must be set to the max deque size - 1
				self.currentBounceTrajectIndex = MAX_BOUNCE_TRAJECTS - 1
		
		if abs(self.x - self.previousTraceX) > BALL_TRACING_STEP_SIZE or abs(
				self.y - self.previousTraceY) > BALL_TRACING_STEP_SIZE:
			self.multipleBounceTrajectPointLists[self.currentBounceTrajectIndex].append(
				pg.Rect(round(self.x), round(self.y), 1, 1))
			self.previousTraceX = self.x
			self.previousTraceY = self.y

	def drawBounceMark(self, bounceLocX, bounceLocY, bounceMarkDirection):
		if bounceMarkDirection == BOUNCE_ARROW_TOP:
			pg.draw.line(self.screen, self.bouncePointColor, (bounceLocX, bounceLocY),
						 (bounceLocX - ARROW_DIM_1, bounceLocY + ARROW_DIM_2), ARROW_WIDTH)
			pg.draw.line(self.screen, self.bouncePointColor, (bounceLocX, bounceLocY),
						 (bounceLocX + ARROW_DIM_1, bounceLocY + ARROW_DIM_2), ARROW_WIDTH)
		elif bounceMarkDirection == BOUNCE_ARROW_RIGHT:
			pg.draw.line(self.screen, self.bouncePointColor, (bounceLocX, bounceLocY),
						 (bounceLocX - ARROW_DIM_2, bounceLocY - ARROW_DIM_1), ARROW_WIDTH)
			pg.draw.line(self.screen, self.bouncePointColor, (bounceLocX, bounceLocY),
						 (bounceLocX - ARROW_DIM_2, bounceLocY + ARROW_DIM_1), ARROW_WIDTH)
		elif bounceMarkDirection == BOUNCE_ARROW_BOTTOM:
			pg.draw.line(self.screen, self.bouncePointColor, (bounceLocX, bounceLocY),
						 (bounceLocX - ARROW_DIM_1, bounceLocY - ARROW_DIM_2), ARROW_WIDTH)
			pg.draw.line(self.screen, self.bouncePointColor, (bounceLocX, bounceLocY),
						 (bounceLocX + ARROW_DIM_1, bounceLocY - ARROW_DIM_2), ARROW_WIDTH)
		else:  # BOUNCE_ARROW_LEFT
			pg.draw.line(self.screen, self.bouncePointColor, (bounceLocX, bounceLocY),
						 (bounceLocX + ARROW_DIM_2, bounceLocY - ARROW_DIM_1), ARROW_WIDTH)
			pg.draw.line(self.screen, self.bouncePointColor, (bounceLocX, bounceLocY),
						 (bounceLocX + ARROW_DIM_2, bounceLocY + ARROW_DIM_1), ARROW_WIDTH)
