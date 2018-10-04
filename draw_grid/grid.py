import pygame as pg

from draw_grid.settings import GRID_COORD_MARGIN_SIZE, BLACK


class Grid():
    def __init__(self, surface, cellSize, initCellValue):
        self.surface = surface
        self.cellSize = cellSize
        self.initCellValue = initCellValue
        self.setGridDimension()
        self.cellValueGrid = [[initCellValue for i in range(surface.get_width())] for j in range(surface.get_height())]
        self.font = pg.font.SysFont('arial', 12, False)
        self.drawAxisLabel = True

    def setGridDimension(self):
        self.colNb = self.surface.get_width() // self.cellSize
        self.lineNb = self.surface.get_height() // self.cellSize

    def draw(self):
        if self.drawAxisLabel:
            gridCoordMargin = GRID_COORD_MARGIN_SIZE
        else:
            gridCoordMargin = 0

        for li in range(self.lineNb + 1):
            liCoord = gridCoordMargin + li * self.cellSize

            if self.drawAxisLabel:
                if li < 10:
                    ident = '   '
                else:
                    ident = '  '
                text = self.font.render(ident + str(li), 1, (0, 0, 0))
                self.surface.blit(text, (0, liCoord))

            pg.draw.line(self.surface, BLACK, (gridCoordMargin, liCoord), (self.surface.get_width(), liCoord))
        for co in range(self.colNb + 1):
            colCoord = gridCoordMargin + co * self.cellSize

            if self.drawAxisLabel:
                if co < 10:
                    ident = '  '
                else:
                    ident = ' '
                text = self.font.render(ident + str(co), 1, (0, 0, 0))
                self.surface.blit(text, (colCoord, 1))

            pg.draw.line(self.surface, BLACK, (colCoord, gridCoordMargin), (colCoord,self.surface.get_height()))

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

    def zoomOut(self):
        delta = self.cellSize // 10

        if delta <= 0:
            delta = 1

        if self.cellSize > 2:
            self.cellSize -= delta
            if self.cellSize <= 11:
                self.drawAxisLabel = False

        self.setGridDimension()