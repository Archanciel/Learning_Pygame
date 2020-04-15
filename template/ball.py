import pygame as pg

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
		
	def draw(self):
		# pg.draw.circle(surface, color, center, radius) -> Rect
		pg.draw.circle(self.screen, self.color, self.rect.center, int(self.rect.width / 2))
