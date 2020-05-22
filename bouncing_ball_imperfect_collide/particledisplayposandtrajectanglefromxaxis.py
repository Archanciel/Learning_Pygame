import pygame as pg
import math

from particledisplayposandtraject import * # using * imports constants aswell !

TWO_PI = math.pi * 2

class ParticleDisplayPosAndTrajectAngleFromXAxis(ParticleDisplayPosAndTraject):
	def __init__(self, screen, x, y, radius, colour, thickness, angleDeg, speed):
		# angleDeg is the clockwise angle with 0 deg corresponding to 12 hour
		super().__init__(screen, x, y, radius, colour, thickness, angleDeg, speed)

	def move(self, angleRad = 0):
		if angleRad == 0:
			angleRad = self.angleRad
			
		# angleRad is the clockwise angle in radians with 0 rad corresponding to 12 o'clock'
		dx = self.speed * math.cos(angleRad)
		dy = self.speed * math.sin(angleRad)
		self.x += dx
		self.y -= dy

	def bounce(self):
		width, height = self.screen.get_size()

		if self.angleRad > 2 * math.pi:
			# avoid displaying a negative value for the angle in degree. Useful only if window height > window width,
			# at least om Windows !
			self.angleRad -= 2 * math.pi

		if self.x > width - self.radius:
			self.x = 2 * (width - self.radius) - self.x
			self.angleRad = math.pi - self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(width, self.y, BOUNCE_ARROW_RIGHT)
		elif self.x < self.radius:
			self.x = 2 * self.radius - self.x
			self.angleRad = math.pi - self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(0, self.y, BOUNCE_ARROW_LEFT)
		if self.y > height - self.radius:
			self.y = 2 * (height - self.radius) - self.y
			self.angleRad = -self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(self.x, height, BOUNCE_ARROW_BOTTOM)
		elif self.y < self.radius:
			self.y = 2 * self.radius - self.y
			self.angleRad = -self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(self.x, 0, BOUNCE_ARROW_TOP)

	def computeDisplayAngleRad(self):
		# computing display angle radians if the X axis is the reference
		# for defining the particle angle.
		if self.angleRad < 0:
			return TWO_PI + self.angleRad
		else:
			return self.angleRad
