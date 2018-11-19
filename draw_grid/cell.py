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

    @staticmethod
    def getExecInfo(gridView):
        import inspect
        import time
        previous_frame = inspect.currentframe().f_back
        (filename, line_number,
         function_name, _, _) = inspect.getframeinfo(previous_frame)
        gridViewInfo = ['gridOffsetXPx: ' + str(gridView.gridOffsetXPx), 'gridOffsetYPx: ' + str(gridView.gridOffsetYPx)]
        execInfo = int(time.time()), filename.split('\\')[-1], function_name, line_number
        return execInfo, gridViewInfo

