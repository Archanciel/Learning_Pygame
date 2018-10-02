import pygame

from template.settings import GREEN, WIDTH, HEIGHT

WIDTH = 800
HEIGHT = 600
FPS = 30


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def moveR(self, delta):
        self.rect.x += delta
        if self.rect.left > WIDTH:
            self.rect.right = 0

    def moveL(self, delta):
        self.rect.x -= delta
        if self.rect.right < 0:
            self.rect.left = WIDTH