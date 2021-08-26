import time
import pymongo
from pymongo import MongoClient
from datetime import datetime
from betResult import CalculateBetResult
from readFile import readFile
from enum import Enum

CONNECTION_STRING = "mongodb+srv://Ryan:trantran2312@cluster0.pwc6h.mongodb.net/NimoLottery?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client["NimoLottery"]
calculationCollection = db["BeanAnalyst"]
boxCollection = db["BeanBoxesv2"]
BetHistory = db["BetHistory"]

class Case(Enum):
    x45 = 1
    x25 = 2
    x15 = 3
    x10 = 4
    row2 = 5
    row1All = 6
    row1Three = 7
    box1 = 8
    box2 = 9
    box3 = 10
    box4 = 11
    notFollowing = 0

x45Dict = readFile("x45 bet.csv")
x45BreakPoint = x45Dict[0]["turn"]

x25Dict = readFile("x25 bet.csv")
x25BreakPoint = x25Dict[0]["turn"]

x15Dict = readFile("x15 bet.csv")
x15BreakPoint = x15Dict[0]["turn"]

x10Dict = readFile("x10 bet.csv")
x10BreakPoint = x10Dict[0]["turn"]

# caution: row 2 has a different structure
row2Dict = readFile("row 2 bet.csv")
row2BreakPoint = row2Dict[0]["turn"]

row1Dict = readFile("row 1 bet.csv")
row1BreakPoint = row1Dict[0]["turn"]

Row1_3BoxesDict = readFile("3 boxes row 1 bet.csv")
Row1_3BoxesBreakPoint = Row1_3BoxesDict[0]["turn"]

Row1_1BoxDict = readFile("1 box row 1 bet.csv")
Row1_1BoxBreakPoint = Row1_1BoxDict[0]["turn"]



def Bet(round, betBox, betAmount):
    curID = -1
    try:
        bets = list(BetHistory.find({"round": round}).sort("time", -1))
        for bet in bets:
            if bet["time"].date() == datetime.today().date():
                curID = bet["_id"]
    except:
        print(f'Round : {round} - Cannot Bet')
    if curID != -1:
        updatingBet = BetHistory.find_one({"_id": curID})
        newBets = updatingBet["bets"]
        newBets[betBox] = betAmount
        BetHistory.update_one({"_id": curID}, {"$set":{"bets":newBets}})
    else:
        BetHistory.insert_one({"round": round, "bets":{betBox: betAmount}, "time": datetime.now()})
    print(f'Round: {round} - Bet: {betBox}: {betAmount}')

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
    lastestBoxAppear = list(boxCollection.find({"box": inputBox}).sort("time", -1).limit(1))
    return int(GetLastestLogRound()) - int(lastestBoxAppear[0]["round"]) - 1

def PrintBoxesCalculation(boxesCalculation):
    for box in boxesCalculation:
        print(box["box"] 
        + " - BasePercentage: " + box["basePercentage"]
        + " - curPercentage: " + box["curPercentage"]
        + " - percentageDiff: " + box["percentageDiff"]
        + " - baseOccur: " + box["baseOccur"]
        + "-  notOccurFor: " + box["notOccurFor"]
        + "-  occurDiffPercentage: " + box["occurDiffPercentage"])

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
    result = 0
    count = 0
    for box in allBoxes:
        if box["box"] != inputBox:
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


# def calculateBet():
    

# add more calculate the max not appear, max appear, curNotAppear, curAppear for each box and also for row
def pushCalculation(round):
    totalCount = boxCollection.count_documents({})
    BoxesCalculation = {}
    
    lastest100 = list(boxCollection.find().sort("time",-1).limit(100))
    allBoxes = boxCollection.find({}).sort("time", -1)

    for box in BOXES:
        curCount = boxCollection.count_documents({"box": box})
        basePercentage = curCount/totalCount * 100
        curPercentage = GetCurBoxPercentage(lastest100, box)
        percentageDiff = curPercentage - basePercentage
        baseAppear = 100/basePercentage
        notAppearFor = BoxNotAppear(box)
        appearFor = BoxAppearInRow(lastest100, box)
        appearDiffPercentage = (notAppearFor - baseAppear) / baseAppear
        boxCalculation = {"basePercentage": basePercentage, "curPercentage": curPercentage, "percentageDiff": percentageDiff, 
        "baseAppear": baseAppear, "appearFor": appearFor, "notAppearFor": notAppearFor, "minAppear": minBox(allBoxes, box), "maxAppear": maxBox(allBoxes, box),
         "appearDiffPercentage": appearDiffPercentage}
        BoxesCalculation[box] = boxCalculation
   
    calculationCollection.insert_one({"round": round, "boxes": BoxesCalculation,"max1stRow": max1stRow(allBoxes),"max2ndRow": max2ndRow(allBoxes), 
    "x50NotAppearFor": BoxX50NotAppearFor(lastest100), "x50AppearFor":BoxX50AppearFor(lastest100), "time": datetime.now()})
    time.sleep(1)

    print(f'Round: {round} analyst updated')
    # CalculateBetResult(round)


isbet = -1
isFollowing = Case.notFollowing
while(True):
    # driver.refresh()
    # time.sleep(0.1)
    calculatedBox = list(calculationCollection.find({}).sort("time", -1).limit(1))[0]
    beanBox = list(boxCollection.find({}).sort("time", -1).limit(1))[0]
    if calculatedBox["round"] != beanBox["round"] or calculatedBox["time"].date() != beanBox["time"].date():
        pushCalculation(beanBox["round"])
    
        logRound = GetLastestLogRound()
        curRound = int(logRound) + 1
        
        if(isbet != curRound):
            chosenBox = []
            # Add box to play
            # print("Current Round: " + str(curRound))
            lastestBox = list(calculationCollection.find({}).sort("time", -1).limit(1))[0]

            # Case 1: bet the x45 box
            x45Turn = int(lastestBox["boxes"]["box8"]["notAppearFor"]) + 1
            x25Turn = int(lastestBox["boxes"]["box7"]["notAppearFor"]) + 1
            x15Turn = int(lastestBox["boxes"]["box6"]["notAppearFor"]) + 1
            x10Turn = int(lastestBox["boxes"]["box5"]["notAppearFor"]) + 1

            row2Turn = int(lastestBox["x50AppearFor"]) + 1
            row1AllTurn = int(lastestBox["x50NotAppearFor"]) + 1
            
            box1NotAppear = int(lastestBox["boxes"]["box1"]["notAppearFor"]) + 1
            box2NotAppear = int(lastestBox["boxes"]["box2"]["notAppearFor"]) + 1
            box3NotAppear = int(lastestBox["boxes"]["box3"]["notAppearFor"]) + 1
            box4NotAppear = int(lastestBox["boxes"]["box4"]["notAppearFor"]) + 1

            if x45Turn >= int(x45BreakPoint):
                if isFollowing == Case.notFollowing or isFollowing == Case.x45:
                    isFollowing = Case.x45
                    betAmount = -1
                    for item in x45Dict:
                        if int(item["turn"]) == int(x45Turn):
                            betAmount = int(item["bet"])
                    if betAmount != -1:
                        Bet(curRound, "box8", betAmount)
            
            elif x25Turn >= int(x25BreakPoint):
                if isFollowing == Case.notFollowing or isFollowing == Case.x25:
                    isFollowing = Case.x25
                    betAmount = -1
                    for item in x25Dict:
                        if int(item["turn"]) == int(x25Turn):
                            betAmount = int(item["bet"])
                    if betAmount != -1:
                        Bet(curRound, "box7", betAmount)
            # this case is different from other cases
            elif row2Turn >= int(row2BreakPoint):
                if isFollowing == Case.notFollowing or isFollowing == Case.row2:
                    isFollowing = Case.row2
                    box5Amount = -1
                    box6Amount = -1
                    box7Amount = -1
                    box8Amount = -1
                    for item in row2Dict:
                        if int(item["turn"]) == int(row2Turn):
                            box5Amount = int(item["x10"])
                            box6Amount = int(item["x15"])
                            box7Amount = int(item["x25"])
                            box8Amount = int(item["x45"])
                    if box5Amount != -1 and box6Amount != -1 and box7Amount != -1 and box8Amount != -1:
                        Bet(curRound, "box5", box5Amount)
                        Bet(curRound, "box6", box6Amount)
                        Bet(curRound, "box7", box7Amount)
                        Bet(curRound, "box8", box8Amount)

            elif x15Turn >= int(x15BreakPoint):
                if isFollowing == Case.notFollowing or isFollowing == Case.x15:
                    isFollowing = Case.x15
                    betAmount = -1
                    for item in x15Dict:
                        if int(item["turn"]) == int(x15Turn):
                            betAmount = int(item["bet"])
                    if betAmount != -1:
                        Bet(curRound, "box6", betAmount)

            elif x10Turn >= int(x10BreakPoint):
                if isFollowing == Case.notFollowing or isFollowing == Case.x10:
                    isFollowing = Case.x10
                    betAmount = -1
                    for item in x10Dict:
                        if int(item["turn"]) == int(x10Turn):
                            betAmount = int(item["bet"])
                    if betAmount != -1:
                        Bet(curRound, "box5", betAmount)
            
            elif row1AllTurn >= int(row1BreakPoint):
                if isFollowing == Case.notFollowing or isFollowing == Case.row1All:
                    isFollowing = Case.row1All
                    betAmount = -1
                    for item in row1Dict:
                        if int(item["turn"]) == int(row1AllTurn):
                            betAmount = int(item["bet"])
                    if betAmount != -1:
                        Bet(curRound, "box1", betAmount)
                        Bet(curRound, "box2", betAmount)
                        Bet(curRound, "box3", betAmount)
                        Bet(curRound, "box4", betAmount)
            
            elif box1NotAppear >= int(Row1_1BoxBreakPoint):
                if isFollowing == Case.notFollowing or isFollowing == Case.box1:
                    isFollowing = Case.box1
                    betAmount = -1
                    for item in Row1_1BoxDict:
                        if int(item["turn"]) == int(box1NotAppear):
                            betAmount = int(item["bet"])
                    if betAmount != -1:
                        Bet(curRound, "box1", betAmount)
            
            elif box2NotAppear >= int(Row1_1BoxBreakPoint):
                if isFollowing == Case.notFollowing or isFollowing == Case.box2:
                    isFollowing = Case.box2
                    betAmount = -1
                    for item in Row1_1BoxDict:
                        if int(item["turn"]) == int(box2NotAppear):
                            betAmount = int(item["bet"])
                    if betAmount != -1:
                        Bet(curRound, "box2", betAmount)
            
            elif box3NotAppear >= int(Row1_1BoxBreakPoint):
                if isFollowing == Case.notFollowing or isFollowing == Case.box3:
                    isFollowing = Case.box3
                    betAmount = -1
                    for item in Row1_1BoxDict:
                        if int(item["turn"]) == int(box3NotAppear):
                            betAmount = int(item["bet"])
                    if betAmount != -1:
                        Bet(curRound, "box3", betAmount)

            elif box4NotAppear >= int(Row1_1BoxBreakPoint):
                if isFollowing == Case.notFollowing or isFollowing == Case.box4:
                    isFollowing = Case.box4
                    betAmount = -1
                    for item in Row1_1BoxDict:
                        if int(item["turn"]) == int(box4NotAppear):
                            betAmount = int(item["bet"])
                    if betAmount != -1:
                        Bet(curRound, "box4", betAmount)
            elif curRound == 211:
                Bet(curRound, "box1", 50)
                Bet(curRound, "box2", 50)
                Bet(curRound, "box3", 50)
                Bet(curRound, "box4", 50)
                Bet(curRound, "box5", 50)
                Bet(curRound, "box6", 50)
                Bet(curRound, "box7", 50)
                Bet(curRound, "box8", 50)
            elif curRound == 212:
                Bet(curRound, "box1", 50)
            elif curRound == 213:
                Bet(curRound, "box2", 100)
            elif curRound == 214:
                Bet(curRound, "box3", 150)
            elif curRound == 215:
                Bet(curRound, "box4", 200)
            elif curRound == 216:
                Bet(curRound, "box5", 250)
            elif curRound == 217:
                Bet(curRound, "box6", 300)
            elif curRound == 218:
                Bet(curRound, "box7", 350)
            elif curRound == 219:
                Bet(curRound, "box8", 400)
            else:
                isFollowing = Case.notFollowing
                print(f'Round: {curRound} not bet!')
            isbet = curRound

            CalculateBetResult(logRound)