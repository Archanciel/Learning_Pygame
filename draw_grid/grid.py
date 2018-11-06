import pygame as pg

from draw_grid.settings import *
from draw_grid.griddatamanager import GridDataManager

class Grid():

    def __init__(self, surface, cellSize, initCellValue, gridDataFileName):
        self.changed = True
        self.surface = surface
        self.cellSize = cellSize
        self.gridDataMgr = GridDataManager(gridDataFileName)
        self.gridCoordMargin = GRID_COORD_MARGIN_SIZE
        self.setGridDimension()

        #Dimensioning the internal value grid to the max displayable cell number.
        #Since one cell can occupy a minimum of 1 px and the grid line width
        #is 1 px at the minimum, 2 cells will require at leastb1 + 1 + 1 + 1 + 1 = 5 px.
        #3 cells require at leastv1 + 1 + 1 + 1 + 1 + 1 + 1 = 7 px.
        #n cells require at least 1 + (n * 2) px
        self.xMaxCellNumber = (surface.get_width() - 1) // 2
        self.yMaxCellNumber = (surface.get_height() - 1) // 2
        self.cellValueGrid = None

        self.font = pg.font.SysFont('arial', int(GRID_COORD_MARGIN_SIZE / 20 * 12), False)
        self.drawAxisLabel = True
        self.gridOffsetXPx = 0
        self.gridOffsetYPx = 0

        self.startDrawRowIndex = 0
        self.startDrawColIndex = 0

    def setStartPattern(self):
        pass

    def setGridDimension(self):
        self.drawnedColNb = (self.surface.get_width() - self.gridCoordMargin - GRID_LINE_WIDTH) // (self.cellSize + GRID_LINE_WIDTH)
        self.drawnedRowNb = (self.surface.get_height() - self.gridCoordMargin - GRID_LINE_WIDTH) // (self.cellSize + GRID_LINE_WIDTH)

    def draw(self):
        if self.drawAxisLabel:
            self.gridCoordMargin = GRID_COORD_MARGIN_SIZE
        else:
            self.gridCoordMargin = 0

        # drawing lines

        maxDrawnedLineNumber = self.drawnedRowNb + 1
        li = 0

        while li < maxDrawnedLineNumber:
            liCoord = self.gridCoordMargin + self.gridOffsetYPx + li * (self.cellSize + GRID_LINE_WIDTH)

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

        maxDrawnedColNumber = self.drawnedColNb + 1
        co = 0

        while co < maxDrawnedColNumber:
            colCoord = self.gridCoordMargin + self.gridOffsetXPx + co * (self.cellSize + GRID_LINE_WIDTH)

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

        maxDrawnedRowIndex = min(self.yMaxCellNumber, self.drawnedRowNb + self.startDrawRowIndex + 2)
        maxDrawnedColIndex = min(self.xMaxCellNumber, self.startDrawColIndex + self.drawnedColNb + 2)

        for row in range(self.startDrawRowIndex, maxDrawnedRowIndex):
            for col in range(self.startDrawColIndex, maxDrawnedColIndex):
                if self.cellValueGrid[row][col]:
                    activeCellXCoord = self.gridCoordMargin + GRID_LINE_WIDTH + self.gridOffsetXPx + (
                                (GRID_LINE_WIDTH + self.cellSize) * col)
                    drawnedActiveCellXCoord, cellWidth = self.computeCellCoordAndSize(self.gridOffsetXPx, activeCellXCoord, col)

                    if drawnedActiveCellXCoord == None:
                        # cell out of display area
                        continue

                    activeCellYCoord = self.gridCoordMargin + GRID_LINE_WIDTH + self.gridOffsetYPx + (
                                (GRID_LINE_WIDTH + self.cellSize) * row)
                    drawnedActiveCellYCoord, cellHeight = self.computeCellCoordAndSize(self.gridOffsetYPx, activeCellYCoord, row)

                    if drawnedActiveCellYCoord == None:
                        # cell out of display area
                        continue

                    pg.draw.rect(self.surface,
                                     GREEN,
                                     [drawnedActiveCellXCoord - CELL_SIZE_OFFSET,
                                      drawnedActiveCellYCoord - CELL_SIZE_OFFSET,
                                      cellWidth,
                                      cellHeight])

        self.changed = False

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
                # else: this case is not possible since activeCellCoordOffset = self.gridCoordMargin + negative
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
        self.updateStartDrawRowIndex()
        self.updateStartDrawColIndex()
        self.changed = True

    def zoomOut(self):
        delta = self.cellSize // 10

        if delta <= 0:
            delta = 1

        if self.cellSize > 2:
            self.cellSize -= delta
            if self.cellSize <= 11:
                self.drawAxisLabel = False

        # repositionning the display horizontaly so that only editable cells (cells in
        # self.cellValueGrid) are displayed, preventing to set a cell value on a cell
        # which does not exists, which would cause an IndexOutOfRange exception.
        maxAllowedXOffsetPx = self.computeMaxAllowedOffsetPx()

        if -self.gridOffsetXPx > maxAllowedXOffsetPx:
            self.gridOffsetXPx = - (maxAllowedXOffsetPx - 1)

        self.setGridDimension()
        self.updateStartDrawRowIndex()
        self.updateStartDrawColIndex()
        self.changed = True

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
        newGridOffset = self.gridOffsetYPx - pixels

        if -newGridOffset > self.yMaxCellNumber:
            #preventing from moving behond grid height. This avoids changing a cell value
            #for a cell outside of the internal cell value grid
            return

        self.gridOffsetYPx -= pixels
        self.updateStartDrawRowIndex()
        self.changed = True

    def moveDown(self, pixels):
        self.gridOffsetYPx += pixels

        if self.gridOffsetYPx > 0:
            self.gridOffsetYPx = 0

        self.updateStartDrawRowIndex()
        self.changed = True

    def moveLeft(self, pixels):
        newGridXOffsetPx = self.gridOffsetXPx - pixels
        maxAllowedXOffsetPx = self.computeMaxAllowedOffsetPx()
        print(maxAllowedXOffsetPx)
        if -newGridXOffsetPx >= maxAllowedXOffsetPx:
            #preventing from moving behond grid height. This avoids changing a cell value
            #for a cell outside of the internal cell value grid
            print('return', newGridXOffsetPx, self.gridOffsetXPx, self.cellSize)
            return

        print('ok', newGridXOffsetPx, self.gridOffsetXPx, self.cellSize)

        self.gridOffsetXPx = newGridXOffsetPx
        self.updateStartDrawColIndex()
        self.changed = True

    def computeMaxAllowedOffsetPx(self):
        maxDrawnedColIndex = min(self.xMaxCellNumber, self.startDrawColIndex + self.drawnedColNb + 2)
        cellPlusSideWidthPxNumber = self.cellSize + GRID_LINE_WIDTH
        maxAllowedXOffsetPx = (maxDrawnedColIndex * cellPlusSideWidthPxNumber) - GRID_LINE_WIDTH
#        displayableCellNumber = round((self.surface.get_width() - GRID_LINE_WIDTH) / cellPlusSideWidthPxNumber)
#        maxAllowedXOffsetPx = ((                                           self.xMaxCellNumber - displayableCellNumber) * cellPlusSideWidthPxNumber) - GRID_LINE_WIDTH
        return maxAllowedXOffsetPx

    def moveRight(self, pixels):
        self.gridOffsetXPx += pixels

        if self.gridOffsetXPx > 0:
            self.gridOffsetXPx = 0

        self.updateStartDrawColIndex()
        self.changed = True

    def updateStartDrawColIndex(self):
        self.startDrawColIndex = -self.gridOffsetXPx // (self.cellSize + GRID_LINE_WIDTH)

    def updateStartDrawRowIndex(self):
        self.startDrawRowIndex = -self.gridOffsetYPx // (self.cellSize + GRID_LINE_WIDTH)

    def toggleCell(self, xyMousePosTuple):
        x, y = xyMousePosTuple
        col = (x - self.gridCoordMargin - GRID_LINE_WIDTH - self.gridOffsetXPx) // (GRID_LINE_WIDTH + self.cellSize)
        row = (y - self.gridCoordMargin - GRID_LINE_WIDTH - self.gridOffsetYPx) // (GRID_LINE_WIDTH + self.cellSize)

        if self.cellValueGrid[row][col]:
            self.cellValueGrid[row][col] = 0
        else:
            self.cellValueGrid[row][col] = 1

        self.changed = True

    def saveGridData(self):
        self.gridDataMgr.writeGridData(self.cellValueGrid)

    def loadGridData(self):
        self.cellValueGrid = self.gridDataMgr.readGridData()

    def initialiseCellsToValue(self, value=0):
        '''
        Sets all cells of the internal cell value grid to the initial value defined at GFrid
        construction.
        :param value: must be 0 (dead) or 1 (alive)
        '''
        self.initCellValue = value
        self.cellValueGrid = [[value for i in range(self.xMaxCellNumber)] for j in range(self.yMaxCellNumber)]

