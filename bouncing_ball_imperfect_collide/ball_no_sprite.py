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
				
		for ball in self.allBalls:
			if not hit_bounds and not ball is self and self.rect.colliderect(ball.rect):
				self.angle = self.angle - math.pi
				break
				
	# Draw our ball to the screen
	def draw(self):
		pg.draw.circle(self.screen, self.color, self.rect.center, int(self.rect.width / 2))
