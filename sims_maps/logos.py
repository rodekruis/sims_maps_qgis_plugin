import csv

class RcLogos():

    def __init__(self):
        self.logos = []


    def __str__(self):
        result = u'RcLogos['
        result += len(self.logos)
        result += u']'
        return result


    def readFromCsv(self, filename):
        csvFile = open(filename, encoding=u'utf-8', mode=u'r', newline=u'')
        csvReader = csv.reader(csvFile, delimiter=';', quotechar='"')

        self.logos = []
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
