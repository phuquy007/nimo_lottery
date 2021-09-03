import pymongo
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date, datetime
import time
from readFile import readFile

CONNECTION_STRING = "mongodb+srv://Ryan:trantran2312@cluster0.pwc6h.mongodb.net/NimoLottery?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client["NimoLottery"]
calculationCollection = db["DiamondAnalyst"]
boxCollection = db["DiamondBoxes"]
# boxCollection = db["BeanBoxesv2"]
BetHistory = db["DiamondBetHistory"]
Emulator = db["DiamondGameEmulation"]

def GetLastestLogRound():
    return list(boxCollection.find({}).sort("time",-1).limit(1))[0]["round"]

def printTest():
    allBoxes = boxCollection.find({}).sort("time", 1)
    result = 0
    count = 0
    times = 0
    for box in allBoxes:
        if int(box["round"]) > 234 and int(box["round"]) < 251 and box["time"].date() == datetime(2021,9,2).date():
            print(f'Round {box["round"]} - {box["box"]} Time {str(box["time"].date())}')
    return result

# printTest()


def BoxNotAppear(inputBox):
    lastestBoxAppear = int(list(boxCollection.find({"box": inputBox}).sort("time", -1).limit(1))[0]["round"])
    lastLogRound = int(GetLastestLogRound())
    result = 0
    if (lastLogRound < lastestBoxAppear):
        result = (lastLogRound - 1) + (2160 - lastestBoxAppear)
    else:
        result = lastLogRound - lastestBoxAppear
    return result


def BoxNotAppear1(inputBox):
    boxes = list(boxCollection.find({}).sort("time", -1).limit(500))
    preRound = -1
    count = 0
    for box in boxes:
        if box["box"] == inputBox:
            return count
        else:
            if preRound == -1 or (preRound == 1 and int(box["round"]) == 2160) or (preRound == int(box["round"]) + 1):
                count += 1
                preRound = int(box["round"])
                continue
            else:
                return count
    return count
# print(f'Box not appear: {BoxNotAppear("box8")}')
# print(f'Box 1 not appear: {BoxNotAppear1("box1")}')
# print(f'Box 2 not appear: {BoxNotAppear1("box2")}')
# print(f'Box 3 not appear: {BoxNotAppear1("box3")}')
# print(f'Box 4 not appear: {BoxNotAppear1("box4")}')
# print(f'Box 5 not appear: {BoxNotAppear1("box5")}')
# print(f'Box 6 not appear: {BoxNotAppear1("box6")}')
# print(f'Box 7 not appear: {BoxNotAppear1("box7")}')
# print(f'Box 8 not appear: {BoxNotAppear1("box8")}')




def minBox(inputBox):
    allBoxes = list(boxCollection.find({}).sort("time", 1))
    result = 0
    count = 0
    times = 0
    for i in range (0, len(allBoxes)):
        if i > 0:
            if allBoxes[i]["box"] != inputBox and (int(allBoxes[i]["round"]) == int(allBoxes[i-1]["round"]) + 1 or (int(allBoxes[i]["round"]) == 1 and int(allBoxes[i-1]["round"]==2160))):
                count += 1
                if count > result:
                    result = count
                    print("Min : " + str(result) + " - Round: " + allBoxes[i]["round"] + " - Time:" + str(allBoxes[i]["time"].date()))
            else:
                if count > 40:
                    times += 1
                count = 0
    print(times)
    return result

def minBox2(inputBox):
    allBoxes = list(boxCollection.find({}).sort("time", 1))
    result = 0
    count = 0
    times = 0
    for i in range (0, len(allBoxes)):
        if i > 0:
            if allBoxes[i]["box"] != inputBox and (int(allBoxes[i]["round"]) == int(allBoxes[i-1]["round"]) + 1 or (int(allBoxes[i]["round"]) == 1 and int(allBoxes[i-1]["round"]==2160))):
                count += 1
                if count > result:
                    result = count
                    # print("Min : " + str(result) + " - Round: " + allBoxes[i]["round"] + " - Time:" + str(allBoxes[i]["time"].date()))
            else:
                if count > 84:
                    times += 1
                count = 0
    print(times)
    return result
print(f'Min Box 1: {minBox2("box1")}')
print(f'Min Box 2: {minBox2("box2")}')
print(f'Min Box 3: {minBox2("box3")}')
print(f'Min Box 4: {minBox2("box4")}')
print(f'Min Box 5: {minBox2("box5")}')
print(f'Min Box 6: {minBox2("box6")}')
print(f'Min Box 7: {minBox2("box7")}')
print(f'Min Box 8: {minBox2("box8")}')




def maxBox(inputBox):
    allBoxes = boxCollection.find({}).sort("time", -1)
    result = 0
    count = 0
    times = 0
    for box in allBoxes:
        if box["box"] == inputBox:
            count += 1
            if count > result:
                result = count
        else:
            if count > 2:
                times += 1
            count = 0
    print(times)
    return result

def max1stRow():
    allBoxes = boxCollection.find({}).sort("time", 1)
    result = 0
    count = 0 
    time = 0
    for box in allBoxes:
        if box["box"] == "box1" or box["box"] == "box2" or box["box"] == "box3" or box["box"] == "box4":
            count += 1
            if count > result:
                result = count
        else:
            if count > 13:
                time += 1
            count = 0
    print(time)
    return result

# print(f'Max 1st Row: {max1stRow()}')


def max2ndRow():
    allBoxes = boxCollection.find({}).sort("time", 1)
    result = 0
    count = 0 
    time = 0
    for box in allBoxes:
        if box["box"] == "box5" or box["box"] == "box6" or box["box"] == "box7" or box["box"] == "box8":
            count += 1
            if count > result:
                result = count
        else:
            if count > 3:
                time += 1
            count = 0
    print(time)
    return result

# print(f'Max 2nd Row: {max2ndRow()}')
# print(minBox("box2"))
# print(minBox("box3"))
# print(minBox("box4"))
# print(max1stRow())
# print(minBox("box2"))

# round = 302
# myBet = list(BetHistory.find({"round": int(round-1)}).sort("time", -1).limit(1))[0]
# result = list(boxCollection.find({"round": str(round)}).sort("time", -1).limit(1))[0]
# print(myBet)
# print(result)
# if(myBet["time"].date() == result["time"].date()):
#     print("Equal")