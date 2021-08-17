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
    baseBoxes.append({"type": type, "percentage": boxCollection.count_documents({"type": type})/totalCount })

print("Total Count: " + str(totalCount))
for box in baseBoxes:
    print("Box Type: " + box["type"] + " - Percentage: " + str(round(box["percentage"], 4)))

#Get the newest 100
curTotal = 100
newestCollection =list(boxCollection.find().limit(100).sort("time", -1))
curBoxes = []
for type in types:
    curBoxes.append({"type": type, "percentage": sum(1 for i in newestCollection if i["type"] == type)})

for box in curBoxes:
    print("Current Box "+ box["type"] + " - " + str(box["percentage"]))


predicts = []
