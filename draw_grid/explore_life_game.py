class World:
    '''
    This class manages the 2 dimentional representation of life game world.
    '''
    def __init__(self, size_x, size_y):
        '''
        Initializes a World with a size_x x size_y matrix initialized with 0's
        (dead cells).
        '''
        self.lines = size_x
        self.cols = size_y
        self.matrix = [['.' for _ in range(self.lines)] for _ in range(self.cols)]

    def seed(self, liveCellList):
        '''
        Seeds the World with a list of live cells. liveCellList contains a 
        list of 2 dimensional tuples denoting the 1 based li-co coordinates 
        of each seeded live cell.
        '''
        for cell in liveCellList:
            self.setCellAlive(cell[0], cell[1])

    def setCellAlive(self, li, co):
       '''
       Sets the cell with the passed 1 based (li, co) coordinates to alive.
       '''
       self.setCellValue(li, co, 'o')
       
    def isCellAlive(self, li, co):
       '''
       Returns True if the cell with the passed 1 based (li, co) coordinates 
       is alive.
       '''
       return self.getCellValue(li, co) == 'o'
       
    def setCellValue(self, li, co, value):
       '''
       Sets value of the cell with the passed 1 based (li, co) coordinates 
       to the passed value.
       '''
       self.matrix[li - 1][co - 1] =  value
                
    def getCellValue(self, li, co):
       '''
       Returns the value of the cell with the passed 1 based (li, co)
       coordinates.
       '''
       return self.matrix[li - 1][co - 1]
                
    def displayWorld(self):
        '''
        Prints a representation of the World matrix
        '''
        self._printXAxis()
        
        l = 0
        line_nb = l
        
        for li in self.matrix:
            if l > 0 and l % 10 == 0:
                tenth = str(int(l / 10))
            else:
                tenth = " "
            if l < 9:
                line_nb = tenth + str(l % 9 + 1)
            elif l == 9:
                l += 1
                line_nb = tenth + "0"
            else:
                line_nb = tenth + str(l % 10)
            print("{}".format(line_nb), end='')
            self._printLine(li)
            l += 1

    def getState(self, x, y):
        '''
        For cell (x, y), returns 1 if alive, 0 if dead. X and y are 1 based !
        '''
        
    def _printXAxis(self):
        for i in range(1, int(self.cols / 10) + 1):
            if i == 1:
                print("                    {}".format(i), end='')
            else:
                print("                   {}".format(i), end='')
            
        print()
        print("  ", end='')
        
        for j in range(self.lines):
            if j < 9:
                j = j % 9 + 1
            elif j == 9:
                continue
            else:
                j = j % 10
            print("{} ".format(j), end='')
            
        print("0")
            
    def _printLine(self, line):
        for cell in line:
            print("{} ".format(cell), end='')
            
        print()


class CellComputer:
    '''
    This class performs cell related computations.
    '''
    def __init__(self, world):
        '''
        Denotes a cell. Passed x and y coordinates are 1 based.
        '''
        self.world = world
        
    def computeNearCellsState(self, li, co):
        '''
        Sums up the state of the neighbor cells of cell located at the 
        1 based passed li, co coordinates
        '''
        ne = self.computeCellState(li - 1, co - 1)
        n = self.computeCellState(li - 1, co)
        nw = self.computeCellState(li - 1, co + 1)
        e = self.computeCellState(li, co - 1)
        w = self.computeCellState(li, co + 1)
        se = self.computeCellState(li + 1, co - 1)
        s = self.computeCellState(li + 1, co)
        sw = self.computeCellState(li + 1, co + 1)
        
        return ne + n + nw + e + w + se + s + sw
        
    def isAlive(self, li, co):
        '''
        Applies the game life rule to the cell whose 1 based (li, co) 
        coordinates are li, co.
        '''
        alive = self.world.isCellAlive(li, co)
        nearCellsTotalState = self.computeNearCellsState(li, co)
        
        return (nearCellsTotalState == 3) or (nearCellsTotalState == 2 and alive)
        
    def computeCellState(self, li, co):  
        '''
        Returns 1 if cell with 1 based (li, co) coordinates is alive, 0 else.
        '''
        if self.world.isCellAlive(li, co):
            return 1
        else:
            return 0
        
w = World(40, 40)
w.seed([(5,5), (5,6), (6,5)])
w.displayWorld()
print(w.isCellAlive(5,5))
c = CellComputer(w)
print(c.computeCellState(5,5))
print(w.isCellAlive(5,4))
print(c.computeCellState(5,4))
print(w.isCellAlive(5,6))
print(c.computeCellState(5,6))
print(c.computeNearCellsState(5,5))
print(c.isAlive(5,5))
print(c.isAlive(5,4))