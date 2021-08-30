import time
import pymongo
from pymongo import MongoClient
from datetime import datetime
from betResult import CalculateBetResult
from readFile import readFile
from enum import Enum
from helper import WriteLog

CONNECTION_STRING = "mongodb+srv://Ryan:trantran2312@cluster0.pwc6h.mongodb.net/NimoLottery?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client["NimoLottery"]
calculationCollection = db["BeanAnalyst"]
boxCollection = db["BeanBoxesv2"]
BetHistory = db["BetHistory"]

BOXES = ["box1", "box2", "box3", "box4", "box5", "box6", "box7", "box8"]

# Return the lasted Round in logs
def GetLastestLogRound():
    return list(boxCollection.find({}).sort("time",-1).limit(1))[0]["round"]

def GetCurBoxPercentage(lastest100, input):
    counter = 0
    for item in lastest100:
        if item["box"] == input:
            counter += 1
    return counter

# Return the number of times a box not appear
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

def max1stRow(allBoxes):
    result = 0
    count = 0 
    time = 0
    for box in allBoxes:
        if box["box"] == "box1" or box["box"] == "box2" or box["box"] == "box3" or box["box"] == "box4":
            count += 1
            if count > result:
                result = count
        else:
            count = 0
    return result

def max2ndRow(allBoxes):
    result = 0
    count = 0 
    time = 0
    for box in allBoxes:
        if box["box"] == "box5" or box["box"] == "box6" or box["box"] == "box7" or box["box"] == "box8":
            count += 1
            if count > result:
                result = count
        else:
            count = 0
    return result

def BoxAppearInRow(lastest100, inputBox):
    counter = 0
    for box in lastest100:
        if box["box"] == inputBox:
            counter += 1
        else:
            return counter
    return counter

def minBox(allBoxes, inputBox):
    allBoxes = list(boxCollection.find({}).sort("time", 1))
    result = 0
    count = 0
    for i in range (0, len(allBoxes)):
        if i > 0:
            if allBoxes[i]["box"] != inputBox and (int(allBoxes[i]["round"]) == int(allBoxes[i-1]["round"]) + 1 or (int(allBoxes[i]["round"]) == 1 and int(allBoxes[i-1]["round"]==2160))):
                count += 1
                if count > result:
                    result = count
            else:
                count = 0
    return result

def maxBox(allBoxes, inputBox):
    result = 0
    count = 0
    for box in allBoxes:
        if box["box"] == inputBox:
            count += 1
            if count > result:
                result = count
        else:
            count = 0
    return result



# add more calculate the max not appear, max appear, curNotAppear, curAppear for each box and also for row
def pushCalculation(round):
    # totalCount = boxCollection.count_documents({})
    BoxesCalculation = {}
    
    lastest100 = list(boxCollection.find().sort("time",-1).limit(100))
    # allBoxes = list(boxCollection.find({}).sort("time", -1))

    for box in BOXES:
        # curCount = boxCollection.count_documents({"box": box})
        # basePercentage = curCount/totalCount * 100
        # curPercentage = GetCurBoxPercentage(lastest100, box)
        # percentageDiff = curPercentage - basePercentage
        # baseAppear = 100/basePercentage
        notAppearFor = BoxNotAppear(box)
        # appearFor = BoxAppearInRow(lastest100, box)
        # appearDiffPercentage = (notAppearFor - baseAppear) / baseAppear
        boxCalculation = {"notAppearFor": notAppearFor}
        # boxCalculation = {"basePercentage": basePercentage, "curPercentage": curPercentage, "percentageDiff": percentageDiff, 
        # "baseAppear": baseAppear, "appearFor": appearFor, "notAppearFor": notAppearFor, "minAppear": minBox(allBoxes, box), "maxAppear": maxBox(allBoxes, box),
        #  "appearDiffPercentage": appearDiffPercentage}
        BoxesCalculation[box] = boxCalculation
   
    # calculationCollection.insert_one({"round": round, "boxes": BoxesCalculation,"max1stRow": max1stRow(allBoxes),"max2ndRow": max2ndRow(allBoxes), 
    # "x50NotAppearFor": BoxX50NotAppearFor(lastest100), "x50AppearFor":BoxX50AppearFor(lastest100), "time": datetime.now()})
    
    calculationCollection.insert_one({"round": round, "boxes": BoxesCalculation, 
    "x50NotAppearFor": BoxX50NotAppearFor(lastest100), "x50AppearFor":BoxX50AppearFor(lastest100), "time": datetime.now()})

    print(f'Round: {round} analyst updated')