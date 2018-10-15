import pygame as pg

from draw_grid.settings import GRID_COORD_MARGIN_SIZE, BLACK, GREEN


class Grid():
    def __init__(self, surface, cellSize, initCellValue):
        self.surface = surface
        self.cellSize = cellSize
        self.initCellValue = initCellValue
        self.setGridDimension()


        #Dimensioning the internal value grid to the max displayable cell number.
        #Since one cell can occupy a minuimum of 1 px and the grid line width
        #is 1 px, 2 cells will require 1 + 1 + 1 + 1 + 1 = 5 px.
        #3 cells require 1 + 1 + 1 + 1 + 1 + 1 + 1 = 7 px.
        #n cells require (n * 2) + 1 px
        self.cellValueGrid = [[initCellValue for i in range((surface.get_width() - 1) // 2)] for j in range((surface.get_height() - 1) // 2)]

        self.setStartPattern()
        self.font = pg.font.SysFont('arial', int(GRID_COORD_MARGIN_SIZE / 20 * 12), False)
        self.drawAxisLabel = True

    def setStartPattern(self):
        for i in range(0,300,10):
            self.cellValueGrid[i][0] = True
        for i in range(0,300,10):
            self.cellValueGrid[i][100] = True
        for i in range(0,300,10):
            self.cellValueGrid[i][300] = True

        for i in range(0, 300, 10):
            self.cellValueGrid[i][0] = True
        for i in range(0, 300, 10):
            self.cellValueGrid[i][15] = True
        for i in range(0, 300, 10):
            self.cellValueGrid[i][30] = True

        for i in range(0, 300, 10):
            self.cellValueGrid[i][0] = True
        for i in range(0, 300, 10):
            self.cellValueGrid[i][15] = True
        for i in range(0, 300, 10):
            self.cellValueGrid[i][30] = True

    def setGridDimension(self):
        self.colNb = (self.surface.get_width() - 1) // (self.cellSize + 1)
        self.lineNb = (self.surface.get_height() - 1) // (self.cellSize + 1)

    def draw(self):
        if self.drawAxisLabel:
            gridCoordMargin = GRID_COORD_MARGIN_SIZE
        else:
            gridCoordMargin = 0

        for li in range(self.lineNb + 1): #+1 since the bottom most margin needs to be drawn !
            liCoord = gridCoordMargin + li * (self.cellSize + 1)

            if self.drawAxisLabel:
                if li < 10:
                    ident = '   '
                else:
                    ident = '  '
                text = self.font.render(ident + str(li), 1, (0, 0, 0))
                self.surface.blit(text, (0, liCoord))

            pg.draw.line(self.surface, BLACK, (gridCoordMargin, liCoord), (self.surface.get_width(), liCoord))
        for co in range(self.colNb + 1): #+1 since the right most margin needs to be drawn !
            colCoord = gridCoordMargin + co * (self.cellSize + 1)

            if self.drawAxisLabel:
                if co < 10:
                    ident = '  '
                else:
                    ident = ' '
                text = self.font.render(ident + str(co), 1, (0, 0, 0))
                self.surface.blit(text, (colCoord, 1))

            pg.draw.line(self.surface, BLACK, (colCoord, gridCoordMargin), (colCoord,self.surface.get_height()))

        #drawing active cells

        for row in range(len(self.cellValueGrid)):
            for col in range(len(self.cellValueGrid[0])):
                if self.cellValueGrid[row][col]:
                    pg.draw.rect(self.surface,
                                     GREEN,
                                     [gridCoordMargin + 1 + ((1 + self.cellSize) * col),
                                      gridCoordMargin + 1 + ((1 + self.cellSize) * row),
                                      self.cellSize,
                                      self.cellSize])

    def zoomIn(self):
        delta = self.cellSize // 10
        if delta <= 0:
            delta = 1

        self.cellSize += delta

        if self.cellSize >= self.surface.get_height():
            self.cellSize -= delta

        if self.cellSize > 11:
            self.drawAxisLabel = True

        self.setGridDimension()
        print('zoom in: cellsize {}, delta {}, col nb {}'.format(self.cellSize, delta, self.colNb))

    def zoomOut(self):
        delta = self.cellSize // 10

        if delta <= 0:
            delta = 1

        if self.cellSize > 2:
            self.cellSize -= delta
            if self.cellSize <= 11:
                self.drawAxisLabel = False
        print('zoom out: cellsize {}, delta {}, colnb {}'.format(self.cellSize, delta, self.colNb))

        self.setGridDimension()