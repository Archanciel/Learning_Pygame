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

    def readGridData(self):
        '''
        Loads the grid data stored in self.filename.

        :return: 2 elements tuple: first element is the 2 dimensional grid table or None if fileName not found.
                 Second element is None or the name of the missing file if fileName not found.
        '''
        twoDIntLst = []
        fileNotFoundName = None

        try:
            with open(self.filename, 'r') as file:
                reader = csv.reader(file, delimiter='\t')

                # read the header line
                next(reader)

                for row in reader:
                    intLst = [int(s) for s in row] # converting the row which contains strings into integers
                    twoDIntLst.append(intLst[1:])
        except FileNotFoundError as e:
            fileNotFoundName = e.filename
            return None, fileNotFoundName

        return twoDIntLst, fileNotFoundName
