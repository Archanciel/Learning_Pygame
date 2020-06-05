import pygame as pg

BLACK = (0, 0, 0)

class TextOnScreen():
	def __init__(self, screen, x, y, textLineLst=[]):
		# angleDeg is the clockwise angle with 0 deg corresponding to 12 hour
		self.screen = screen
		self.x = x
		self.y = y
		self.textLineLst = textLineLst
		
		# Position related instance variables
		self.font = pg.font.Font(None, 25)
		self.font_height = self.font.get_linesize()

		# Calculating the left margin based on longest possible text
		self.textHorizontalSize = self.computeMaxTextLength()
		#self.textLeftMargin = (rectSize - self.textHorizontalSize) / 2

		# Calculating the top margin based on the number of text lines
		self.lineNumber = len(textLineLst)
		# self.textTopMargin = radius - (self.font_height * self.lineNumber / 2)
		self.textColor = BLACK
		
		# The text surfaces ...
		self.images = []
		
		if textLineLst != []:
			self.addTextLines(textLineLst)

	def addTextLine(self, textLine):
		textSurface = self.font.render(textLine, True, self.textColor)
		self.images.append(textSurface)

	def addTextLines(self, textLineLst):
		for textLine in textLineLst:
			textSurface = self.font.render(textLine, True, self.textColor)
			self.images.append(textSurface)
				
	def computeMaxTextLength(self):
		maxLength = 0
		
		for textLine in self.textLineLst:
			currLength = self.font.size(textLine)[0]
			if currLength > maxLength:
				maxLength = currLength
				
		return maxLength
			
	def display(self):
		for imageIdx, textSurface in enumerate(self.images):
			#if y * self.font_height + self.font_height > (2 * self.radius):
				# Don't blit below the rect area.
				#break
			textCoordinatesTuple = (self.x,
									self.y + imageIdx * self.font_height)
			self.screen.blit(textSurface, textCoordinatesTuple)
