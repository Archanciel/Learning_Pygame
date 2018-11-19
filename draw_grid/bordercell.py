from draw_grid.cell import Cell
from draw_grid.settings import *

class BorderCell(Cell):
    @staticmethod

    def computeBorderCellCoordAndSize(gridView, cellRowOrColIndex, doComputeX):
        '''
        When drawing a cell on the gridView view, according to the gridView view position, a visible cell may be
        have to be partially drawned if it is at the left side of the gridView view or at its right side.
        The gridView view position is given by the parm currentGridXorYOffsetPx. For example, moving the gridView view
        10 pixels to the right will be reflected with a value of -10 for currentGridXorYOffsetPx, which means
        the underlying gridView matrix is shifted 10 pixels to the left.

        A cell located precisely at the left side of the gridView view would be drawned entirely. But if the view
        is shifted one pixel to the right (currentGridXorYOffsetPx == -1), the cell has to be partially drawned
        since 1 pixel of its left part is now outside of the gridView view. Its top left x coordinate will be 20
        (the gridView view margin size in pixels), but its size will be reduced by 1 pixel.

        The method computes the cell top left x or y coordinate aswell as its size accounting for the fact the cell
        may have to be partially drawned if part of the cell is before the gridView view left size or beyhound its right
        side. Additionnally, the displayed or not gridView view margin is taken in consideration.

        Note that the code of this method is commented regarding the horizontal dimension and its effect on the
        x cell top left coordinate. In order to keep comments readable, their adaptation to handling the vertical
        dimension (y) is left to the reader !

        :param currentGridXorYOffsetPx: x or y gridView offset in pixels
        :param borderIndependentCellXorYcoordPx: cell x or y coord as deducted from its location in the internal gridView
                                           matrix
        :param cellRowOrColIndex: index of current cell row or col in the internal gridView
                                           matrix

        :return: drawnedCellXorYcoordPx - drawned cell top left x or y pixel coordinate
                 cellSizePx - size of current cell (square in fact)
        '''
        cellSizePx = 0

        if doComputeX:
            currentGridXorYOffsetPx = gridView.gridOffsetXPx
            borderIndependentCellXorYcoordPx = Cell.computeBorderIndependentCellXCoord(gridView, cellRowOrColIndex)
        else:
            currentGridXorYOffsetPx = gridView.gridOffsetYPx
            borderIndependentCellXorYcoordPx = Cell.computeBorderIndependentCellYCoord(gridView, cellRowOrColIndex)

        drawnedCellXorYcoordPx = borderIndependentCellXorYcoordPx

        if borderIndependentCellXorYcoordPx > 0:
            # here, the current cell x coordinate is greater than the left gridView limit and so must be
            # drawn entirely or partially ...
            cellCoordOffset = gridView.gridCoordMargin - borderIndependentCellXorYcoordPx
            if cellCoordOffset > 0:
                if cellCoordOffset < gridView.gridCoordMargin:
                    # here, we moved the gridView to the left to a point where the current active cell is partially
                    # at the left of the col margin (gridView coord margin where the row/col numbers are displayed)
                    cellSizePx = gridView.cellSize - cellCoordOffset
                    drawnedCellXorYcoordPx = gridView.gridCoordMargin
                    print(Cell.getExecInfo(gridView, cellRowOrColIndex, doComputeX))
                else:
                    # here, the current active cell is behond the gridView coord margin and is drawn entirely
                    cellSizePx = gridView.cellSize
                    print(Cell.getExecInfo(gridView, cellRowOrColIndex, doComputeX))
            else:
                print(Cell.getExecInfo(gridView, cellRowOrColIndex, doComputeX))
                cellSizePx = gridView.cellSize
        else:
            # here, the current cell x coord is at the left of the left gridView limit
            cellCoordOffset = gridView.gridCoordMargin + borderIndependentCellXorYcoordPx
            if cellCoordOffset >= 0:
                if cellCoordOffset <= gridView.gridCoordMargin:
                    # here, the current active cell x coord is at the left of the left
                    # gridView limit. But part or of the cell has to be drawn for the part
                    # which is still at the right of the gridView coord margin

                    # the move offset must account for the number of columns already moved to the left ...
                    offset = currentGridXorYOffsetPx - (GRID_LINE_WIDTH + gridView.cellSize) * cellRowOrColIndex

                    cellSizePx = gridView.cellSize - offset + GRID_LINE_WIDTH
                    drawnedCellXorYcoordPx = gridView.gridCoordMargin
                    print(Cell.getExecInfo(gridView, cellRowOrColIndex, doComputeX))
                # else: this case is not possible since activeCellCoordOffset = gridView.gridCoordMargin + negative
                # value
            elif cellCoordOffset < 0:
                if abs(cellCoordOffset) <= gridView.gridCoordMargin:
                    # the move offset must account for the number of columns already moved to the left ...
                    offset = currentGridXorYOffsetPx + (GRID_LINE_WIDTH + gridView.cellSize) * cellRowOrColIndex

                    cellSizePx = gridView.cellSize + offset + GRID_LINE_WIDTH
                    drawnedCellXorYcoordPx = gridView.gridCoordMargin
                    print(Cell.getExecInfo(gridView, cellRowOrColIndex, doComputeX))
                else:
                    # the move offset must account for the number of columns already moved to the left ...
                    offset = currentGridXorYOffsetPx - (GRID_LINE_WIDTH + gridView.cellSize) * cellRowOrColIndex

                    cellwidth = gridView.cellSize - offset + GRID_LINE_WIDTH
                    cellSizePx = cellwidth
                    drawnedCellXorYcoordPx = gridView.gridCoordMargin
                    print(Cell.getExecInfo(gridView, cellRowOrColIndex, doComputeX))

        return drawnedCellXorYcoordPx, cellSizePx
