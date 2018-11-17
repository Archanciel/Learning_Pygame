from draw_grid.cell import Cell
from draw_grid.settings import *

class CenterCell(Cell):
    '''
    Thia class calculates the horizontal (x) and vertical (y) offset caused by a zoom in or out operation.
    These offsets will be used by the GridView class to reposition the grid view so that the zoomed zone
    remains centered in the view.
    '''
    def __init__(self, gridView):
        '''
        The CenterCell instance is created before the zoom operation takes place. It records the coordinates of
        the cell positioned at the center of the grid view so that they can be compared to the mid cell
        coordinates after the zoom occured in  order to adjust the grid view positioning, if possible, so that
        the mid cell remains centered.

        :param gridView:
        '''
        self.gridView = gridView

        # computing the row/col index of the cell displaed in the middle of the grid view before the zoom occurs
        self.centerCellRowIndexBeforeZoom = gridView.startDrawRowIndex + (gridView.gridViewDisplayableRowNb // 2) - 1 # minus 1 since 0 based !
        self.centerCellColIndexBeforeZoom = gridView.startDrawColIndex + (gridView.gridViewDisplayableColNb // 2) - 1

        # computing the top left x and y coordinates of the mid cell before the zoom operation
        self.centerCellTopLeftXCoordBeforeZoom = super().computeBorderIndependentCellXCoord(gridView, self.centerCellColIndexBeforeZoom)
        self.centerCellTopLeftYCoordBeforeZoom = super().computeBorderIndependentCellXCoord(gridView, self.centerCellRowIndexBeforeZoom)

    def computeXYOffsetAfterZoom(self):
        '''
        This method is called after the zoom operation occured. It return the horizontal (x) and vertical (y)
        offset to be applied to the grid view, if possible, to keep the mid cell at the center of the grid view.

        :return: zoomXOffsetPx and zoomYOffsetPx tuple
        '''
        # computing the top left x and y coordinates of the mid cell after the zoom operation
        topLeftXCoordPxAfterZoom = super().computeBorderIndependentCellXCoord(self.gridView, self.centerCellColIndexBeforeZoom)
        topLeftYCoordPxAfterZoom = super().computeBorderIndependentCellXCoord(self.gridView, self.centerCellRowIndexBeforeZoom)

        # calculating the x and y offset caused ba the zoom operation
        zoomXOffsetPx = self.centerCellTopLeftXCoordBeforeZoom - topLeftXCoordPxAfterZoom
        zoomYOffsetPx = self.centerCellTopLeftYCoordBeforeZoom - topLeftYCoordPxAfterZoom

        return zoomXOffsetPx, zoomYOffsetPx