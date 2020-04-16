import pygame as pg
from settings import *

class Ball(pg.sprite.Sprite):
	def __init__(self, screen, color, radius, startX, startY, dirX, dirY):
		super().__init__()
		self.screen = screen
		self.color = color
		rectSize = radius * 2
		self.image = pg.Surface((rectSize, rectSize))
		self.rect = self.image.get_rect()
		self.moveDir = [dirX, dirY]
		pg.draw.circle(self.image, self.color, self.rect.center, int(self.rect.width / 2))

	def update(self):
		self.rect = self.rect.move(self.moveDir)
		
		if self.rect.top <= 0 or self.rect.bottom >= self.screen.get_height():
			# inverting y direction
			self.moveDir[1] = -self.moveDir[1] 
			
		if self.rect.left <= 0 or self.rect.right >= self.screen.get_width():
			# inverting x direction
			self.moveDir[0] = -self.moveDir[0] 