
import pygame


def main():
    pygame.init()
    DISPLAY = pygame.display.set_mode((1000,500),0,32)
    WHITE = (255,255,255)
    blue = (0,0,255)
    DISPLAY.fill(WHITE)
    pygame.mouse.set_visible(False)
    pygame.draw.rect(DISPLAY, blue,(480,200,50,250))
    pygame.display.update()
    pygame.mouse.set_pos((480, 200))
    run = True
    clock = pygame.time.Clock()
    timer = 0
    dt = 0
    pos = 0
    
    while run:
        for event in pygame.event.get():            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if timer == 0:
                	timer = 0.001
                    # Click again before 0.5 seconds to double click.
                elif timer < 0.5:
                    # Double click happened
                    run = False
            else:
            	if run:
                    pos = pygame.mouse.get_pos()
                    DISPLAY.fill(WHITE)
                    pygame.draw.rect(DISPLAY, blue, (pos[0],pos[1], 50, 250))
                    pygame.display.update()
        
        # Increase timer after mouse was pressed the first time.
        if timer != 0:
            timer += dt
            # Reset after 0.5 seconds.
            if timer >= 0.5:
                 timer = 0
        
        # dt == time in seconds since last tick.
        # / 1000 to convert milliseconds to seconds.
        dt = clock.tick(30) / 1000
       
main() 