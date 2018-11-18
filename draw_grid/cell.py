from draw_grid.settings import *

class Cell:
    @staticmethod
    def computeBorderIndependentCellXCoord(gridView, col):
        return gridView.gridCoordMargin + GRID_LINE_WIDTH - gridView.gridOffsetXPx + (
                (GRID_LINE_WIDTH + gridView.cellSize) * col)

    @staticmethod
    def computeBorderIndependentCellYCoord(gridView, row):
        return gridView.gridCoordMargin + GRID_LINE_WIDTH - gridView.gridOffsetYPx + (
                (GRID_LINE_WIDTH + gridView.cellSize) * row)

