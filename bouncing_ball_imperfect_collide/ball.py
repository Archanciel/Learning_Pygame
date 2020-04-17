import pygame as pg
import math
from settings import *

class Ball(pg.sprite.Sprite):
	def __init__(self, 
	             screen, 
	             spriteGroup, 
	             color, 
	             radius, 
	             startX, 
	             startY, 
	             speed, 
	             angle=-45):
		super().__init__()
		self.screen = screen
		self.spriteGroup = spriteGroup
		self.color = color
		rectSize = radius * 2
		self.image = pg.Surface((rectSize, rectSize))
		self.rect = self.image.get_rect()
#		self.rect.left = startX
#		self.rect.top = startY
		self.speed = speed
		self.angle = angle
		pg.draw.circle(self.image, self.color, self.rect.center, int(self.rect.width / 2))

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
				
		for ball in self.spriteGroup.sprites():
			if not hit_bounds and not ball is self and self.rect.colliderect(ball.rect):
				self.angle = self.angle - math.pi
				break
				
	# Draw our ball to the screen
#	def draw(self): not used !
#		pg.draw.circle(self.image, self.color, self.rect.center, int(self.rect.width / 2))
				
'''		
		self.rect = self.rect.move(self.moveDir)
		
		if self.rect.top <= 0 or self.rect.bottom >= self.screen.get_height():
			# inverting y direction
			self.moveDir[1] = -self.moveDir[1] 
			
		if self.rect.left <= 0 or self.rect.right >= self.screen.get_width():
			# inverting x direction
			self.moveDir[0] = -self.moveDir[0] 
'''