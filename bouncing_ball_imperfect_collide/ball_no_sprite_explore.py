import pygame as pg
import math
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
		texthorizontalSize = self.font.size("angle: 360")[0]
		self.textLeftMargin = (self.rect.width - texthorizontalSize) / 2

		# Calculating the top margin based on the number of text lines
		self.lineNumber = 3
		self.textTopMargin = radius - (self.font_height * self.lineNumber / 2)
		self.textColor = BLACK

		self.trajectPoints = []
		self.previousX = 0
		self.previousY = 0
		self.previousSteppedX = 0
		self.previousSteppedY = 0
		self.previousMoveRight = None
		self.previousMoveDown = None
		self.directionChangeNumber = -2

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

		if hit_bounds:
			self.previousSteppedX = 0
			self.previousSteppedY = 0

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

		if self.previousMoveRight != moveRight or self.previousMoveDown != moveDown:
			# ball direction changed
			self.previousMoveRight = moveRight
			self.previousMoveDown = moveDown
			self.directionChangeNumber += 1

			if self.directionChangeNumber >= 3:
				self.trajectPoints = []
				self.directionChangeNumber = 0

		self.previousX = currentX
		self.previousY = currentY

		# Writing information on the ball surface
		textLines = [None] * self.lineNumber
		textLines[0] = 'x: ' + str(currentX) + ' ' + ('+' if moveRight else '-')
		textLines[1] = 'y: ' + str(currentY) + ' ' + ('+' if moveDown else '-')
		textLines[2] = 'angle: ' + str(int(math.degrees(self.angle)))

		self.images = []  # The text surfaces.

		for line in textLines:
			surf = self.font.render(line, True, self.textColor)
			self.images.append(surf)

		for y, surf in enumerate(self.images):
			# Don't blit below the rect area.
			if y * self.font_height + self.font_height > self.rect.h:
				break
			self.screen.blit(surf, (
			self.rect.x + self.textLeftMargin, self.rect.y + self.textTopMargin + y * self.font_height))

		angleDegree = math.degrees(self.angle)
		x = 0
		y = 0
		if moveRight and moveDown:
			a = self.radius / math.sin(self.angle) * math.cos(self.angle)
			x = self.rect.left
			y = self.rect.centery - a
		elif not moveRight and moveDown:
			calcAngleDegree = 180 - angleDegree
			angle = math.radians(calcAngleDegree)
			o = self.radius / math.cos(angle) * math.sin(angle)
			x = self.rect.right
			y = self.rect.centery - o
		elif not moveRight and not moveDown:
			a = self.radius
			o = a * math.sin(self.angle) / math.cos(self.angle)
			x = self.rect.centerx + o
			y = self.rect.centery + a
		elif moveRight and not moveDown:
			calcAngleDegree = 180 - angleDegree
			angle = math.radians(calcAngleDegree)
			o = self.radius
			a = o * math.cos(angle) / math.sin(angle)
			x = self.rect.centerx - a
			y = self.rect.centery + o

		if abs(x - self.previousSteppedX) > BALL_TRACING_STEP_SIZE and abs(y - self.previousSteppedY) > BALL_TRACING_STEP_SIZE:
			self.trajectPoints.append(pg.Rect(x, y, 2, 2))
			self.previousSteppedX = x
			self.previousSteppedY = y

		for point in self.trajectPoints:
			pg.draw.circle(self.screen, GREEN, point.center, 2)
