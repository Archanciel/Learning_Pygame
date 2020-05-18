import pygame
import math
import os

BOUNCE_ARROW_TOP = 2
BOUNCE_ARROW_RIGHT = 3
BOUNCE_ARROW_BOTTOM = 4
BOUNCE_ARROW_LEFT = 5

class Particle:
	def __init__(self, screen, x, y, radius, colour, thickness, angleDeg, speed):
		# angleDeg is the clockwise angle with 0 deg corresponding to 12 hour
		self.screen = screen
		self.x = x
		self.y = y
		self.radius = radius
		self.angleDeg = angleDeg
		self.angleRad = math.radians(angleDeg)
		self.speed = speed
		self.colour = colour
		self.thickness = thickness

	def move(self, angleDeg=0):
		if angleDeg == 0:
			angleDeg = self.angleDeg
			
		# angleDeg is the clockwise angle with 0 deg corresponding to 12 o'clock'
		angleRad = math.radians(angleDeg) - math.pi / 2
		dx = self.speed * math.cos(angleRad)
		dy = self.speed * math.sin(angleRad)
		self.x += dx
		self.y += dy

	def move_tuto(self, angleRad = 0):
		if angleRad == 0:
			angleRad = self.angleRad
			
		# angleRad is the clockwise angle in radians with 0 rad corresponding to 12 o'clock'
		dx = self.speed * math.sin(angleRad)
		dy = self.speed * math.cos(angleRad)
		self.x += dx
		self.y -= dy

	def my_move(self, angleDeg=0):
		if angleDeg == 0:
			angleDeg = self.angleDeg
			
		# angleDeg is the clockwise angle with 0 deg corresponding to 3 o'clock'
		angleRad = math.radians(angleDeg)
		dx = self.speed * math.cos(angleRad)
		dy = self.speed * math.sin(angleRad)
		self.x += dx
		self.y += dy

	def display(self):
		if os.name == 'posix':
			pygame.draw.circle(self.screen, self.colour, (self.x, self.y), self.radius, self.thickness)
		else:
			pygame.draw.circle(self.screen, self.colour, (round(self.x), round(self.y)), self.radius, self.thickness)

	def bounce(self):
		width, height = self.screen.get_size()
		
		if self.x > width - self.radius:
			self.x = 2 * (width - self.radius) - self.x
			self.angleRad = - self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(width, self.y, BOUNCE_ARROW_RIGHT)
		elif self.x < self.radius:
			self.x = 2 * self.radius - self.x
			self.angleRad = - self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(0, self.y, BOUNCE_ARROW_LEFT)
		if self.y > height - self.radius:
			self.y = 2 * (height - self.radius) - self.y
			self.angleRad = math.pi - self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(self.x, 0, BOUNCE_ARROW_TOP)
		elif self.y < self.radius:
			self.y = 2 * self.radius - self.y
			self.angleRad = math.pi - self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(self.x, height, BOUNCE_ARROW_BOTTOM)

	def storeBounceLocationData(self, bounceX, bounceY, bounceDirection):
		# storing bounce mark location coordinates, implemented by sub classes
		pass
