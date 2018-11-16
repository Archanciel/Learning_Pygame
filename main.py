# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 1
# Video link: https://www.youtube.com/watch?v=uWvb3QzA48c
# Project setup

import pygame as pg

from tkinter import *
from tkinter import messagebox

from draw_grid.gridview import GridView
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

        self.gridView = GridView(surface=self.screen, cellSize=DEFAULT_CELL_SIZE, gridDataFileName='gridData.csv')
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
                        self.gridView.saveGridData()

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
                            self.gridView.toggleCell(event.pos)
            elif event.type == pg.MOUSEMOTION:
                if self.buttonDownPressed:
                    self.dragging = True
                    self.mouse_x_end, self.mouse_y_end = event.pos
                    xOffset = self.mouse_x_beg - self.mouse_x_end
                    yOffset = self.mouse_y_beg - self.mouse_y_end

                    self.gridView.move(xOffset, yOffset)

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

        if pg.key.get_mods() & pg.KMOD_SHIFT: #SHIFT key pressed
            if keys[pg.K_UP]:
                self.gridView.zoomIn()
            elif keys[pg.K_DOWN]: # using elif: since either zoom in or out, not both together, makes sense
                self.gridView.zoomOut()
        elif pg.key.get_mods() & pg.KMOD_CTRL:  # CTRL key pressed
            if keys[pg.K_UP]:
                self.gridView.moveViewToTop()
            if keys[pg.K_DOWN]:
                self.gridView.moveViewToBottom()
            if keys[pg.K_LEFT]:
                self.gridView.moveViewToLeftHome()
            if keys[pg.K_RIGHT]:
                self.gridView.moveViewToRightEnd()
        else:
            if keys[pg.K_DOWN]:
                self.gridView.moveViewDown(GRID_MOVE_INCREMENT)
            if keys[pg.K_UP]:
                self.gridView.moveViewUp(GRID_MOVE_INCREMENT)
            if keys[pg.K_RIGHT]:
                self.gridView.moveViewRight(GRID_MOVE_INCREMENT)
            if keys[pg.K_LEFT]:
                self.gridView.moveViewLeft(GRID_MOVE_INCREMENT)

    def update(self):
        '''
        Updates all game objects.
        '''
        pass

    def draw(self):
        '''
        Redraws all game objects.
        '''
        if self.gridView.changed:
            # optimization: the grid is only drawned if something changed on it
            self.screen.fill(WHITE)
            self.gridView.draw()

            # *after* drawing everything, flip the display
            pg.display.flip()

    def show_start_screen(self):
        '''
        Shows game splash/start screen.
        '''
        Tk().wm_withdraw()  # to hide the main window
        if messagebox.askquestion(None, 'Do you want to load existing grid data ?') == 'yes':
            fileNotFoundName = self.gridView.loadGridData()
            if fileNotFoundName:
                messagebox.showerror(None, fileNotFoundName + ' not found. Grid initialized with neutral data !')
                self.gridView.initialiseCellsToValue(0)
        else:
            self.gridView.initialiseCellsToValue(0)

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