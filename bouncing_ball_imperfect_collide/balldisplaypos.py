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
		self.bouncePointColor = bouncePointColor

		# Position related instance variables
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

		self.multipleBounceTrajectPointLists = deque(maxlen=MAX_BOUNCE_TRAJECTS)
		self.previousTraceX = 0
		self.previousTraceY = 0
		self.currentBounceTrajectIndex = -1

		self.bounceMarkX = None
		self.bounceMarkY = None
		self.bounceMarkDirection = None

	def storeBounceLocationData(self, bounceX, bounceY, bounceDirection):
		self.bounceMarkX = bounceX
		self.bounceMarkY = bounceY
		self.bounceMarkDirection = bounceDirection

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
		super().draw()

		if self.previousMoveRight != self.currentMoveRight or self.previousMoveDown != self.currentMoveDown:
			# ball direction changed
			self.previousMoveRight = self.currentMoveRight
			self.previousMoveDown = self.currentMoveDown

			# add a new traject point list to the deque. This will remove the oldest
			# traject point list if the number of traject point list exceeds
			# MAX_BOUNCE_TRAJECTS
			self.multipleBounceTrajectPointLists.append([])
			self.currentBounceTrajectIndex += 1

			if self.currentBounceTrajectIndex >= MAX_BOUNCE_TRAJECTS:
				# since the new traject points list is added at the right of the deque,
				# the currentBounceTrajectIndex must be set to the max deque size - 1
				self.currentBounceTrajectIndex = MAX_BOUNCE_TRAJECTS - 1

		# Writing information on the ball surface if the ball size is large enough
		if self.textHorizontalSize <= self.radius * 2:
			self.blitTextOnBall(round(self.currentX, 2), round(self.currentY, 2), self.currentMoveDown, self.currentMoveRight)

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

		# handling ball traject tracing

		x = self.ballCenterFloat[0]
		y = self.ballCenterFloat[1]

		if abs(x - self.previousTraceX) > BALL_TRACING_STEP_SIZE or abs(
				y - self.previousTraceY) > BALL_TRACING_STEP_SIZE:
			self.multipleBounceTrajectPointLists[self.currentBounceTrajectIndex].append(
				pg.Rect(round(x), round(y), 1, 1))
			self.previousTraceX = x
			self.previousTraceY = y

		# handling ball bounce location tracing
		if DRAW_BOUNCE_LOCATION:
			if self.bounceMarkDirection != None:
				# we use the Rect.width (and height) to code the type of draw bounce mark type
				self.multipleBounceTrajectPointLists[self.currentBounceTrajectIndex].append(
					pg.Rect(round(self.bounceMarkX), round(self.bounceMarkY), self.bounceMarkDirection,
							self.bounceMarkDirection))

		for oneBouncesTrajectPointList in self.multipleBounceTrajectPointLists:
			for point in oneBouncesTrajectPointList:
				if point.width > 1:
					# indicates that this point is a bounce mark location on the screen limits.
					# The bounce mark direction is coded in the point.width !
					self.drawBounceMark(bounceLocX=point.x, bounceLocY=point.y, bounceMarkDirection=point.width)
				else:
					pg.draw.circle(self.screen, self.color, point.center, 1)

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
