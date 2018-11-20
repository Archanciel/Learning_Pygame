import csv

class GridDataManager():
    '''
    This class reads/writes the internal grid data from/to a csv file.
    '''

    def __init__(self, filename):
        self.filename = filename

    def writeGridData(self, gridData):
        with open(self.filename, 'w', newline = '') as file:
            writer = csv.writer(file, delimiter = '\t')

            # write col header row
            csvFileHeader = [''] + [i for i in range(0, len(gridData[0]))]
            writer.writerow(csvFileHeader)

            for li in range(0, len(gridData)):
                line = [li] + gridData[li]
                writer.writerow(line)

    def readGridData(self, requiredDimX, requiredDimY):
        '''
        Loads the grid data stored in self.filename. If the input file contains less data than what is
        required to fill a grid table of dimension dimX x dimY, empty (0) cells are added to the
        data read from the input file so that a dimX x dimY matrix is returned to the caller.

        :param requiredDimX: 1 based horizontal dimension of returned grid table
        :param requiredDimY: 1 based vertical dimension of returned grid table

        :return: 2 elements tuple: first element is the 2 dimensional grid matrix (list of list) or None
                 if fileName not found.

                 Second element is None or the name of the missing file if fileName not found.
        '''
        twoDIntMatrix = []
        fileNotFoundName = None

        try:
            with open(self.filename, 'r') as file:
                reader = csv.reader(file, delimiter='\t')

                # reading the header line and use it to determine the x dimension of the input data

                header = next(reader)
                dataDimX = len(header) - 1
                fillerDimX = 0

                if dataDimX < requiredDimX:
                    fillerDimX = requiredDimX - dataDimX

                dataDimY = 0

                for row in reader:
                    dataDimY += 1
                    intLst = [int(s) for s in row] # converting the row which contains strings into integers
                    cellDataRow = intLst[1:] # stripping off col 0 which contains line numbers
                    if fillerDimX > 0:
                        fillerList = [0 for _ in range(fillerDimX)]
                    else:
                        fillerList = []
                    twoDIntMatrix.append(cellDataRow + fillerList)

                if dataDimY < requiredDimY:
                    fillerDimY = requiredDimY - dataDimY

                for _ in range(fillerDimY):
                    twoDIntMatrix.append([0 for _ in range(requiredDimY)])
        except FileNotFoundError as e:
            fileNotFoundName = e.filename
            return None, fileNotFoundName

        return twoDIntMatrix, fileNotFoundName
