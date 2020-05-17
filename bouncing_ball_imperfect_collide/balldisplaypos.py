import pygame as pg
import math
from collections import deque
import os

from ball import Ball

from settings import *

class BallDisplayPos(Ball):
	def __init__(self,
				 game,
				 allBalls,
				 color,
				 bouncePointColor,
				 radius,
				 startX,
				 startY,
				 speed,
				 angle=45):
		super().__init__(game,
				 allBalls,
				 color,
				 radius,
				 startX,
				 startY,
				 speed,
				 angle)

		# Pos display related instance variables
		self.font = pg.font.Font(None, 32)
		self.font_height = self.font.get_linesize()

		# Calculating the left margin based on longest possible text
		rectSize = radius * 2
		self.textHorizontalSize = self.font.size("angle: 360")[0]
		self.textLeftMargin = (rectSize - self.textHorizontalSize) / 2

		# Calculating the top margin based on the number of text lines
		self.lineNumber = 3
		self.textTopMargin = radius - (self.font_height * self.lineNumber / 2)
		self.textColor = BLACK

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

	def storeBounceLocationData(self, bounceX, bounceY, bounceDirection):
		self.bounceMarkX = bounceX
		self.bounceMarkY = bounceY
		self.bounceMarkDirection = bounceDirection

	# Draw our ball to the screen
	def draw(self):
		super().draw()

		currentMoveDown, currentMoveRight = self.storeBallTrajectData()

		# Writing information on the ball surface if the ball size is large enough
		if self.textHorizontalSize <= self.radius * 2:
			self.blitTextOnBall(round(self.ballCenterFloat[0], 2), round(self.ballCenterFloat[1], 2), currentMoveDown, currentMoveRight)

		# angleDegree = math.degrees(self.angle)
		# x = 0
		# y = 0
		#
		# if moveRight and moveDown:
		# 	a = self.radius / math.sin(self.angle) * math.cos(self.angle)
		# 	x = self.rect.left
		# 	y = self.rect.centery - a
		# elif not moveRight and moveDown:
		# 	calcAngleDegree = 180 - angleDegree
		# 	angle = math.radians(calcAngleDegree)
		# 	o = self.radius / math.cos(angle) * math.sin(angle)
		# 	x = self.rect.right
		# 	y = self.rect.centery - o
		# elif not moveRight and not moveDown:
		# 	a = self.radius
		# 	o = a * math.sin(self.angle) / math.cos(self.angle)
		# 	x = self.rect.centerx + o
		# 	y = self.rect.centery + a
		# elif moveRight and not moveDown:
		# 	calcAngleDegree = 180 - angleDegree
		# 	angle = math.radians(calcAngleDegree)
		# 	o = self.radius
		# 	a = o * math.cos(angle) / math.sin(angle)
		# 	x = self.rect.centerx - a
		# 	y = self.rect.centery + o

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
					pg.draw.circle(self.screen, self.color, point.center, 1)

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

		currentMoveDown = (self.ballCenterFloat[1] - self.previousY) > 0
		currentMoveRight = (self.ballCenterFloat[0] - self.previousX) > 0

		self.previousX = self.ballCenterFloat[0]
		self.previousY = self.ballCenterFloat[1]

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

		if abs(self.ballCenterFloat[0] - self.previousTraceX) > BALL_TRACING_STEP_SIZE or abs(
				self.ballCenterFloat[1] - self.previousTraceY) > BALL_TRACING_STEP_SIZE:
			self.multipleBounceTrajectPointLists[self.currentBounceTrajectIndex].append(
				pg.Rect(round(self.ballCenterFloat[0]), round(self.ballCenterFloat[1]), 1, 1))
			self.previousTraceX = self.ballCenterFloat[0]
			self.previousTraceY = self.ballCenterFloat[1]
			
		return currentMoveDown, currentMoveRight

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

	def blitTextOnBall(self, xValue, yValue, ballDirectionMoveDown, ballDirectionMoveRight):
		textLines = [None] * self.lineNumber
		textLines[0] = 'x: ' + str(xValue) + ' ' + ('+' if ballDirectionMoveRight else '-')
		textLines[1] = 'y: ' + str(yValue) + ' ' + ('+' if ballDirectionMoveDown else '-')

		if (self.angleRadian < 0):
			# negative degrees are nonsensical !
			angleDegree = round(math.degrees(2 * math.pi + self.angleRadian))
		else:
			angleDegree = round(math.degrees(self.angleRadian))

		textLines[2] = 'angle: ' + str(angleDegree)

		self.images = []  # The text surfaces.

		for line in textLines:
			textSurface = self.font.render(line, True, self.textColor)
			self.images.append(textSurface)
		for y, textSurface in enumerate(self.images):
			if y * self.font_height + self.font_height > (2 * self.radius):
				# Don't blit below the rect area.
				break
			textCoordinatesTuple = (self.ballCenterFloat[0] - self.radius + self.textLeftMargin,
									self.ballCenterFloat[1] - self.radius + self.textTopMargin + y * self.font_height)
			self.screen.blit(textSurface, textCoordinatesTuple)
