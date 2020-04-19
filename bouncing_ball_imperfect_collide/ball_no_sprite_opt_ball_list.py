import pygame as pg
import math
from settings import *

class Ball(pg.sprite.Sprite):
	def __init__(self, 
	             screen, 
	             allBalls, 
	             index,
	             color, 
	             radius, 
	             startX, 
	             startY, 
	             speed, 
	             angle=-45):
		super().__init__()
		self.screen = screen
		self.allBalls = allBalls
		self.ballNumber = len(allBalls)
		self.index = index
		self.color = color
		rectSize = radius * 2
		self.rect = pg.Rect(startX, startY, rectSize, rectSize)
		self.speed = speed
		self.angle = math.radians(-angle)
		pg.draw.circle(self.screen, self.color, self.rect.center, int(self.rect.width / 2))

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

		for i in range(self.index + 1, self.ballNumber):
			ball = self.allBalls[i]
			if not hit_bounds and not ball is self and self.collideBall(ball):
				self.angle = self.angle - math.pi
				break

	def collideBall(self, ball):
		'''
		Returns True if self collides with ball.
		'''
		xDiff = (self.rect.centerx - ball.rect.centerx)
		yDiff = (self.rect.centery - ball.rect.centery)
		hypothenuseSquared = xDiff * xDiff + yDiff * yDiff
		sumOfRadiuses = self.rect.width / 2 + ball.rect.width / 2

		return hypothenuseSquared <= sumOfRadiuses * sumOfRadiuses

	# Draw our ball to the screen
	def draw(self):
		pg.draw.circle(self.screen, self.color, self.rect.center, int(self.rect.width / 2))
