import pygame
import os

class Particle:
    def __init__(self, screen, x, y, radius):
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = (0, 0, 255)
        self.thickness = 1

    def display(self):
        if os.name == 'posix':
            pygame.draw.circle(self.screen, self.colour, (self.x, self.y), self.radius, self.thickness)
        else:
            pygame.draw.circle(self.screen, self.colour, (round(self.x), round(self.y)), self.radius, self.thickness)

