from draw_grid.settings import *

class CenterCell():
    '''
    Thia class calculates the horizontal (x) and vertical (y) offset caused by a zoom in or out operation.
    These offsets will be used by the GridView class to reposition the grid view so that the zoomed zone
    remains centered in the view.
    '''
    def __init__(self, gridView):
        '''
        The MidCell instance is created before the zoom operation takes place. It records the coordinates of
        the cell positioned at the center of the grid view so that they can be compared to the mid cell
        coordinates after the zoom occured in  order to adjust the grid view positioning, if possible, so that
        the mid cell remains centered.

        :param gridView:
        '''
        self.gridView = gridView

        # computing the row/col index of the cell displaed in the middle of the grid view before the zoom occurs
        self.midCellRowIndexBeforeZoom = gridView.startDrawRowIndex + (gridView.drawnedRowNb // 2) - 1 # minus 1 since 0 based !
        self.midCellColIndexolBeforeZoom = gridView.startDrawColIndex + (gridView.drawnedColNb // 2) - 1

        # computing the top left x and y coordinates of the mid cell before the zoom operation

        self.midCellTopLeftXCoordBeforeZoom = gridView.gridCoordMargin + GRID_LINE_WIDTH + gridView.gridOffsetXPx + (
                (GRID_LINE_WIDTH + gridView.cellSize) * self.midCellColIndexolBeforeZoom)

        self.midCellTopLeftYCoordBeforeZoom = gridView.gridCoordMargin + GRID_LINE_WIDTH + gridView.gridOffsetYPx + (
                (GRID_LINE_WIDTH + gridView.cellSize) * self.midCellRowIndexBeforeZoom)

    def computeXYOffsetAfterZoom(self):
        '''
        This method is called after the zoom operation occured. It return the horizontal (x) and vertical (y)
        offset to be applied to the grid view, if possible, to keep the mid cell at the center of the grid view.

        :return: zoomXOffsetPx and zoomYOffsetPx tuple
        '''
        # computing the top left x and y coordinates of the mid cell after the zoom operation

        topLeftXCoordPxAfterZoom = self.gridView.gridCoordMargin + GRID_LINE_WIDTH + self.gridView.gridOffsetXPx + (
                (GRID_LINE_WIDTH + self.gridView.cellSize) * self.midCellColIndexolBeforeZoom)

        topLeftYCoordPxAfterZoom = self.gridView.gridCoordMargin + GRID_LINE_WIDTH + self.gridView.gridOffsetYPx + (
                (GRID_LINE_WIDTH + self.gridView.cellSize) * self.midCellRowIndexBeforeZoom)

        # calculating the x and y offset caused ba the zoom operation
        zoomXOffsetPx = self.midCellTopLeftXCoordBeforeZoom - topLeftXCoordPxAfterZoom
        zoomYOffsetPx = self.midCellTopLeftYCoordBeforeZoom - topLeftYCoordPxAfterZoom

        return zoomXOffsetPx, zoomYOffsetPx