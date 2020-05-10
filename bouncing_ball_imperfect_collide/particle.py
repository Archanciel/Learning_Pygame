import pygame

class Particle:
    def __init__(self, screen, x, y, radius):
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = (0, 0, 255)
        self.thickness = 3

    def display(self):
        pygame.draw.circle(self.screen, self.colour, (self.x, self.y), self.radius, self.thickness)

