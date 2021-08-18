import pymongo
from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://Ryan:trantran2312@cluster0.pwc6h.mongodb.net/NimoLottery?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client["NimoLottery"]
boxCollection = db["BoxesByType"]

totalCount = boxCollection.count_documents({})

types = ["x5", "x10", "x15", "x25", "x45"]
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


# get the difference between the base and the current percentage
predicts = []
for type in types:
    # get the newest of each type
    lastestBox = list(boxCollection.find({}).sort("time",-1).limit(1))
    lastestBoxByType = list(boxCollection.find({"type": type}).sort("time",-1).limit(1))
    basePercent = next((x for x in baseBoxes if x["type"] == type), None)["percentage"]
    curPercent = next((x for x in curBoxes if x["type"] == type), None)["percentage"]
    baseOccur = 100 / basePercent

    predicts.append({"type": type, "round":lastestBoxByType[0]["round"], "percentDiff": (basePercent - curPercent), "baseOccur": baseOccur, "distanceDiff": int(lastestBox[0]["round"]) - int(lastestBoxByType[0]["round"]) - baseOccur, "time": lastestBoxByType[0]["time"]})
    
for predict in predicts:
    print(predict)