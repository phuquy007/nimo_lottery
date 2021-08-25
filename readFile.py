import csv

def readFile(fileName):
    with open(fileName, mode='r') as csvFile:
        csvReader = csv.DictReader(csvFile)
        return csvReader