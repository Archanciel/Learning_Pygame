import pygame as pg
import math
from settings import *

class Ball():
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
		self.font = pg.font.Font(None, 32)
		self.font_height = self.font.get_linesize()
		self.textLeftMargin = self.rect.width / 4
		self.textTopMargin = radius - self.font_height / 2
		self.text_color = BLACK

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
		lines = []
		lines.append('x: ' + str(int(self.rect.centerx)) + ' y: ' + str(int(self.rect.centery)))
		lines.append('angle: ' + str(int(math.degrees(self.angle))))
        
		self.images = []  # The text surfaces.
                
		for line in lines:
			surf = self.font.render(line, True, self.text_color)
			self.images.append(surf)
        	
		for y, surf in enumerate(self.images):
            # Don't blit below the rect area.
			if y * self.font_height + self.font_height > self.rect.h:
				break
			self.screen.blit(surf, (self.rect.x + self.textLeftMargin, self.rect.y + self.textTopMargin + y*self.font_height))
