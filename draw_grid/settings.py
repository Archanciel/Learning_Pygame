# game options/settings
TITLE = "Draw grid"
WINDOWS_LOCATION = '100,20'
GRID_SIZE = 791 # grid is always a square !
FPS = 20

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# grid constants
GRID_LINE_WIDTH = 1 #must be 1, otherwise when moving cell to left or up, white line around active cells ... I did not
                    #solved this small problem !
DEFAULT_CELL_SIZE = 15 #15 Windows, 35 Android
GRID_COORD_MARGIN_SIZE = 20 #20 Windows, 40 Android
GRID_MOVE_INCREMENT = 1
