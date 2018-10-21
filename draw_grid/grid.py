import pygame as pg

from draw_grid.settings import *

class Grid():
    def __init__(self, surface, cellSize, initCellValue):
        self.surface = surface
        self.cellSize = cellSize
        self.initCellValue = initCellValue
        self.setGridDimension()

        #Dimensioning the internal value grid to the max displayable cell number.
        #Since one cell can occupy a minimum of 1 px and the grid line width
        #is 1 px, 2 cells will require 1 + 1 + 1 + 1 + 1 = 5 px.
        #3 cells require 1 + 1 + 1 + 1 + 1 + 1 + 1 = 7 px.
        #n cells require 1 + (n * 2) px
        self.xMaxCellNumber = (surface.get_width() - 1) // 2
        self.yMaxCellNumber = (surface.get_height() - 1) // 2
        self.cellValueGrid = [[initCellValue for i in range(self.xMaxCellNumber)] for j in range(self.yMaxCellNumber)]

        self.setStartPattern()
        self.font = pg.font.SysFont('arial', int(GRID_COORD_MARGIN_SIZE / 20 * 12), False)
        self.drawAxisLabel = True
        self.gridOffsetX = 0
        self.gridOffsetY = 0

    def setStartPattern(self):
        for i in range(0,self.xMaxCellNumber,10):
            for j in range(0,self.yMaxCellNumber,10):
                self.cellValueGrid[i][j] = True

    def setGridDimension(self):
        self.colNb = (self.surface.get_width() - GRID_LINE_WIDTH) // (self.cellSize + GRID_LINE_WIDTH)
        self.lineNb = (self.surface.get_height() - GRID_LINE_WIDTH) // (self.cellSize + GRID_LINE_WIDTH)

    def draw(self):
        if self.drawAxisLabel:
            gridCoordMargin = GRID_COORD_MARGIN_SIZE
        else:
            gridCoordMargin = 0

        # drawing lines

        maxDrawnedLineNumber = self.lineNb + 1
        li = 0

        while li < maxDrawnedLineNumber:
            liCoord = gridCoordMargin + self.gridOffsetY + li * (self.cellSize + GRID_LINE_WIDTH)

            if self.drawAxisLabel:
                if li < 10:
                    ident = '   '
                else:
                    ident = '  '
                text = self.font.render(ident + str(li), 1, (0, 0, 0))
                if liCoord < gridCoordMargin // 2:
                    pass
                else:
                    self.surface.blit(text, (0, liCoord))

            li += 1

            if liCoord < gridCoordMargin:
                # We do not draw the line if its y coordinate is less than the grid
                # coordinates margin size.
                # Since the line was skipped, it must be replaced by a supplementary
                # line at the bottom of the grid
                maxDrawnedLineNumber += 1
                continue
            else:
                pg.draw.line(self.surface, BLACK, (gridCoordMargin, liCoord), (self.surface.get_width(), liCoord), GRID_LINE_WIDTH)

        # drawing columns

        maxDrawnedColNumber = self.lineNb + 1
        co = 0

        while co < maxDrawnedColNumber:
            colCoord = gridCoordMargin + self.gridOffsetX + co * (self.cellSize + GRID_LINE_WIDTH)

            if self.drawAxisLabel:
                if co < 10:
                    ident = '  '
                else:
                    ident = ' '
                text = self.font.render(ident + str(co), 1, (0, 0, 0))
                if colCoord < gridCoordMargin // 2:
                    pass
                else:
                    self.surface.blit(text, (colCoord, 1))

            co += 1

            if colCoord < gridCoordMargin:
                # We do not draw the column line if its x coordinate is less than the grid
                # coordinates margin size.
                # Since the column was skipped, it must be replaced by a supplementary
                # column at the very right of the grid
                maxDrawnedColNumber += 1
                continue
            else:
                pg.draw.line(self.surface, BLACK, (colCoord, gridCoordMargin), (colCoord,self.surface.get_height()), GRID_LINE_WIDTH)

        # drawing active cells

        # // 2 + 1 below is required to handle correctly GRID_LINE_WIDTH > 1 !

        for row in range(len(self.cellValueGrid)):
            for col in range(len(self.cellValueGrid[0])):
                if self.cellValueGrid[row][col]:
                    activeCellXCoordPx = gridCoordMargin + GRID_LINE_WIDTH // 2 + 1 + self.gridOffsetX + (
                                (GRID_LINE_WIDTH + self.cellSize) * col)
                    if activeCellXCoordPx > 0:
                        activeCellLeftOffsetX = gridCoordMargin - activeCellXCoordPx
                        if activeCellLeftOffsetX > 0 and activeCellLeftOffsetX < gridCoordMargin:
                            xCellSize = self.cellSize - activeCellLeftOffsetX
#                            print('offsetX={} activeCellXCoordPx={} xCellSize={}'.format(self.gridOffsetX,
#                                                                                         activeCellXCoordPx, xCellSize))
                            activeCellXCoordPx = gridCoordMargin
                        else:
                            xCellSize = self.cellSize
                    else:
                        activeCellLeftOffsetX = gridCoordMargin + activeCellXCoordPx
                        if activeCellLeftOffsetX >= 0 and activeCellLeftOffsetX < gridCoordMargin:
                            xCellSize = self.cellSize + self.gridOffsetX + GRID_LINE_WIDTH // 2 + 1
                            print('OOOoffsetX={} activeCellLeftOffsetX={} xCellSize={} activeCellXCoordPx={}'.format(self.gridOffsetX,
                                                                                            activeCellLeftOffsetX, xCellSize,
                                                                                            activeCellXCoordPx))
                            activeCellXCoordPx = gridCoordMargin
                        elif activeCellLeftOffsetX < 0:
                            if abs(activeCellLeftOffsetX) <= gridCoordMargin:
                                xCellSize = self.cellSize + self.gridOffsetX + GRID_LINE_WIDTH // 2 + 1
                                print('offsetX={} activeCellLeftOffsetX={} xCellSize={} activeCellXCoordPx={}'.format(self.gridOffsetX,
                                                                                                activeCellLeftOffsetX, xCellSize,
                                                                                                activeCellXCoordPx))
                                activeCellXCoordPx = gridCoordMargin
                            elif (self.cellSize + self.gridOffsetX + GRID_LINE_WIDTH // 2 + 1) >= 0:
                                xCellSize = self.cellSize + self.gridOffsetX + GRID_LINE_WIDTH // 2 + 1
                                activeCellXCoordPx = gridCoordMargin
                            else:
                                xCellSize = 0
                                activeCellXCoordPx = gridCoordMargin
                    activeCellYCoordPx = gridCoordMargin + GRID_LINE_WIDTH // 2 + 1 + self.gridOffsetY + (
                                (GRID_LINE_WIDTH + self.cellSize) * row)
                    pg.draw.rect(self.surface,
                                     GREEN,
                                     [activeCellXCoordPx,
                                      activeCellYCoordPx,
                                      xCellSize,
                                      self.cellSize])
                    # code below not working !!!
                    # pg.draw.rect(self.surface,
                    #                  GREEN,
                    #                  [gridCoordMargin + GRID_LINE_WIDTH + ((self.cellSize + GRID_LINE_WIDTH) * col),
                    #                   gridCoordMargin + GRID_LINE_WIDTH + ((self.cellSize + GRID_LINE_WIDTH) * row),
                    #                   self.cellSize,
                    #                   self.cellSize])
                    # pg.draw.rect(self.surface,
                    #                  GREEN,
                    #                  [gridCoordMargin + GRID_LINE_WIDTH - 1 + ((self.cellSize + GRID_LINE_WIDTH) * col),
                    #                   gridCoordMargin + GRID_LINE_WIDTH - 1 + ((self.cellSize + GRID_LINE_WIDTH) * row),
                    #                   self.cellSize,
                    #                   self.cellSize])

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
#        print('zoom in: cellsize {}, delta {}, col nb {}'.format(self.cellSize, delta, self.colNb))

    def zoomOut(self):
        delta = self.cellSize // 10

        if delta <= 0:
            delta = 1

        if self.cellSize > 2:
            self.cellSize -= delta
            if self.cellSize <= 11:
                self.drawAxisLabel = False

        self.setGridDimension()
#        print('zoom out: cellsize {}, delta {}, colnb {}'.format(self.cellSize, delta, self.colNb))

    def moveUp(self, pixels):
        self.gridOffsetY -= pixels

    def moveDown(self, pixels):
        self.gridOffsetY += pixels

        if self.gridOffsetY > 0:
            self.gridOffsetY = 0

    def moveLeft(self, pixels):
        self.gridOffsetX -= pixels

    def moveRight(self, pixels):
        self.gridOffsetX += pixels

        if self.gridOffsetX > 0:
            self.gridOffsetX = 0
