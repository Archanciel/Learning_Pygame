import pygame as pg
import math

from particle import Particle

BLACK = (0, 0, 0)

TWO_PI = math.pi * 2

class ParticleDisplayPos(Particle):
	def __init__(self, screen, x, y, radius, colour, thickness, angleDeg, speed):
		# angleDeg is the clockwise angle with 0 deg corresponding to 12 hour
		super().__init__(screen, x, y, radius, colour, thickness, angleDeg, speed)
		
		# Position related instance variables
		self.font = pg.font.Font(None, 32)
		self.font_height = self.font.get_linesize()

		# Calculating the left margin based on longest possible text
		rectSize = radius * 2
		self.textHorizontalSize = self.font.size("angle: 360")[0]
		self.textLeftMargin = (rectSize - self.textHorizontalSize) / 2

		# Calculating the top margin based on the number of text lines
		self.lineNumber = 3
		self.textTopMargin = radius - (self.font_height * self.lineNumber / 2)
		self.textColor = BLACK
		
		self.angleRadCorrection = math.pi / 2

	def display(self):
		super().display()

		# Writing information on the ball surface if the ball size is large enough
		if self.textHorizontalSize <= self.radius * 2:
			self.blitTextOnBall(round(self.x, 2), round(self.y, 2))

	def blitTextOnBall(self, xValue, yValue):
		textLines = [None] * self.lineNumber
		textLines[0] = 'x: ' + str(xValue)
		textLines[1] = 'y: ' + str(yValue)
		
		displayAngleRad = abs(self.angleRad - self.angleRadCorrection)
		
		if displayAngleRad >= TWO_PI:
			displayAngleRad -= TWO_PI

		angleDegree = round(math.degrees(displayAngleRad))

		textLines[2] = 'angle: ' + str(angleDegree)

		self.images = []  # The text surfaces.

		for line in textLines:
			textSurface = self.font.render(line, True, self.textColor)
			self.images.append(textSurface)
		for y, textSurface in enumerate(self.images):
			if y * self.font_height + self.font_height > (2 * self.radius):
				# Don't blit below the rect area.
				break
			textCoordinatesTuple = (self.x - self.radius + self.textLeftMargin,
									self.y - self.radius + self.textTopMargin + y * self.font_height)
			self.screen.blit(textSurface, textCoordinatesTuple)
