import pygame
import math
import os

BOUNCE_ARROW_TOP = 2
BOUNCE_ARROW_RIGHT = 3
BOUNCE_ARROW_BOTTOM = 4
BOUNCE_ARROW_LEFT = 5

if os.name == 'posix':
	GRAVITY = (math.pi, 0.8) # ok on Android
else:
	GRAVITY = (math.pi, 0.02) # ok on Windows

DRAG = 0.999
ELASTICITY = 0.75

class Particle:
	def __init__(self, screen, x, y, radius, color, thickness, angleDeg, speed):
		# angleDeg is the clockwise angle with 0 deg corresponding to 12 o'clock
		self.screen = screen
		self.x = x
		self.y = y
		self.radius = radius
		self.angleRad = math.radians(angleDeg)
		self.speed = speed
		self.color = color
		self.thickness = thickness

	def move(self):			
		# angleRad is the clockwise angle in radians with 0 rad corresponding
		# to 12 o'clock'
		dx = self.speed * math.sin(self.angleRad)
		dy = self.speed * math.cos(self.angleRad)
		self.x += dx
		self.y -= dy

	def moveGravity(self):
		
		self.angleRad, self.speed = self.addAngleSpeedVector((self.angleRad, self.speed), GRAVITY)
		self.move()	
		self.speed *= DRAG

	def bounce(self):
		bounced = False
		width, height = self.screen.get_size()

		if self.angleRad > 2 * math.pi:
			# avoid displaying a negative value for the angle in degree. Useful only if window height > window width,
			# at least om Windows !
			self.angleRad -= 2 * math.pi

		if self.x > width - self.radius:
			bounced = True
			self.x = 2 * (width - self.radius) - self.x
			self.angleRad = -self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(width, self.y, BOUNCE_ARROW_RIGHT)
		elif self.x < self.radius:
			bounced = True
			self.x = 2 * self.radius - self.x
			self.angleRad = -self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(0, self.y, BOUNCE_ARROW_LEFT)
		if self.y > height - self.radius:
			bounced = True
			self.y = 2 * (height - self.radius) - self.y
			self.angleRad = math.pi - self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(self.x, height, BOUNCE_ARROW_BOTTOM)
		elif self.y < self.radius:
			bounced = True
			self.y = 2 * self.radius - self.y
			self.angleRad = math.pi - self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(self.x, 0, BOUNCE_ARROW_TOP)
			
		return bounced
	
	def bounceElasticity(self):
		width, height = self.screen.get_size()

		if self.angleRad > 2 * math.pi:
			# avoid displaying a negative value for the angle in degree. Useful only if window height > window width,
			# at least om Windows !
			self.angleRad -= 2 * math.pi

		if self.x > width - self.radius:
			self.x = 2 * (width - self.radius) - self.x
			self.angleRad = -self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(width, self.y, BOUNCE_ARROW_RIGHT)
			self.speed *= ELASTICITY
		elif self.x < self.radius:
			self.x = 2 * self.radius - self.x
			self.angleRad = -self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(0, self.y, BOUNCE_ARROW_LEFT)
			self.speed *= ELASTICITY
		if self.y > height - self.radius:
			self.y = 2 * (height - self.radius) - self.y
			self.angleRad = math.pi - self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(self.x, height, BOUNCE_ARROW_BOTTOM)
			self.speed *= ELASTICITY
		elif self.y < self.radius:
			self.y = 2 * self.radius - self.y
			self.angleRad = math.pi - self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(self.x, 0, BOUNCE_ARROW_TOP)
			self.speed *= ELASTICITY

	def storeBounceLocationData(self, bounceX, bounceY, bounceDirection):
		# storing bounce mark location coordinates, implemented by sub classes
		pass

	def display(self):
		if os.name == 'posix':
			pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius, self.thickness)
		else:
			pygame.draw.circle(self.screen, self.color, (round(self.x), round(self.y)), self.radius, self.thickness)
	
	def addAngleSpeedVector(self, vector1, vector2):
		# Computes the Y axis based (angle, speed) vector resulting from adding the Y axis based
		# vector1 and vector2
		angle1 = vector1[0]
		length1 = vector1[1]
		angle2 = vector2[0]
		length2 = vector2[1]

		x = math.sin(angle1) * length1 + math.sin(angle2) * length2
		y = math.cos(angle1) * length1 + math.cos(angle2) * length2

		length = math.hypot(x, y)
		angle = (math.pi / 2) - math.atan2(y, x)

		return (angle, length)