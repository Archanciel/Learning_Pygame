# Pygame template - skeleton for a new pygame project
import pygame
import random

WIDTH = 800
HEIGHT = 600
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        self.rect.x += 5
        if self.rect.x > WIDTH:
            self.rect.x = 0 - self.rect.width

        if self.rect.left > WIDTH: # BETTER !!!
            self.rect,right = 0

    def moveR(self, delta):
        self.rect.x += delta
        if self.rect.left > WIDTH:
            self.rect.right = 0

    def moveL(self, delta):
        self.rect.x -= delta
        if self.rect.right < 0:
            self.rect.left = WIDTH

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
allSprites = pygame.sprite.Group()
player = Player()
allSprites.add(player)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        player.moveR(5)

    if keys[pygame.K_LEFT]:
        player.moveL(5)

    # Update
    allSprites.update()

    # Draw / render
    screen.fill(BLACK)
    allSprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()