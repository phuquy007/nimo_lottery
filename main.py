import pymongo
from pymongo import MongoClient
from bean_crawl import Plays

CONNECTION_STRING = "mongodb+srv://Ryan:trantran2312@cluster0.pwc6h.mongodb.net/NimoLottery?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client["NimoLottery"]
boxCollection = db["BoxesByType"]
# boxCollection = db["BeanBoxes"]

totalCount = boxCollection.count_documents({})
playPoint = 50

types = ["x5", "x10", "x15", "x25", "x45"]
breakPoint = ["200", "150", "100", "80", "50"]
def printList(collection):
    for item in collection:
        print(item["round"] + " - " + str(item["time"]))

baseBoxes = []
for type in types:
    # baseBoxes[type] = {"percentage": boxCollection.count_documents({"type": type})/totalCount }
    baseBoxes.append({"type": type, "percentage": boxCollection.count_documents({"type": type})/totalCount * 100})

print("Total Count: " + str(totalCount))
for box in baseBoxes:
    print("Box Type: " + box["type"] + " - Percentage: " + str(round(box["percentage"], 2)))

#Get 100 newest boxes
curTotal = 100
newestCollection =list(boxCollection.find().limit(100).sort("time", -1))
curBoxes = []
for type in types:
    curBoxes.append({"type": type, "percentage": sum(1 for i in newestCollection if i["type"] == type)})

for box in curBoxes:
    print("Current Box "+ box["type"] + " - " + str(box["percentage"]))

def isX5OccurAlot():
    x5LastestBoxes = list(boxCollection.find().sort("time",-1).limit(8))
    for box in x5LastestBoxes:
        if box["type"] != "x5":
            return False
    return True



# get the difference between the base and the current percentage
chosenBox = []
#Calculate the next round chosen boxes
# if x5 occur > 10, select all the 2nd row boxes
if isX5OccurAlot():
    chosenBox.append("x10")
    chosenBox.append("x15")
    chosenBox.append("x25")
    chosenBox.append("x45")
#else if if 2 or more 2nd row have the distanceDiffPercent > 30%, add these box to the chosenBoxes
else:
    sortedCollection = list(boxCollection.find({}).sort("time",-1))
    for type in types:
        curPos = sortedCollection.index(next(i for i in sortedCollection if i["type"]==type)) + 1
        basePercent = next((x for x in baseBoxes if x["type"] == type), None)["percentage"]
        baseOccur = 100 / basePercent
        occurDiff = curPos - baseOccur
        distanceDiffPecent = occurDiff/baseOccur * 100
        print("baseOccur: " + str(baseOccur) + " curPos: " + str(curPos) + " occurDiff:" + str(occurDiff) + " occurDiffPecent:" + str(distanceDiffPecent) )
        if distanceDiffPecent > playPoint:
            chosenBox.append(type)
# if len(chosenBox) <= 1:
#     chosenBox.append("x5")
#else add x5 and another box that has distanceDiffPercent > 30%


for play in chosenBox:
    print(play)
Plays(chosenBox)