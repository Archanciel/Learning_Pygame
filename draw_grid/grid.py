import pygame as pg

from draw_grid.settings import *

class Grid():
    def __init__(self, surface, cellSize, initCellValue):
        self.surface = surface
        self.cellSize = cellSize
        self.initCellValue = initCellValue
        self.gridCoordMargin = GRID_COORD_MARGIN_SIZE
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

        self.startDrawRowIndex = 0
        self.startDrawColIndex = 0

    def setStartPattern(self):
        for i in range(0,self.xMaxCellNumber,10):
            for j in range(0,self.yMaxCellNumber,10):
                self.cellValueGrid[i][j] = True

    def setGridDimension(self):
        self.drawnedColNb = (self.surface.get_width() - GRID_LINE_WIDTH - self.gridCoordMargin) // (self.cellSize + GRID_LINE_WIDTH)
        self.drawnedRowNb = (self.surface.get_height() - GRID_LINE_WIDTH - self.gridCoordMargin) // (self.cellSize + GRID_LINE_WIDTH)

    def draw(self):
        if self.drawAxisLabel:
            self.gridCoordMargin = GRID_COORD_MARGIN_SIZE
        else:
            self.gridCoordMargin = 0

        # drawing lines

        maxDrawnedLineNumber = self.drawnedRowNb + 1
        li = 0

        while li < maxDrawnedLineNumber:
            liCoord = self.gridCoordMargin + self.gridOffsetY + li * (self.cellSize + GRID_LINE_WIDTH)

            if self.drawAxisLabel:
                if li < 10:
                    ident = '   '
                else:
                    ident = '  '
                text = self.font.render(ident + str(li), 1, (0, 0, 0))
                if liCoord < self.gridCoordMargin // 2:
                    pass
                else:
                    self.surface.blit(text, (0, liCoord))

            li += 1

            if liCoord < self.gridCoordMargin:
                # We do not draw the line if its y coordinate is less than the grid
                # coordinates margin size.
                # Since the line was skipped, it must be replaced by a supplementary
                # line at the bottom of the grid
                maxDrawnedLineNumber += 1
                continue
            else:
                pg.draw.line(self.surface, BLACK, (self.gridCoordMargin, liCoord), (self.surface.get_width(), liCoord), GRID_LINE_WIDTH)

        # drawing columns

        maxDrawnedColNumber = self.drawnedRowNb + 1
        co = 0

        while co < maxDrawnedColNumber:
            colCoord = self.gridCoordMargin + self.gridOffsetX + co * (self.cellSize + GRID_LINE_WIDTH)

            if self.drawAxisLabel:
                if co < 10:
                    ident = '  '
                else:
                    ident = ' '
                text = self.font.render(ident + str(co), 1, (0, 0, 0))
                if colCoord < self.gridCoordMargin // 2:
                    pass
                else:
                    self.surface.blit(text, (colCoord, 1))

            co += 1

            if colCoord < self.gridCoordMargin:
                # We do not draw the column line if its x coordinate is less than the grid
                # coordinates margin size.
                # Since the column was skipped, it must be replaced by a supplementary
                # column at the very right of the grid
                maxDrawnedColNumber += 1
                continue
            else:
                pg.draw.line(self.surface, BLACK, (colCoord, self.gridCoordMargin), (colCoord,self.surface.get_height()), GRID_LINE_WIDTH)

        # drawing active cells

        # // 2 + 1 below is required to handle correctly GRID_LINE_WIDTH > 1 !

        activeCellLeftOffsetX = 0 # contains the active cell x offset from the left grid limit
                                  # (which has value 0). If its value is negative, this means
                                  # cell was moved further to the left of the left grid limit. If
                                  # its value is positive, the cell will be drawned entirely or not
                                  # depending if its x coord is positioned at the right of the grid
                                  # coord margin or at its left, i.e between the left grid limit
                                  # and the grid coord margin

#The two commented line below cause active cell drawîng problems when an active cell is to be drawned partially.
#This happens in normal display and after zoomong in or out
        # for row in range(self.startDrawRowIndex, self.drawnedRowNb + self.startDrawRowIndex):
        #     for col in range(self.startDrawColIndex, self.drawnedColNb + self.startDrawColIndex):
        for row in range(len(self.cellValueGrid)):
            for col in range(len(self.cellValueGrid[0])):
                if self.cellValueGrid[row][col]:
                    activeCellXCoord = self.gridCoordMargin + GRID_LINE_WIDTH + self.gridOffsetX + (
                                (GRID_LINE_WIDTH + self.cellSize) * col)
                    drawnedActiveCellXCoord, cellWidth = self.computeCellCoordAndSize(self.gridOffsetX, activeCellXCoord, col)

                    if drawnedActiveCellXCoord == None:
                        # cell out of display area
                        continue

                    activeCellYCoord = self.gridCoordMargin + GRID_LINE_WIDTH + self.gridOffsetY + (
                                (GRID_LINE_WIDTH + self.cellSize) * row)
                    drawnedActiveCellYCoord, cellHeight = self.computeCellCoordAndSize(self.gridOffsetY, activeCellYCoord, row)

                    if drawnedActiveCellYCoord == None:
                        # cell out of display area
                        continue

                    pg.draw.rect(self.surface,
                                     GREEN,
                                     [drawnedActiveCellXCoord,
                                      drawnedActiveCellYCoord,
                                      cellWidth,
                                      cellHeight])

    def computeCellCoordAndSize(self, gridMoveOffset, activeCellCoord, rowOrColIndex):
        '''
        Computes the active cell top left x or y coordinate aswell as the active cell size. Used to redraw active
        cells, accounting for their modified coordinates due to horizontal or/and vertical moves combined with
        ooming in or out.

        Note that the code of this method is commented for handling an horizontal move. In order to keep comments
        readable, their adaption to handling a vertical move is left to the reader !

        :param gridMoveOffset: x or y grid move offset
        :param activeCellCoord: active cell x or y coord
        :param rowOrColIndex: index of current active cell row or col

        :return: activeCellCoord - current cell top left x or y coordinate
                 cellEdgeSize - size of current cell (square in fact)
        '''
        cellEdgeSize = 0

        if activeCellCoord > 0:
            # here, the current active cell x coordinate is greater than the left grid limit and so must be
            # drawn entirely or partially ...
            activeCellCoordOffset = self.gridCoordMargin - activeCellCoord
            if activeCellCoordOffset > 0:
                if activeCellCoordOffset < self.gridCoordMargin:
                    # here, we moved the grid to the left to a point where the current active cell is partially
                    # at the left of the col margin (grid coord margin where the row/col numbers are displayed)
                    cellEdgeSize = self.cellSize - activeCellCoordOffset
                    if cellEdgeSize <= 0:
                        # this happens depending on the combination of the cell size set by the zoom
                        # level and the value of the GRID_MOVE_INCREMENT constant
                        return None, None
                    activeCellCoord = self.gridCoordMargin
                else:
                    # here, the current active cell is behond the grid coord margin and is drawn entirely
                    cellEdgeSize = self.cellSize
            else:
                cellEdgeSize = self.cellSize
        else:
            # here, the current active cell x coord is at the left of the left grid limit
            activeCellCoordOffset = self.gridCoordMargin + activeCellCoord  # activeCellXCoord is negative here !
            if activeCellCoordOffset >= 0:
                if activeCellCoordOffset <= self.gridCoordMargin:
                    # here, the current active cell x coord is at the left of the left grid limit. But part
                    # of the cell has to be drawn for the part which is still at the right of the grid coord
                    # margin

                    # the move offset must account for the number of columns already moved to the left ...
                    offset = gridMoveOffset + (GRID_LINE_WIDTH + self.cellSize) * rowOrColIndex

                    cellEdgeSize = self.cellSize + offset + GRID_LINE_WIDTH
                    if cellEdgeSize <= 0:
                        # this happens depending on the combination of the cell size set by the zoom
                        # level and the value of the GRID_MOVE_INCREMENT constant
                        return None, None
                    activeCellCoord = self.gridCoordMargin
                # else: this case is not possible since activeCellLeftOffsetX = self.gridCoordMargin + negative
                # value
            elif activeCellCoordOffset < 0:
                if abs(activeCellCoordOffset) <= self.gridCoordMargin:
                    # the move offset must account for the number of columns already moved to the left ...
                    offset = gridMoveOffset + (GRID_LINE_WIDTH + self.cellSize) * rowOrColIndex

                    cellEdgeSize = self.cellSize + offset + GRID_LINE_WIDTH
                    if cellEdgeSize <= 0:
                        # this happens depending on the combination of the cell size set by the zoom
                        # level and the value of the GRID_MOVE_INCREMENT constant
                        return None, None
                    activeCellCoord = self.gridCoordMargin
                else:
                    # the move offset must account for the number of columns already moved to the left ...
                    offset = gridMoveOffset + (GRID_LINE_WIDTH + self.cellSize) * rowOrColIndex

                    cellwidth = self.cellSize + offset + GRID_LINE_WIDTH
                    if cellwidth > 0:
                        cellEdgeSize = cellwidth
                        activeCellCoord = self.gridCoordMargin
                    else:
                        # we do not draw a cell which size would be 0 !
                        return None, None

        return activeCellCoord, cellEdgeSize

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

    def move(self, xOffset, yOffset):
        if xOffset > 0:
            self.moveLeft(xOffset)
        elif xOffset < 0:
            self.moveRight(-xOffset)

        if yOffset > 0:
            self.moveUp(yOffset)
        elif yOffset < 0:
            self.moveDown(-yOffset)

    def moveUp(self, pixels):
        self.gridOffsetY -= pixels
        self.updateStartDrawRowIndex()

    def moveDown(self, pixels):
        self.gridOffsetY += pixels

        if self.gridOffsetY > 0:
            self.gridOffsetY = 0

        self.updateStartDrawRowIndex()

    def moveLeft(self, pixels):
        self.gridOffsetX -= pixels
        self.updateStartDrawColIndex()

    def moveRight(self, pixels):
        self.gridOffsetX += pixels

        if self.gridOffsetX > 0:
            self.gridOffsetX = 0

        self.updateStartDrawColIndex()

    def updateStartDrawColIndex(self):
        self.startDrawColIndex = (-self.gridOffsetX - 1) // self.cellSize
#        print('offsetX {}, anchorX {}'.format(self.gridOffsetX, self.startDrawLineIndex))

    def updateStartDrawRowIndex(self):
        self.startDrawRowIndex = (-self.gridOffsetY - 1) // self.cellSize
#        print('offsetY {}, anchorY {}'.format(self.gridOffsetY, self.startDrawLineIndex))
