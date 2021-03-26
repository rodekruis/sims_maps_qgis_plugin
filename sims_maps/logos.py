import csv

class RcLogos():

    def __init__(self):
        self.logos = []


    def __str__(self):
        result = 'RcLogos['
        result += len(self.logos)
        result += ']'
        return result


    def readFromCsv(self, filename):
        csvFile = open(filename, encoding='utf-8', mode='r', newline='')
        csvReader = csv.reader(csvFile, delimiter=';', quotechar='"')

        self.logos = []
        #issue14: skip header of logos.csv
        next(csvReader, None)
        for row in csvReader:
            #print(row)
            self.logos.append(row)

        csvFile.close()


    def getFileNames(self, sorted=True):
        result = []
        for row in self.logos:
            result.append(row[3])
        if sorted:
            result.sort()
        return result
