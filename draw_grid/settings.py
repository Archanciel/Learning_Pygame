# game options/settings
TITLE = "Draw grid"
WINDOWS_LOCATION = '400, 20' # 400 enables to read output in Pycharm console window !
GRID_WIDTH = 791 # grid is always a square !
GRID_HEIGHT = 791 # grid is always a square !
FPS = 20

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# grid constants

GRID_LINE_WIDTH_TUPLE = (1, 0)
#GRID_LINE_WIDTH_TUPLE = (2, 0)
#GRID_LINE_WIDTH_TUPLE = (3, 1)
#GRID_LINE_WIDTH_TUPLE = (4, 1)
#GRID_LINE_WIDTH_TUPLE = (5, 2)
#GRID_LINE_WIDTH_TUPLE = (6, 2)
#GRID_LINE_WIDTH_TUPLE = (7, 3)
#GRID_LINE_WIDTH_TUPLE = (8, 3)

GRID_LINE_WIDTH = GRID_LINE_WIDTH_TUPLE[0]
CELL_SIZE_OFFSET = GRID_LINE_WIDTH_TUPLE[1] # constant used when drawing an active cell to correct an unexplained
                                            # error which introduce blank pixels at top and left of the drawned
                                            # rectangle when the grid line width is bigger than 2 !

DEFAULT_CELL_SIZE = 15 # 15 Windows, 35 Android

# Since one cell can occupy a minimum of 1 px and the grid line width
# is 1 px at the minimum, 2 cells will require at least 1 + 1 + 1 + 1 + 1 = 5 px.
# 3 cells require at least 1 + 1 + 1 + 1 + 1 + 1 + 1 = 7 px.
# n cells require at least 1 + (n * 2) px. This explains that the smallest possible
# cell constant SMALLEST_CELL_REQUIRED_PX_NUMBER is 2 pixels.
SMALLEST_CELL_REQUIRED_PX_NUMBER = 2

# Cell size under which the grid axis label zone is no longer displayed
AXIS_HIDE_CELL_SIZE_LIMIT = 11


GRID_COORD_MARGIN_SIZE = 20 #20 Windows, 40 Android
GRID_MOVE_INCREMENT = 1
