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
calculationCollection = db["BeanAnalyst"]
boxCollection = db["BeanBoxesv2"]
BetHistory = db["BetHistory"]
Emulator = db["GameEmulation"]

x45Dict = readFile("x45 bet.csv")
x45BreakPoint = x45Dict[0]["bet"]
# print(x45BreakPoint)

def getBetAmount(betCase, betTurn):
    for item in x45Dict:
        print(f'Turn: {item["turn"]} - Bet: {item["bet"]}')
        if int(item["turn"]) == int(betTurn):
            return item["bet"]
    return -1

# print(getBetAmount("", 153))

# print(datetime.date().today())

# boxes = list(boxCollection.find({}).sort("time", -1))
# print(boxes[0])
# # print(boxes[1])
# box = list(calculationCollection.find({}).sort("time", -1).limit(2))
# print(box[0])
# print(box[1])

# boxes = list(boxCollection.find({}).sort("time", -1))
# print(boxes[0])
# print(list(BetHistory.find({}).sort("time", -1).limit(1))[0])
# myDiamond = Emulator.find_one({"id": "quytran"})
# print(myDiamond["diamond"])

# lastestBox = list(calculationCollection.find({}).sort("time", -1).limit(1))[0]
# print(lastestBox["x50AppearFor"])


# BetHistory.insert_one({"Round": 12, "bets": {"box1": 10, "box2": 20}, "Time":datetime.now()})

# try:
#     bets = list(BetHistory.find({"Round": 12}).sort("Time", -1))
#     for bet in bets:
#         if bet["Time"].date() == datetime.today().date():
#             curID = bet["_id"]
# except:
#     print(f'Round : {12} - Cannot Bet')
# if curID != -1:
#     updatingBet = BetHistory.find_one({"_id": curID})
#     newBets = updatingBet["bets"]
#     newBets["box3"] = 30
#     # print(newBets)
#     BetHistory.update_one({"_id": curID}, {"$set":{"bets":newBets}})

totalBetDiamond = 0
myBet = list(BetHistory.find({}).sort("time", -1).limit(1))[0]

# for box, betAmt in myBet["bets"].items():
#     print(f'Box: {box} - Bet: {betAmt}')
#     totalBetDiamond += betAmt
# print(totalBetDiamond)

def minBox(inputBox):
    allBoxes = boxCollection.find({}).sort("time", 1)
    result = 0
    count = 0
    times = 0
    for box in allBoxes:
        if box["box"] != inputBox:
            count += 1
            if count > result:
                result = count
                print("Min : " + str(result) + " - Round: " + box["round"] + " - Time:" + str(box["time"].date()))
        else:
            if count > 63:
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
                    print("Min : " + str(result) + " - Round: " + allBoxes[i]["round"] + " - Time:" + str(allBoxes[i]["time"].date()))
            else:
                if count > 63:
                    times += 1
                count = 0
    print(times)
    return result
# print(minBox2("box7"))
def printTest():
    allBoxes = boxCollection.find({}).sort("time", 1)
    result = 0
    count = 0
    times = 0
    for box in allBoxes:
        if int(box["round"]) > 1662 and int(box["round"]) < 1895 and box["time"].date() == datetime(2021,8,28).date():
            print(f'Round {box["round"]} - {box["box"]} Time {str(box["time"].date())}')
    return result

printTest()


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