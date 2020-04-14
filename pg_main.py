# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 1
# Video link: https://www.youtube.com/watch?v=uWvb3QzA48c
# Project setup

import pygame as pg
import os

from template.player import Player
from template.settings import *

class Game: 
    def __init__(self):
        '''
        Initializes game window, etc.
        '''
        # setting Pygame window position
        self.clock = pg.time.Clock()
        self.timer = 0
        self.dt = 0

        os.environ['SDL_VIDEO_WINDOW_POS'] = WINDOWS_LOCATION

        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.running = True

    def new(self):
        '''
        Starts a new game.
        '''
        self.all_sprites = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)

    def run(self):
        '''
        Is the game loop.
        '''
        self.playing = True

        while self.playing:
            self.clock.tick(FPS)
            self.handleEvents()
            self.update()
            self.draw()
            # Increase timer after mouse was pressed the first time.
            if self.timer != 0:
                self.timer += self.dt
            # Reset after 0.5 seconds.
            if self.timer >= 0.5:
                self.timer = 0
        
            # dt == time in seconds since last tick.
            # / 1000 to convert milliseconds to seconds.
            self.dt = self.clock.tick(30) / 1000

    def handleEvents(self):
        '''
        Acquires and handles events.
        '''
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN: #on Android, tap the sreen to quit
                if self.timer == 0:
            	    self.timer = 0.001
                    # Click again before 0.5 seconds to double click.
                elif self.timer < 0.5:
                    # Double click happened
                    if self.playing:
                        self.playing = False
                    self.running = False
                    
                mouse_x, mouse_y = pg.mouse.get_pos()
                pg.key.get_pressed()
                
                if mouse_y > 2000:
                    if self.playing:
                       self.playing = False
                    self.running = False
                else:	 
                    if mouse_x < 800: 
         	           self.player.moveL(10)
                    else:
                	    self.player.moveR(10)
                    
    def update(self):
        '''
        Updates all game objects.
        '''
        self.all_sprites.update()

    def draw(self):
        '''
        Redraws all game objects.
        '''
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        '''
        Shows game splash/start screen.
        '''
        pass

    def show_go_screen(self):
        '''
        Shows game over screen.
        '''
        pass

g = Game()
g.show_start_screen()

while g.running:
    g.new()
    g.run()
    g.show_go_screen()

pg.quit()