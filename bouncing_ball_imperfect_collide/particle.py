import pygame
import math
import os

class Particle:
	def __init__(self, screen, x, y, radius, thickness, angle, speed):
		self.screen = screen
		self.x = x
		self.y = y
		self.radius = radius
		self.angle = math.radians(angle)
		self.speed = speed
		self.colour = (0, 0, 255)
		self.thickness = thickness

	def move(self, angle):
		angleRad = math.radians(angle) - math.pi / 2
		dx = self.speed * math.cos(angleRad)
		dy = self.speed * math.sin(angleRad)
		self.x += dx
		self.y += dy

	def display(self):
		if os.name == 'posix':
			pygame.draw.circle(self.screen, self.colour, (self.x, self.y), self.radius, self.thickness)
		else:
			pygame.draw.circle(self.screen, self.colour, (round(self.x), round(self.y)), self.radius, self.thickness)

