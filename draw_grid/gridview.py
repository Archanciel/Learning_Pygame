import pygame as pg

from draw_grid.midcell import MidCell
from draw_grid.settings import *
from draw_grid.griddatamanager import GridDataManager

class GridView():

    def __init__(self, surface, cellSize, gridDataFileName):
        self.changed = True
        self.surface = surface
        self.cellSize = cellSize
        self.gridDataMgr = GridDataManager(gridDataFileName)
        self.gridCoordMargin = GRID_COORD_MARGIN_SIZE
        self.setGridDimension()

        self.horizontalMaxManagedCellNumber = (surface.get_width() - 1) // SMALLEST_CELL_REQUIRED_PX_NUMBER
        self.verticalMaxManagedCellNumber = (surface.get_height() - 1) // SMALLEST_CELL_REQUIRED_PX_NUMBER
        self.cellValueGrid = None

        self.font = pg.font.SysFont('arial', int(GRID_COORD_MARGIN_SIZE / 20 * 12), False)
        self.drawAxisLabel = True

        # when opening the grid windows, the visible part of the cells is set at the very
        # left and very top. This means that the self.gridOffsetXPx and self.gridOffsetYPx
        # have a value of 0 pixel. When clicking on the left arrow, the self.gridOffsetXPx
        # will be subtracted the number of pixels set in the GRID_MOVE_INCREMENT constant.
        # On the contrary, pressing the right arrow will increment the self.gridOffsetXPx,
        # this up to 0. Same behavior for the up and down keys, respectively.
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

        maxDrawnedRowIndex = min(self.verticalMaxManagedCellNumber, self.drawnedRowNb + self.startDrawRowIndex + 2)
        maxDrawnedColIndex = min(self.horizontalMaxManagedCellNumber, self.startDrawColIndex + self.drawnedColNb + 2)

        for row in range(self.startDrawRowIndex, maxDrawnedRowIndex):
            for col in range(self.startDrawColIndex, maxDrawnedColIndex):
                if self.cellValueGrid[row][col]:
                    theoreticalCellXCoord = self.gridCoordMargin + GRID_LINE_WIDTH + self.gridOffsetXPx + (
                                (GRID_LINE_WIDTH + self.cellSize) * col)
                    drawnedCellXCoord, drawnedCellWidth = self.computeVisibleCellCoordAndSize(self.gridOffsetXPx, theoreticalCellXCoord, col)

                    theoreticalCellYCoord = self.gridCoordMargin + GRID_LINE_WIDTH + self.gridOffsetYPx + (
                                (GRID_LINE_WIDTH + self.cellSize) * row)
                    drawnedCellYCoord, drawnedCellHeight = self.computeVisibleCellCoordAndSize(self.gridOffsetYPx, theoreticalCellYCoord, row)

                    if drawnedCellYCoord == None:
                        # cell out of display area
                        continue

                    pg.draw.rect(self.surface,
                                     GREEN,
                                     [drawnedCellXCoord - CELL_SIZE_OFFSET,
                                      drawnedCellYCoord - CELL_SIZE_OFFSET,
                                      drawnedCellWidth,
                                      drawnedCellHeight])

        self.changed = False

    def computeVisibleCellCoordAndSize(self, currentGridXorYOffsetPx, theoreticalCellXorYcoordPx, cellRowOrColIndex):
        '''
        When drawing a cell on the grid view, according to the grid view position, a visible cell may be
        have to be partially drawned if it is at the left side of the grid view or at its right side.
        The grid view position is given by the parm currentGridXorYOffsetPx. For example, moving the grid view
        10 pixels to the right will be reflected with a value of -10 for currentGridXorYOffsetPx, which means
        the underlying grid matrix is shifted 10 pixels to the left.

        A cell located precisely at the left side of the grid view would be drawned entirely. But if the view
        is shifted one pixel to the right (currentGridXorYOffsetPx == -1), the cell has to be partially drawned
        since 1 pixel of its left part is now outside of the grid view. Its top left x coordinate will be 20
        (the grid view margin size in pixels), but its size will be reduced by 1 pixel.

        The method computes the cell top left x or y coordinate aswell as its size accounting for the fact the cell
        may have to be partially drawned if part of the cell is before the grid view left size or beyhound its right
        side. Additionnally, the displayed or not grid view margin is taken in consideration.

        Note that the code of this method is commented regarding the horizontal dimension and its effect on the
        x cell top left coordinate. In order to keep comments readable, their adaptation to handling the vertical
        dimension (y) is left to the reader !

        :param currentGridXorYOffsetPx: x or y grid offset in pixels
        :param theoreticalCellXorYcoordPx: cell x or y coord as deducted from its location in the internal grid
                                           matrix
        :param cellRowOrColIndex: index of current cell row or col in the internal grid
                                           matrix

        :return: drawnedCellXorYcoordPx - drawned cell top left x or y pixel coordinate
                 cellSize - size of current cell (square in fact)
        '''
        cellSize = 0
        drawnedCellXorYcoordPx = theoreticalCellXorYcoordPx

        if theoreticalCellXorYcoordPx > 0:
            # here, the current cell x coordinate is greater than the left grid limit and so must be
            # drawn entirely or partially ...
            cellCoordOffset = self.gridCoordMargin - theoreticalCellXorYcoordPx
            if cellCoordOffset > 0:
                if cellCoordOffset < self.gridCoordMargin:
                    # here, we moved the grid to the left to a point where the current active cell is partially
                    # at the left of the col margin (grid coord margin where the row/col numbers are displayed)
                    cellSize = self.cellSize - cellCoordOffset
                    if cellSize <= 0:
                        # this happens depending on the combination of the cell size set by the zoom
                        # level and the value of the GRID_MOVE_INCREMENT constant
                        return None, None
                    drawnedCellXorYcoordPx = self.gridCoordMargin
                else:
                    # here, the current active cell is behond the grid coord margin and is drawn entirely
                    cellSize = self.cellSize
            else:
                cellSize = self.cellSize
        else:
            # here, the current cell x coord is at the left of the left grid limit
            cellCoordOffset = self.gridCoordMargin + theoreticalCellXorYcoordPx  # activeCellXCoord is negative here !
            if cellCoordOffset >= 0:
                if cellCoordOffset <= self.gridCoordMargin:
                    # here, the current active cell x coord is at the left of the left grid limit. But part
                    # of the cell has to be drawn for the part which is still at the right of the grid coord
                    # margin

                    # the move offset must account for the number of columns already moved to the left ...
                    offset = currentGridXorYOffsetPx + (GRID_LINE_WIDTH + self.cellSize) * cellRowOrColIndex

                    cellSize = self.cellSize + offset + GRID_LINE_WIDTH
                    if cellSize <= 0:
                        # this happens depending on the combination of the cell size set by the zoom
                        # level and the value of the GRID_MOVE_INCREMENT constant
                        return None, None
                    drawnedCellXorYcoordPx = self.gridCoordMargin
                # else: this case is not possible since activeCellCoordOffset = self.gridCoordMargin + negative
                # value
            elif cellCoordOffset < 0:
                if abs(cellCoordOffset) <= self.gridCoordMargin:
                    # the move offset must account for the number of columns already moved to the left ...
                    offset = currentGridXorYOffsetPx + (GRID_LINE_WIDTH + self.cellSize) * cellRowOrColIndex

                    cellSize = self.cellSize + offset + GRID_LINE_WIDTH
                    if cellSize <= 0:
                        # this happens depending on the combination of the cell size set by the zoom
                        # level and the value of the GRID_MOVE_INCREMENT constant
                        return None, None
                    drawnedCellXorYcoordPx = self.gridCoordMargin
                else:
                    # the move offset must account for the number of columns already moved to the left ...
                    offset = currentGridXorYOffsetPx + (GRID_LINE_WIDTH + self.cellSize) * cellRowOrColIndex

                    cellwidth = self.cellSize + offset + GRID_LINE_WIDTH
                    if cellwidth > 0:
                        cellSize = cellwidth
                        drawnedCellXorYcoordPx = self.gridCoordMargin
                    else:
                        # we do not draw a cell which size would be 0 !
                        return None, None

        return drawnedCellXorYcoordPx, cellSize

    def zoomIn(self):
        midCellBeforeZoom = MidCell(self)
        delta = self.cellSize // 10
        if delta <= 0:
            delta = 1

        self.cellSize += delta

        if self.cellSize >= self.surface.get_height():
            self.cellSize -= delta

        if self.cellSize > AXIS_HIDE_CELL_SIZE_LIMIT:
            self.drawAxisLabel = True
            self.gridCoordMargin = GRID_COORD_MARGIN_SIZE

        self.setGridDimension()
        self.updateStartDrawRowIndex()
        self.updateStartDrawColIndex()

        zoomXOffset, zoomYOffset = midCellBeforeZoom.computeXYOffsetAfterZoom()
        print('zoomIn before recentring', self.gridOffsetXPx)

        self.moveViewRight(-zoomXOffset)
        self.moveViewDown(-zoomYOffset)
        print('zoomIn after recentring', self.gridOffsetXPx)

        self.changed = True

    def zoomOut(self):
        midCellBeforeZoom = MidCell(self)
        delta = self.cellSize // 10

        if delta <= 0:
            delta = 1

        if self.cellSize > SMALLEST_CELL_REQUIRED_PX_NUMBER:
            self.cellSize -= delta
            if self.cellSize <= AXIS_HIDE_CELL_SIZE_LIMIT:
                self.drawAxisLabel = False
                self.gridCoordMargin = 0

        # repositionning the display horizontaly so that only editable cells (cells in
        # self.cellValueGrid) are displayed, preventing to set a cell value on a cell
        # which does not exists, which would cause an IndexOutOfRange exception.
        maxAllowedOffsetXPx = self.computeMaxAllowedHorizontalOffsetPx()

        if -self.gridOffsetXPx > maxAllowedOffsetXPx:
            self.gridOffsetXPx = - (maxAllowedOffsetXPx - 1)

        # repositionning the display vertically so that only editable cells (cells in
        # self.cellValueGrid) are displayed, preventing to set a cell value on a cell
        # which does not exists, which would cause an IndexOutOfRange exception.
        maxAllowedOffsetYPx = self.computeMaxAllowedVerticalOffsetPx()

        if -self.gridOffsetYPx > maxAllowedOffsetYPx:
            self.gridOffsetYPx = - (maxAllowedOffsetYPx - 1)

        self.setGridDimension()
        self.updateStartDrawRowIndex()
        self.updateStartDrawColIndex()
        print('zoomOut Before recentring', self.gridOffsetXPx)

        zoomXOffset, zoomYOffset = midCellBeforeZoom.computeXYOffsetAfterZoom()
        self.moveViewLeft(zoomXOffset)
        self.moveViewUp(zoomYOffset)
        print('zoomOut after recentring', self.gridOffsetXPx)

        self.changed = True

    def move(self, xOffset, yOffset):
        if xOffset > 0:
            self.moveViewRight(xOffset)
        elif xOffset < 0:
            self.moveViewLeft(-xOffset)

        if yOffset > 0:
            self.moveViewDown(yOffset)
        elif yOffset < 0:
            self.moveViewUp(-yOffset)

    def moveViewDown(self, pixels):
        # print('moveViewDown')
        newGridYOffset = self.gridOffsetYPx - pixels
        maxAllowedOffsetYPx = self.computeMaxAllowedVerticalOffsetPx()

        if -newGridYOffset >= maxAllowedOffsetYPx:
            #preventing from moving behond grid height. This avoids changing a cell value
            #for a cell outside of the internal cell value grid
            return

        self.gridOffsetYPx = newGridYOffset
        self.updateStartDrawRowIndex()
        self.changed = True

    def moveViewToTop(self):
        '''
        Resets to the top most (0) row.
        '''
        # print('moveViewToTop')
        self.gridOffsetYPx = 0
        self.updateStartDrawRowIndex()
        self.changed = True

    def moveViewUp(self, pixels):
        # print('moveViewUp')
        self.gridOffsetYPx += pixels
        maxAllowedOffsetYPx = self.computeMaxAllowedVerticalOffsetPx()

        if self.gridOffsetYPx > 0:
            self.gridOffsetYPx = 0
        elif -self.gridOffsetYPx > maxAllowedOffsetYPx:
            # this can happen when zooming out and recentring the displayed zone
            self.gridOffsetYPx = -maxAllowedOffsetYPx

        self.updateStartDrawRowIndex()
        self.changed = True

    def moveViewToBottom(self):
        '''
        Sets the display to the right most or end column.
        '''
        # print('moveViewToBottom')
        maxAllowedOffsetYPx = self.computeMaxAllowedVerticalOffsetPx()
        self.gridOffsetYPx = -maxAllowedOffsetYPx + 1
        self.updateStartDrawRowIndex()
        self.changed = True

    def moveViewRight(self, pixels):
        # print('moveViewRight')
        newGridXOffsetPx = self.gridOffsetXPx - pixels
        maxAllowedOffsetXPx = self.computeMaxAllowedHorizontalOffsetPx()
        if -newGridXOffsetPx >= maxAllowedOffsetXPx:
            #preventing from moving behond grid width. This avoids changing a cell value
            #for a cell outside of the internal cell value grid
            return

        self.gridOffsetXPx = newGridXOffsetPx
        self.updateStartDrawColIndex()
        print('moveViewRight', self.gridOffsetXPx)
        self.changed = True

    def moveViewToRightEnd(self):
        '''
        Sets the display to the right most or end column.
        '''
        # print('moveViewToRightEnd')
        maxAllowedOffsetXPx = self.computeMaxAllowedHorizontalOffsetPx()
        self.gridOffsetXPx = -maxAllowedOffsetXPx + 1
        self.updateStartDrawColIndex()
        print('moveViewToRightEnd', self.gridOffsetXPx)
        self.changed = True

    def computeMaxAllowedHorizontalOffsetPx(self):
        '''
        Calculates the maximum possible horizontal offset in pixels so that only columns which exist in the internal
        2 dimensions cell grid table are displayed.

        :return: maximum possible horizontal offset in px
        '''
        # calculate the pixel number required to draw a cell plus one grid line
        cellPlusSideWidthPxNumber = self.cellSize + GRID_LINE_WIDTH

        # calculate how many cells can be drawned in the cell display zone
        displayableCellNumber = (self.surface.get_width() - GRID_LINE_WIDTH - self.gridCoordMargin) / \
                                cellPlusSideWidthPxNumber

        # determine the max allowed horizontal offset in pixels according to how many cells
        # are available in the internal cell table for drawing. If we try to draw more cells,
        # we will get an out of range exception when we try to access a cell in the internal
        # cell table which does not exist (is beyhond the maximal available horizontal (x) cell number)
        maxAllowedHorizontalOffsetPx = ((self.horizontalMaxManagedCellNumber - displayableCellNumber) *
                                        cellPlusSideWidthPxNumber) - GRID_LINE_WIDTH

        return int(maxAllowedHorizontalOffsetPx)

    def computeMaxAllowedVerticalOffsetPx(self):
        '''
        Calculates the maximum possible vertical offset in pixels so that only rows which exist in the internal
        2 dimensions cell grid table are displayed.

        :return: maximum possible vertical offset in px
        '''
        # calculate the pixel number required to draw a cell plus one grid line
        cellPlusSideHeightPxNumber = self.cellSize + GRID_LINE_WIDTH

        # calculate how many cells can be drawned in the cell display zone
        displayableCellNumber = (self.surface.get_height() - GRID_LINE_WIDTH - self.gridCoordMargin) / \
                                cellPlusSideHeightPxNumber

        # determine the max allowed vertical offset in pixels according to how many cells
        # are available in the internal cell table for drawing. If we try to draw more cells,
        # we will get an out of range exception when we try to access a cell in the internal
        # cell table which does not exist (is beyhond the maximal available vertical (y) cell number)
        maxAllowedVerticalOffsetPx = ((self.verticalMaxManagedCellNumber - displayableCellNumber) *
                                        cellPlusSideHeightPxNumber) - GRID_LINE_WIDTH

        return int(maxAllowedVerticalOffsetPx)

    def moveViewLeft(self, pixels):
        # print('moveViewLeft')
        self.gridOffsetXPx += pixels
        maxAllowedOffsetXPx = self.computeMaxAllowedHorizontalOffsetPx()

        if self.gridOffsetXPx > 0:
            self.gridOffsetXPx = 0
        elif -self.gridOffsetXPx > maxAllowedOffsetXPx:
            # this can happen when zooming out and recentring the displayed zone
            self.gridOffsetXPx = -maxAllowedOffsetXPx

        self.updateStartDrawColIndex()
        print('moveViewLeft', self.gridOffsetXPx)
        self.changed = True

    def moveViewToLeftHome(self):
        '''
        Resets to the left most (0) column.
        '''
        # print('moveViewToLeftHome')
        self.gridOffsetXPx = 0
        self.updateStartDrawColIndex()
        print('moveViewToLeftHome', self.gridOffsetXPx)
        self.changed = True

    def updateStartDrawColIndex(self):
        '''
        Updates the index of the first drawned column. When the grid window is started,
        self.gridOffsetXPx has value 0. This means that the left most drawned cell obtained
        from the internal self.cellValueGrid two dimensional table has an x index value of 0.

        When moving the displayed cell portion to the left, the left most displayed cell
        column x index will become 1, then 2, etc, i.e. the positive value of the
        self.gridOffsetXPx integer divided by the current cell width + grid line width.
        '''
        self.startDrawColIndex = -self.gridOffsetXPx // (self.cellSize + GRID_LINE_WIDTH)

    def updateStartDrawRowIndex(self):
        '''
        Updates the index of the first drawned row. When the grid window is started,
        self.gridOffsetXYx has value 0. This means that the top most drawned cell obtained
        from the internal self.cellValueGrid two dimensional table has a y index value of 0.

        When moving up the displayed cell portion, the top most displayed cell
        row y index will become 1, then 2, etc, i.e. the positive value of the
        self.gridOffsetYPx integer divided by the current cell height + grid line width.
        '''
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
        '''
        Loads the grid data. If load successful, returns None. If the file was not found, returns the missing
        file name.

        :return: None if ok, missing file name if not.
        '''
        gridTable, fileNotFoundName = self.gridDataMgr.readGridData()

        if gridTable:
            self.cellValueGrid = gridTable

        return fileNotFoundName

    def initialiseCellsToValue(self, value=0):
        '''
        Sets all cells of the internal cell value grid to the initial value defined at GFrid
        construction.
        :param value: must be 0 (dead) or 1 (alive)
        '''
        self.initCellValue = value
        self.cellValueGrid = [[value for i in range(self.horizontalMaxManagedCellNumber)] for j in range(self.verticalMaxManagedCellNumber)]

