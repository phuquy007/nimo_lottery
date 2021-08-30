import time
import pymongo
from pymongo import MongoClient
from datetime import datetime
from diamondBetResult import CalculateBetResult
from readFile import readFile
from enum import Enum

CONNECTION_STRING = "mongodb+srv://Ryan:trantran2312@cluster0.pwc6h.mongodb.net/NimoLottery?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client["NimoLottery"]
calculationCollection = db["DiamondAnalyst"]
boxCollection = db["DiamondBoxes"]
BetHistory = db["DiamondBetHistory"]

BOXES = ["box1", "box2", "box3", "box4", "box5", "box6", "box7", "box8"]

# Return the lasted Round in logs
def GetLastestLogRound():
    return list(boxCollection.find({}).sort("time",-1).limit(1))[0]["round"]
    
def BoxNotAppear(inputBox):
    lastestBoxAppear = int(list(boxCollection.find({"box": inputBox}).sort("time", -1).limit(1))[0]["round"])
    lastLogRound = int(GetLastestLogRound())
    result = 0
    if (lastLogRound < lastestBoxAppear):
        result = (lastLogRound - 1) + (2160 - lastestBoxAppear)
    else:
        result = lastLogRound - lastestBoxAppear
    return result

def BoxX50NotAppearFor(lastest100):
    counter = 0
    for box in lastest100:
        if box["box"] != "box1" and box["box"] != "box2" and box["box"] != "box3" and box["box"] != "box4":
            counter += 1
        else:
            return counter
    return counter

def BoxX50AppearFor(lastest100):
    counter = 0
    for box in lastest100:
        if box["box"] == "box1" or box["box"] == "box2" or box["box"] == "box3" or box["box"] == "box4" :
            counter += 1
        else:
            return counter
    return counter

def pushCalculation(round):
    BoxesCalculation = {}
    
    lastest100 = list(boxCollection.find().sort("time",-1).limit(100))

    for box in BOXES:
        notAppearFor = BoxNotAppear(box)
        boxCalculation = {"notAppearFor": notAppearFor}
        BoxesCalculation[box] = boxCalculation

    calculationCollection.insert_one({"round": round, "boxes": BoxesCalculation,
    "x50NotAppearFor": BoxX50NotAppearFor(lastest100), "x50AppearFor":BoxX50AppearFor(lastest100), "time": datetime.now()})

    print(f'Round: {round} analyst updated')