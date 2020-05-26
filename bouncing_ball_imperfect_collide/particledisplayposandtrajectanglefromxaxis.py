import pygame as pg
import math

from particledisplayposandtraject import * # using * imports constants aswell !

TWO_PI = math.pi * 2

class ParticleDisplayPosAndTrajectAngleFromXAxis(ParticleDisplayPosAndTraject):
	def __init__(self, screen, x, y, radius, color, thickness, angleDeg, speed, bouncePointColor=None):
		# angleDeg is the clockwise angle with 0 deg corresponding to 12 hour
		super().__init__(screen, x, y, radius, color, thickness, angleDeg, speed, bouncePointColor)

	def move(self, angleRad = 0):
		if angleRad == 0:
			angleRad = self.angleRad
			
		# angleRad is the clockwise angle in radians with 0 rad corresponding 
		# to 3 o'clock'
		dx = self.speed * math.cos(angleRad)
		dy = self.speed * math.sin(angleRad)
		self.x += dx
		self.y -= dy

	def moveGravity(self):
		# gravity related constants are defined here simply to facilitate their 
		# modification while experimenting
		from move_particle_gravity import GRAVITY
		from move_particle_gravity import DRAG
		
		self.angleRad, self.speed = self.addAngleSpeedVector((self.angleRad, self.speed), GRAVITY)
		self.move()	
		#self.speed *= DRAG

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
			self.angleRad = math.pi - self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(width, self.y, BOUNCE_ARROW_RIGHT)
		elif self.x < self.radius:
			bounced = True
			self.x = 2 * self.radius - self.x
			self.angleRad = math.pi - self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(0, self.y, BOUNCE_ARROW_LEFT)
		if self.y > height - self.radius:
			bounced = True
			self.y = 2 * (height - self.radius) - self.y
			self.angleRad = -self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(self.x, height, BOUNCE_ARROW_BOTTOM)
		elif self.y < self.radius:
			bounced = True
			self.y = 2 * self.radius - self.y
			self.angleRad = -self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(self.x, 0, BOUNCE_ARROW_TOP)
			
		return bounced

	def bounceElasticity(self):
		# gravity related constants are defined here simply to facilitate their 
		# modification while experimenting
		from move_particle_gravity import ELASTICITY
		
		bounced = False
		width, height = self.screen.get_size()

		if self.angleRad > 2 * math.pi:
			# avoid displaying a negative value for the angle in degree. Useful only if window height > window width,
			# at least om Windows !
			self.angleRad -= 2 * math.pi

		if self.x > width - self.radius:
			bounced = True
			self.x = 2 * (width - self.radius) - self.x
			self.angleRad = math.pi - self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(width, self.y, BOUNCE_ARROW_RIGHT)
			self.speed *= ELASTICITY
		elif self.x < self.radius:
			bounced = True
			self.x = 2 * self.radius - self.x
			self.angleRad = math.pi - self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(0, self.y, BOUNCE_ARROW_LEFT)
			self.speed *= ELASTICITY
		if self.y > height - self.radius:
			bounced = True
			self.y = 2 * (height - self.radius) - self.y
			self.angleRad = -self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(self.x, height, BOUNCE_ARROW_BOTTOM)
			self.speed *= ELASTICITY
		elif self.y < self.radius:
			bounced = True
			self.y = 2 * self.radius - self.y
			self.angleRad = -self.angleRad

			# storing bounce mark location coordinates
			self.storeBounceLocationData(self.x, 0, BOUNCE_ARROW_TOP)
			self.speed *= ELASTICITY
			
		return bounced

	def computeDisplayAngleRad(self):
		# computing display angle radians if the X axis is the reference
		# for defining the particle angle.
		if self.angleRad < 0:
			return TWO_PI + self.angleRad
		else:
			return self.angleRad
			
	def addAngleSpeedVectorYAxisBased(self, vector1, vector2):
	
		x1 = math.sin(vector1[0]) * vector1[1]
		y1 = math.cos(vector1[0]) * vector1[1]
	
		x2 = math.sin(vector2[0]) * vector2[1]
		y2 = math.cos(vector2[0]) * vector2[1]
	
		xSum = x1 + x2
		ySum = y1 + y2
		speedSum = math.hypot(xSum, ySum)
		angleSum = (math.pi / 2) - math.atan2(ySum, xSum)
		
		return (angleSum, speedSum) 
		
	def addAngleSpeedVector(self, vector1, vector2):
		angle1 = vector1[0]
		length1 = vector1[1]		
		angle2 = vector2[0]
		length2 = vector2[1]		
		
		x = math.cos(angle1) * length1 + math.cos(angle2) * length2
		y = math.sin(angle1) * length1 + math.sin(angle2) * length2
		
		length = math.hypot(x, y)
		angle = math.atan2(y, x)
		
		return (angle, length)
