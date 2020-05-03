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
				 bouncePointColor,
				 radius,
				 startX,
				 startY,
				 speed,
				 angle=45):
		super().__init__()
		self.game = game
		self.screen = game.screen
		self.allBalls = allBalls
		self.color = color
		self.bouncePointColor = bouncePointColor
		self.radius = radius
		rectSize = radius * 2
		
		# will store the exact baLl center float tuple. Pygame rect only stores
		# integers
		self.ballCenterFloat = (startX + radius, startY + radius)
		
		self.speed = speed
		self.angleRadian = math.radians(angle)

		# Position related instance variables
		self.font = pg.font.Font(None, 32)
		self.font_height = self.font.get_linesize()

		# Calculating the left margin based on longest possible text
		self.textHorizontalSize = self.font.size("angle: 360")[0]
		self.textLeftMargin = (rectSize - self.textHorizontalSize) / 2

		# Calculating the top margin based on the number of text lines
		self.lineNumber = 3
		self.textTopMargin = radius - (self.font_height * self.lineNumber / 2)
		self.textColor = BLACK

		self.multipleBounceTrajectPointLists = deque(maxlen=MAX_BOUNCE_TRAJECTS)
		self.previousX = 0
		self.previousY = 0
		self.previousTraceX = 0
		self.previousTraceY = 0
		self.previousMoveRight = None
		self.previousMoveDown = None
		self.currentBounceTrajectIndex = -1

		self.bounceX = None
		self.bounceY = None
		self.bounceMarkDirection = None

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
			
			# storing bounce location coordinates
			self.bounceX = self.screen.get_width()
			self.bounceY = self.ballCenterFloat[1]
			self.bounceMarkDirection = BOUNCE_ARROW_RIGHT

		if self.ballCenterFloat[0] - self.radius <= 0:
			self.angleRadian = math.pi - self.angleRadian
			if self.angleRadian > 2 * math.pi:
				# if not done, angleRadian continue to increase, which corrupts the display of ball
				# angle in degree
				self.angleRadian = self.angleRadian - (2 * math.pi)
			hit_bounds = True
			
			# storing bounce location coordinates
			self.bounceX = 0
			self.bounceY = self.ballCenterFloat[1]
			self.bounceMarkDirection = BOUNCE_ARROW_LEFT

		if self.ballCenterFloat[1] - self.radius <= 0:
			self.angleRadian = -self.angleRadian
			hit_bounds = True
			
			# storing bounce location coordinates
			self.bounceX = self.ballCenterFloat[0]
			self.bounceY = 0
			self.bounceMarkDirection = BOUNCE_ARROW_TOP

		if self.ballCenterFloat[1] + self.radius >= self.screen.get_height():
			self.angleRadian = -self.angleRadian
			hit_bounds = True
			
			# storing bounce location coordinates
			self.bounceX = self.ballCenterFloat[0]
			self.bounceY = self.screen.get_height()
			self.bounceMarkDirection = BOUNCE_ARROW_BOTTOM

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

		currentX = self.ballCenterFloat[0]
		currentY = self.ballCenterFloat[1]

		if (currentX - self.previousX) == 0 and (currentY - self.previousY) == 0:
			# the case after double click to stop the balls
			moveRight = self.previousMoveRight
			moveDown = self.previousMoveDown
		else:
			moveRight = (currentX - self.previousX) > 0
			moveDown = (currentY - self.previousY) > 0

			self.previousX = currentX
			self.previousY = currentY

		if self.previousMoveRight != moveRight or self.previousMoveDown != moveDown:
			# ball direction changed
			self.previousMoveRight = moveRight
			self.previousMoveDown = moveDown

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
			self.blitTextOnBall(round(currentX, 2), round(currentY, 2), moveDown, moveRight)

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

		if abs(x - self.previousTraceX) > BALL_TRACING_STEP_SIZE or abs(y - self.previousTraceY) > BALL_TRACING_STEP_SIZE:
			self.multipleBounceTrajectPointLists[self.currentBounceTrajectIndex].append(pg.Rect(round(x), round(y), 1, 1))
			self.previousTraceX = x
			self.previousTraceY = y

		# handling ball bounce location tracing
		if DRAW_BOUNCE_LOCATION:
			if self.bounceMarkDirection != None:
				# we use the Rect.width (and height) to code the type of draw bounce mark type
				self.multipleBounceTrajectPointLists[self.currentBounceTrajectIndex].append(pg.Rect(round(self.bounceX), round(self.bounceY), self.bounceMarkDirection, self.bounceMarkDirection))

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
			pg.draw.line(self.screen, self.bouncePointColor, (bounceLocX, bounceLocY), (bounceLocX - ARROW_DIM_1, bounceLocY + ARROW_DIM_2), ARROW_WIDTH)
			pg.draw.line(self.screen, self.bouncePointColor, (bounceLocX, bounceLocY), (bounceLocX + ARROW_DIM_1, bounceLocY + ARROW_DIM_2), ARROW_WIDTH)
		elif bounceMarkDirection == BOUNCE_ARROW_RIGHT:
			pg.draw.line(self.screen, self.bouncePointColor, (bounceLocX, bounceLocY), (bounceLocX - ARROW_DIM_2, bounceLocY - ARROW_DIM_1), ARROW_WIDTH)
			pg.draw.line(self.screen, self.bouncePointColor, (bounceLocX, bounceLocY), (bounceLocX - ARROW_DIM_2, bounceLocY + ARROW_DIM_1), ARROW_WIDTH)
		elif bounceMarkDirection == BOUNCE_ARROW_BOTTOM:
			pg.draw.line(self.screen, self.bouncePointColor, (bounceLocX, bounceLocY), (bounceLocX - ARROW_DIM_1, bounceLocY - ARROW_DIM_2), ARROW_WIDTH)
			pg.draw.line(self.screen, self.bouncePointColor, (bounceLocX, bounceLocY), (bounceLocX + ARROW_DIM_1, bounceLocY - ARROW_DIM_2), ARROW_WIDTH)
		else: # BOUNCE_ARROW_LEFT
			pg.draw.line(self.screen, self.bouncePointColor, (bounceLocX, bounceLocY), (bounceLocX + ARROW_DIM_2, bounceLocY - ARROW_DIM_1), ARROW_WIDTH)
			pg.draw.line(self.screen, self.bouncePointColor, (bounceLocX, bounceLocY), (bounceLocX + ARROW_DIM_2, bounceLocY + ARROW_DIM_1), ARROW_WIDTH)

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
			textCoordinatesTuple = (self.ballCenterFloat[0] - self.radius + self.textLeftMargin, self.ballCenterFloat[1] - self.radius + self.textTopMargin + y * self.font_height)
			self.screen.blit(textSurface, textCoordinatesTuple)
