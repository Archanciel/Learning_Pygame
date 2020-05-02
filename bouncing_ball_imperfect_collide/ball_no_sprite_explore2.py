import pygame as pg
import math
from collections import deque
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
		self.rect = pg.Rect(startX, startY, rectSize, rectSize)
		
		# will store the exact baLl center float tuple. Pygame rect only stores
		# integers
		self.ballCenterFloat = self.rect.center
		
		self.speed = speed
		self.angleRadian = math.radians(angle)

		# Position related instance variables
		self.font = pg.font.Font(None, 32)
		self.font_height = self.font.get_linesize()

		# Calculating the left margin based on longest possible text
		self.textHorizontalSize = self.font.size("angle: 360")[0]
		self.textLeftMargin = (self.rect.width - self.textHorizontalSize) / 2

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
		
		self.rect.center = (round(self.ballCenterFloat[0]), round(self.ballCenterFloat[1]))
		hit_bounds = False

		if self.rect.right >= self.screen.get_width():
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

		if self.rect.left <= 0:
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

		if self.rect.top <= 0:
			self.angleRadian = -self.angleRadian
			hit_bounds = True
			
			# storing bounce location coordinates
			self.bounceX = self.ballCenterFloat[0]
			self.bounceY = 0
			self.bounceMarkDirection = BOUNCE_ARROW_TOP

		if self.rect.bottom >= self.screen.get_height():
			self.angleRadian = -self.angleRadian
			hit_bounds = True
			
			# storing bounce location coordinates
			self.bounceX = self.ballCenterFloat[0]
			self.bounceY = self.screen.get_height()
			self.bounceMarkDirection = BOUNCE_ARROW_BOTTOM

		for ball in self.allBalls:
			if not hit_bounds and not ball is self and self.collideBall(ball):
				self.angleRadian = self.computeCollideAngleOpposite()
				#self.angleRadian = self.computeCollideAnglePhysic2(ball)
				if self.angleRadian < (-2 * math.pi):
					# if not done, angleRadian continue to increase, which corrupts the display of ball
					# angle in degree
					self.angleRadian = self.angleRadian + (2 * math.pi)
				if PAUSE_ON_COLLIDE:
					self.game.pause = True
				break

	def computeCollideAngleOpposite(self):
		return self.angleRadian - math.pi

	def computeCollideAnglePhysic(self, collideBall):
		x = collideBall.ballCenterFloat[0] - self.ballCenterFloat[0]
		y = - collideBall.ballCenterFloat[1] + collideBall.ballCenterFloat[1]
		tangentAngleRadian = math.acos(x / math.sqrt((x * x) + (y * y)))
		epsilon = 2 * math.pi - self.angleRadian
		
		return (2 * tangentAngleRadian) + epsilon
				
	def computeCollideAnglePhysic2(self, collideBall):
		x = collideBall.ballCenterFloat[0] - self.ballCenterFloat[0]
		y = - collideBall.ballCenterFloat[1] + collideBall.ballCenterFloat[1]
		tangentAngleRadian = math.acos(x / math.sqrt((x * x) + (y * y)))
		
		return (2 * tangentAngleRadian) - self.angleRadian
				
	def collideBall(self, ball):
		xDiff = (self.rect.centerx - ball.rect.centerx)
		yDiff = (self.rect.centery - ball.rect.centery)
		hSquare = xDiff * xDiff + yDiff * yDiff
		radiuses = self.rect.width / 2 + ball.rect.width / 2

		return hSquare <= radiuses * radiuses

	# Draw our ball to the screen
	def draw(self):
		pg.draw.circle(self.screen, self.color, self.rect.center, int(self.rect.width / 2))

		currentX = round(self.ballCenterFloat[0], 2)
		currentY = round(self.ballCenterFloat[1], 2)

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
		if self.textHorizontalSize <= self.rect.width:
			self.blitTextOnBall(currentX, currentY, moveDown, moveRight)

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

		x = self.rect.centerx
		y = self.rect.centery

		if abs(x - self.previousTraceX) > BALL_TRACING_STEP_SIZE or abs(y - self.previousTraceY) > BALL_TRACING_STEP_SIZE:
			self.multipleBounceTrajectPointLists[self.currentBounceTrajectIndex].append(pg.Rect(x, y, 1, 1))
			self.previousTraceX = x
			self.previousTraceY = y

		# handling ball bounce location tracing
		if DRAW_BOUNCE_LOCATION:
			if self.bounceMarkDirection != None:
				self.multipleBounceTrajectPointLists[self.currentBounceTrajectIndex].append(pg.Rect(self.bounceX, self.bounceY, self.bounceMarkDirection, self.bounceMarkDirection))

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
			if y * self.font_height + self.font_height > self.rect.h:
				# Don't blit below the rect area.
				break
			textCoordinatesTuple = (self.rect.x + self.textLeftMargin, self.rect.y + self.textTopMargin + y * self.font_height)
			self.screen.blit(textSurface, textCoordinatesTuple)
