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
            csvFileHeader = [i for i in range(0, len(gridData[0]))]
            writer.writerow(csvFileHeader)

            # write grid data
            writer.writerows(gridData)

    def readGridData(self):
        twoDIntLst = []

        with open(self.filename, 'r') as file:
            reader = csv.reader(file, delimiter='\t')

            # read the header line
            next(reader)

            for row in reader:
                intLst = [int(s) for s in row] # converting the row which contains strings into integers
                twoDIntLst.append(intLst)

        return twoDIntLst
