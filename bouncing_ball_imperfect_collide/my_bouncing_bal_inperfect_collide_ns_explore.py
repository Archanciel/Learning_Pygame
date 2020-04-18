# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 1
# Video link: https://www.youtube.com/watch?v=uWvb3QzA48c
# Project setup

import pygame as pg
import os, random

from ball_no_sprite_explore import Ball
from settings import *

COLORS = [WHITE, RED, GREEN, BLUE, YELLOW]

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

        self.allBalls = None

    def new(self):
        '''
        Starts a new game.
        '''
        
        # Create multiple sprite Ball instances
        self.allBalls = []

        for i in range(1, 3):
            colIdx = random.randrange(0, 4)

            if os.name == 'posix':
                ball = Ball(screen=self.screen,
                            allBalls=self.allBalls,
                            color=COLORS[colIdx],
                            radius=200,
                            startX=i * 500,
                            startY= i * 650,
                            speed=6)
            else:
                ball = Ball(screen=self.screen,
                            allBalls=self.allBalls,
                            color=COLORS[colIdx],
                            radius=max(i * 3, 10),
                            startX=i * 60,
                            startY=i * 45,
                            speed=min(i * 2, 4))

            self.allBalls.append(ball)
            
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
        if self.timerDC >= 0.1:
            self.timerDC = 0

        # dt == time in seconds since last tick.
        # / 1000 to convert milliseconds to 10th of seconds.
        self.dt = self.clock.tick(FPS) / 10000

    def handleDoubleClick(self):
        if self.timerDC == 0:
            self.timerDC = 0.01
            # Click again before 0.1 seconds to double click.
        elif self.timerDC < 0.1:
            # Double click happened
            if self.playing:
                self.playing = False
                
            self.running = False

    def update(self):
        '''
        Updates all game objects.
        '''
        for ball in self.allBalls:
            ball.update()

    def draw(self):
        '''
        Redraws all game objects.
        '''
        self.screen.fill(BLACK)
        
        for ball in self.allBalls: 
            ball.draw()
        
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