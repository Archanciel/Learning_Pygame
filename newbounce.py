import pygame

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

class Ball(pygame.sprite.Sprite):
    """This class represents the ball."""
    def __init__(self, diameter):
        """ Constructor. Pass in the balls x and y position. """
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Create the surface, give dimensions and set it to be transparent
        self.image = pygame.Surface([diameter, diameter])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

        # Draw the ellipse onto the surface
        pygame.draw.circle(self.image, (255,0,0), self.rect.center,int(diameter / 2))

# Initialize Pygame
pygame.init()

# Set the height and width of the screen
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

## Loop until the user clicks the close button.
done = False

# --- Create sprites and groups
ball = Ball(50)
g = pygame.sprite.Group(ball)

# -------- Main Program Loop -----------
while not done:
    # --- Events code goes here (mouse clicks, key hits etc)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Clear the screen
    screen.fill(BLACK)

    # --- Draw all the objects
    g.draw(screen)

    # --- Update the screen with what we've drawn.
    pygame.display.flip()
    #pygame.display.update()

    # --- Limit to 60 frames per second
    clock.tick(60)

pygame.quit()