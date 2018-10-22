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

        xCellSize = 0
        activeCellLeftOffsetX = 0 # contains the active cell x offset from the left grid limit
                                  # (which has value 0). If its value is negative, this means
                                  # cell was moved further to the left of the left grid limit. If
                                  # its value is positive, the cell will be drawned entirely or not
                                  # depending if its x coord is positioned at the right of the grid
                                  # coord margin or at its left, i.e between the left grid limit
                                  # and the grid coord margin

        for row in range(len(self.cellValueGrid)):
            for col in range(len(self.cellValueGrid[0])):
                if self.cellValueGrid[row][col]:
                    activeCellXCoord = gridCoordMargin + (GRID_LINE_WIDTH // 2 + 1) + self.gridOffsetX + (
                                (GRID_LINE_WIDTH + self.cellSize) * col)
                    if activeCellXCoord > 0:
                        # here, the current active cell x coordinate is greater than the left grid limit and so must be
                        # drawn entirely or partially ...
                        activeCellLeftOffsetX = gridCoordMargin - activeCellXCoord
                        if activeCellLeftOffsetX > 0:
                            if activeCellLeftOffsetX < gridCoordMargin:
                                # here, we moved the grid to the left to a point where the current active cell is partially
                                # at the left of the col margin (grid coord margin where the row/col numbers are displayed)
                                xCellSize = self.cellSize - activeCellLeftOffsetX
                                if xCellSize <= 0:
                                    # this happens depending on the combination of the cell size set by the zoom
                                    # level and the value of the GRID_MOVE_INCREMENT constant
                                    continue
                                activeCellXCoord = gridCoordMargin
                            else:
                                # here, the current active cell is behond the grid coord margin and is drawn entirely
                                xCellSize = self.cellSize
                        else:
                            xCellSize = self.cellSize
                    else:
                        # here, the current active cell x coord is at the left of the left grid limit
                        activeCellLeftOffsetX = gridCoordMargin + activeCellXCoord # activeCellXCoord is negative here !
                        if activeCellLeftOffsetX >= 0:
                            if activeCellLeftOffsetX <= gridCoordMargin:
                                # here, the current active cell x coord is at the left of the left grid limit. But part
                                # of the cell has to be drawn for the part which is still at the right of the grid coord
                                # margin

                                # the move offset must account for the number of columns already moved to the left ...
                                offsetX = self.gridOffsetX + (GRID_LINE_WIDTH + self.cellSize) * col

                                xCellSize = self.cellSize + offsetX + (GRID_LINE_WIDTH // 2 + 1)
                                if xCellSize <= 0:
                                    # this happens depending on the combination of the cell size set by the zoom
                                    # level and the value of the GRID_MOVE_INCREMENT constant
                                    continue
                                activeCellXCoord = gridCoordMargin
                            # else: this case is not possible since activeCellLeftOffsetX = gridCoordMargin + negative
                            # value
                        elif activeCellLeftOffsetX < 0:
                            if abs(activeCellLeftOffsetX) <= gridCoordMargin:
                                # the move offset must account for the number of columns already moved to the left ...
                                offsetX = self.gridOffsetX + (GRID_LINE_WIDTH + self.cellSize) * col

                                xCellSize = self.cellSize + offsetX + (GRID_LINE_WIDTH // 2 + 1)
                                if xCellSize <= 0:
                                    # this happens depending on the combination of the cell size set by the zoom
                                    # level and the value of the GRID_MOVE_INCREMENT constant
                                    continue
                                activeCellXCoord = gridCoordMargin
                            else:
                                # the move offset must account for the number of columns already moved to the left ...
                                offsetX = self.gridOffsetX + (GRID_LINE_WIDTH + self.cellSize) * col

                                cellwidth = self.cellSize + offsetX + (GRID_LINE_WIDTH // 2 + 1)
                                if cellwidth > 0:
                                    xCellSize = cellwidth
                                    activeCellXCoord = gridCoordMargin
                                else:
                                    continue # we do not draw a cell which size would be 0 !

                    activeCellYCoordPx = gridCoordMargin + (GRID_LINE_WIDTH // 2 + 1) + self.gridOffsetY + (
                                (GRID_LINE_WIDTH + self.cellSize) * row)

                    pg.draw.rect(self.surface,
                                     GREEN,
                                     [activeCellXCoord,
                                      activeCellYCoordPx,
                                      xCellSize,
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
