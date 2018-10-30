import unittest
import os,sys,inspect
import csv
from io import StringIO

DUMMY_HEADER = ["DUMMY HEADER 1", "DUMMY HEADER 2"]

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from griddatamanager import GridDataManager

class TestGridDataManager(unittest.TestCase):#

    def testWriteGridData(self):
        csvFileName = "test.csv"
        gridDataMgr = GridDataManager(csvFileName)
        gridData = [[0, 1, 1, 0, 0],
                    [0, 1, 0, 1, 1]]
        gridDataMgr.writeGridData(gridData)

        with open(csvFileName, 'r') as csvFile:
            csvReader = csv.reader(csvFile)

            #checking header
            self.assertEqual(['\t0\t1\t2\t3\t4'], next(csvReader))

            #checking line 0
            self.assertEqual(['0\t0\t1\t1\t0\t0'], next(csvReader))

            #checking line 1
            self.assertEqual(['1\t0\t1\t0\t1\t1'], next(csvReader))

        os.remove(csvFileName)

    def testReadGridData(self):
        csvFileName = "test.csv"
        gridDataMgr = GridDataManager(csvFileName)
        gridData = [[0, 1, 1, 0, 0],
                    [0, 1, 0, 1, 1]]
        gridDataMgr.writeGridData(gridData)

        gridDataMgr = GridDataManager(csvFileName)
        gridData = gridDataMgr.readGridData()

        self.assertEqual([[0, 1, 1, 0, 0],[0, 1, 0, 1, 1]], gridData)

        os.remove(csvFileName)

if __name__ == '__main__':
    unittest.main()