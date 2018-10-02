# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 1
# Video link: https://www.youtube.com/watch?v=uWvb3QzA48c
# Project setup

import pygame as pg

from draw_grid.player import Player
from draw_grid.settings import *
import os

class Grid():
    def __init__(self, surface, cellSize, initCellValue):
        self.surface = surface
        self.columns = surface.get_width() // cellSize
        self.lines = surface.get_height() // cellSize
        self.cellSize = cellSize
        self.initCellValue = initCellValue
#        self.grid = [[initCellValue] * self.columns for i in range(self.lines)]
        self.grid = [[initCellValue for i in range(self.columns)] for j in range(self.lines)]
        self.font = pg.font.SysFont('comicsans', 18, False)

    def draw(self):
        for li in range(self.lines):
            for co in range(self.columns):
                coCoord = GRID_COORD_MARGIN_SIZE + co * CELL_SIZE
                text = self.font.render(' ' + str(co), 1, (0, 0, 0))
                self.surface.blit(text, (coCoord, 1))
                pg.draw.rect(self.surface, BLACK, pg.Rect(GRID_COORD_MARGIN_SIZE + li * CELL_SIZE, coCoord, CELL_SIZE, CELL_SIZE), 1)



class Game:
    def __init__(self):
        '''
        Initializes game window, etc.
        '''
        # setting Pygame window position
        os.environ['SDL_VIDEO_WINDOW_POS'] = WINDOWS_LOCATION

        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

        self.grid = Grid(self.screen, CELL_SIZE, 0)

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