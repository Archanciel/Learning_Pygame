# game options/settings
TITLE = "Draw grid"
WINDOWS_LOCATION = '100,20'
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
CELL_SIZE_OFFSET = GRID_LINE_WIDTH_TUPLE[1] #constant used when drawing an active cell to correct an unexplained
                                            #error which introduce blank pixels at top and left of the drawned
                                            #rectangle when the grid line width is bigger than 2 !

DEFAULT_CELL_SIZE = 15 #15 Windows, 35 Android
GRID_COORD_MARGIN_SIZE = 20 #20 Windows, 40 Android
GRID_MOVE_INCREMENT = 1
