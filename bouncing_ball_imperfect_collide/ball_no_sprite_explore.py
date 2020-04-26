import pygame as pg
import math
from collections import deque
from settings import *

class Ball(pg.sprite.Sprite):
	def __init__(self,
				 screen,
				 allBalls,
				 color,
				 radius,
				 startX,
				 startY,
				 speed,
				 angle=-45):
		super().__init__()
		self.screen = screen
		self.allBalls = allBalls
		self.color = color
		self.radius = radius
		rectSize = radius * 2
		self.rect = pg.Rect(startX, startY, rectSize, rectSize)
		self.speed = speed
		self.angle = math.radians(-angle)

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

	def update(self):
		delta_x = self.speed * math.cos(self.angle)
		delta_y = self.speed * math.sin(self.angle)
		self.rect = self.rect.move(delta_x, delta_y)
		hit_bounds = False

		if self.rect.right >= self.screen.get_width() or self.rect.left <= 0:
			self.angle = math.pi - self.angle
			hit_bounds = True

		if self.rect.top <= 0 or self.rect.bottom >= self.screen.get_height():
			self.angle = -self.angle
			hit_bounds = True

		for ball in self.allBalls:
			if not hit_bounds and not ball is self and self.collideBall(ball):
				self.angle = self.angle - math.pi
				break

	def collideBall(self, ball):
		xDiff = (self.rect.centerx - ball.rect.centerx)
		yDiff = (self.rect.centery - ball.rect.centery)
		hSquare = xDiff * xDiff + yDiff * yDiff
		radiuses = self.rect.width / 2 + ball.rect.width / 2

		return hSquare <= radiuses * radiuses

	# Draw our ball to the screen
	def draw(self):
		pg.draw.circle(self.screen, self.color, self.rect.center, int(self.rect.width / 2))

		currentX = int(self.rect.centerx)
		currentY = int(self.rect.centery)

		moveRight = (currentX - self.previousX) > 0
		moveDown = (currentY - self.previousY) > 0

		self.previousX = currentX
		self.previousY = currentY

		if self.previousMoveRight != moveRight or self.previousMoveDown != moveDown:
			# ball direction changed
			self.previousMoveRight = moveRight
			self.previousMoveDown = moveDown

			# add a new traject points list to the deque. This will remove the oldest
			# traject points list if the number of traject points list exceeds
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

		x = self.rect.centerx
		y = self.rect.centery

		if abs(x - self.previousTraceX) > BALL_TRACING_STEP_SIZE or abs(y - self.previousTraceY) > BALL_TRACING_STEP_SIZE:
			self.multipleBounceTrajectPointLists[self.currentBounceTrajectIndex].append(pg.Rect(x, y, 1, 1))
			self.previousTraceX = x
			self.previousTraceY = y

		for oneBouncesTrajectPointList in self.multipleBounceTrajectPointLists:
			for point in oneBouncesTrajectPointList:
				pg.draw.circle(self.screen, self.color, point.center, 2)

	def blitTextOnBall(self, xValue, yValue, ballDirectionMoveDown, ballDirectionMoveRight):
		textLines = [None] * self.lineNumber
		textLines[0] = 'x: ' + str(xValue) + ' ' + ('+' if ballDirectionMoveRight else '-')
		textLines[1] = 'y: ' + str(yValue) + ' ' + ('+' if ballDirectionMoveDown else '-')
		textLines[2] = 'angle: ' + str(int(math.degrees(self.angle)))

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
