# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 1
# Video link: https://www.youtube.com/watch?v=uWvb3QzA48c
# Project setup

import pygame as pg
import os

from ball import Ball
from settings import *

class Game: 
    def __init__(self):
        '''
        Initializes game window, etc.
        '''
        # setting Pygame window position
        self.clock = pg.time.Clock()
        self.timerDC = 0
        self.dt = 0

        os.environ['SDL_VIDEO_WINDOW_POS'] = WINDOWS_LOCATION

        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.playing = False
        self.running = True

        self.all_sprites = None

    def new(self):
        '''
        Starts a new game.
        '''
        self.all_sprites = pg.sprite.Group()
        figure = Ball(screen=self.screen, color=GREEN, radius=30, startX=50, startY=50, dirX=10, dirY=10)
        self.all_sprites.add(figure)
        figure = Ball(screen=self.screen, color=RED, radius=30, startX=500, startY=600, dirX=15, dirY=15)
        self.all_sprites.add(figure)

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
            self.updateTimerForDoubleClick()

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
                self.handleDoubleClick()
                                        
    def updateTimerForDoubleClick(self):
        # Increase timerDC after mouse was pressed the first time.
        if self.timerDC != 0:
            self.timerDC += self.dt
        # Reset after 0.5 seconds.
        if self.timerDC >= 0.07:
            self.timerDC = 0

        # dt == time in seconds since last tick.
        # / 1000 to convert milliseconds to seconds.
        self.dt = self.clock.tick(FPS) / 2000

    def handleDoubleClick(self):
        if self.timerDC == 0:
            self.timerDC = 0.001
            # Click again before 0.5 seconds to double click.
        elif self.timerDC < 0.07:
            # Double click happened
            if self.playing:
                self.playing = False
            self.running = False

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