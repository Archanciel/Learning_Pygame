# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 1
# Video link: https://www.youtube.com/watch?v=uWvb3QzA48c
# Project setup

import pygame as pg

from tkinter import *
from tkinter import messagebox

from draw_grid.grid import Grid
from draw_grid.settings import *
import os

I = 1


class Game:
    def __init__(self):
        '''
        Initializes game window, etc.
        '''
        # setting Pygame window position
        os.environ['SDL_VIDEO_WINDOW_POS'] = WINDOWS_LOCATION

        pg.init()
        self.screen = pg.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

        self.grid = Grid(surface=self.screen, cellSize=DEFAULT_CELL_SIZE, initCellValue=0, gridDataFileName='gridData.csv')
        self.buttonDownPressed = False
        self.dragging = False
        self.mouse_x_beg = 0
        self.mouse_y_beg = 0
        self.mouse_x_end = 0
        self.mouse_y_end = 0

    def new(self):
        '''
        Starts a new game.
        '''
        pass

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
                    Tk().wm_withdraw()  # to hide the main window
                    if messagebox.askquestion(None,'Do you want to save grid data ?') == 'yes':
                        self.grid.saveGridData()

            # handling mouse grid move
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == I:
                    self.buttonDownPressed = True
                    self.mouse_x_beg, self.mouse_y_beg = event.pos
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == I:
                    self.buttonDownPressed = False
                    if self.dragging:
                        self.dragging = False
                    else:
                        if (self.mouse_x_beg, self.mouse_y_beg) == event.pos:
                            # here, we just clicked on a cell to activate or deactivate it
                            self.grid.toggleCell(event.pos)
            elif event.type == pg.MOUSEMOTION:
                if self.buttonDownPressed:
                    self.dragging = True
                    self.mouse_x_end, self.mouse_y_end = event.pos
                    xOffset = self.mouse_x_beg - self.mouse_x_end
                    yOffset = self.mouse_y_beg - self.mouse_y_end

                    self.grid.move(xOffset, yOffset)

                    self.mouse_x_beg = self.mouse_x_end
                    self.mouse_y_beg = self.mouse_y_end

            # technique used to allow moving grid only 1 unit at a time
            # elif event.type == pg.KEYDOWN:
            #     if event.key == pg.K_RIGHT:
            #         self.grid.moveRight(1)
            #     elif event.key == pg.K_LEFT:
            #         self.grid.moveLeft(1)

        # technique used to enable move grid more than 1 unit at a time
        keys = pg.key.get_pressed()

        if pg.key.get_mods() & pg.KMOD_CTRL: #CTRL key pressed
            if keys[pg.K_UP]:
                self.grid.zoomIn()
            if keys[pg.K_DOWN]:
                self.grid.zoomOut()
        else:
            if keys[pg.K_UP]:
                self.grid.moveUp(GRID_MOVE_INCREMENT)
            if keys[pg.K_DOWN]:
                self.grid.moveDown(GRID_MOVE_INCREMENT)
            if keys[pg.K_LEFT]:
                self.grid.moveLeft(GRID_MOVE_INCREMENT)
            if keys[pg.K_RIGHT]:
                self.grid.moveRight(GRID_MOVE_INCREMENT)

    def update(self):
        '''
        Updates all game objects.
        '''
        pass

    def draw(self):
        '''
        Redraws all game objects.
        '''
        if self.grid.changed:
            # optimization: the grid is only drawned if something changed on it
            self.screen.fill(WHITE)
            self.grid.draw()

            # *after* drawing everything, flip the display
            pg.display.flip()

    def show_start_screen(self):
        '''
        Shows game splash/start screen.
        '''
        Tk().wm_withdraw()  # to hide the main window
        if messagebox.askquestion(None, 'Do you want to load existing grid data ?') == 'yes':
            self.grid.loadGridData()

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