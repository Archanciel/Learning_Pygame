# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 1
# Video link: https://www.youtube.com/watch?v=uWvb3QzA48c
# Project setup

import pygame as pg

from draw_grid.grid import Grid
from draw_grid.settings import *
import os


class Game:
    def __init__(self):
        '''
        Initializes game window, etc.
        '''
        # setting Pygame window position
        os.environ['SDL_VIDEO_WINDOW_POS'] = WINDOWS_LOCATION

        pg.init()
        self.screen = pg.display.set_mode((GRID_SIZE, GRID_SIZE))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

        self.grid = Grid(self.screen, DEFAULT_CELL_SIZE, 0)
        self.dragging = False
        self.mouse_x_beg = 0
        self.mouse_y_beg = 0
        self.mouse_x_end = 0
        self.mouse_y_end = 0

    def new(self):
        '''
        Starts a new game.
        '''
        self.all_sprites = pg.sprite.Group()
#        self.player = Player()
#        self.all_sprites.add(self.player)

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
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:            
                    self.dragging = True
                    self.mouse_x_beg, self.mouse_y_beg = event.pos
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:            
                    self.dragging = False
            elif event.type == pg.MOUSEMOTION:
                if self.dragging:
                    self.mouse_x_end, self.mouse_y_end = event.pos

        keys = pg.key.get_pressed()

        if keys[pg.K_UP]:
            self.grid.zoomIn()
        elif keys[pg.K_DOWN]:
            self.grid.zoomOut()
            
        print('x {}, y {} offset'.format(self.mouse_x_end - self.mouse_x_beg, self.mouse_y_end - self.mouse_y_beg))   

    def update(self):
        '''
        Updates all game objects.
        '''
        self.all_sprites.update()

    def draw(self):
        '''
        Redraws all game objects.
        '''
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.grid.draw()

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