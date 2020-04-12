import pygame
import sys

pygame.init()
win = pygame.display.set_mode((500, 500)) #no effect on Android !
pygame.display.set_caption('First Pygame') #no effect on Android !
win.fill((255,255,255)) #set scn color to white

run = True

while run:
    pygame.time.delay(100)
    pygame.display.flip() #on Nndroid, without it, scn remains black !
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #no effect on Android !
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN: #on Android, tap the sreen to quit
            run = False

pygame.quit()
sys.exit(0)