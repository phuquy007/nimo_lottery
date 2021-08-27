from os import truncate
import pymongo
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
from readFile import readFile
from enum import Enum
from betResult import CalculateBetResult
from analystBox import pushCalculation

# Connect to Mongo
CONNECTION_STRING = "mongodb+srv://Ryan:trantran2312@cluster0.pwc6h.mongodb.net/NimoLottery?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client["NimoLottery"]
calculationCollection = db["BeanAnalyst"]
boxCollection = db["BeanBoxesv2"]
Emulator = db["GameEmulation"]
BetHistory = db["BetHistory"]

# Selenium load the website
chrome_options = Options()
# chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=800x600")  
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:\chromedriver\chromedriver.exe")
url = 'https://www.nimo.tv/mkt/act/super/bean_box_lottery'
driver.get(url)
time.sleep(2)

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

TOTAL_COUNT = boxCollection.count_documents({})

BOXES = ["box1", "box2", "box3", "box4", "box5", "box6", "box7", "box8"]

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

# Return the current Round
def GetCurRound():
    return driver.find_element_by_xpath("//*[@id='container']/div/div[2]/div[2]/div/em").text

# Return the lasted Round in logs
def GetLastestLogRound():
    return list(boxCollection.find({}).sort("time",-1).limit(1))[0]["round"]

# Return the lasted Bet Round in logs
def GetLastestcalculationBox():
    return list(calculationCollection.find({}).sort("time",-1).limit(1))[0]["round"]

def calculateKeys(betAmt):
    key5k = betAmt // 5000
    betAmt = betAmt % 5000
    key1k = betAmt // 1000
    betAmt = betAmt % 1000
    key500 = betAmt // 500
    betAmt = betAmt % 500
    key50 = betAmt // 50
    return {"key5k": key5k, "key1k": key1k, "key500": key500, "key50": key50}

def boxClick(betBox):
    try:
        box1 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[1]")
        box2 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[2]")
        box3 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[3]")
        box4 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[4]")
        box5 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[5]")
        box6 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[6]")
        box7 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[7]")
        box8 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[8]")

        if betBox == "box1":
            box1.click()
            time.sleep(0.2)
        if betBox == "box2":
            box2.click()
            time.sleep(0.2)
        if betBox == "box3":
            box3.click()
            time.sleep(0.2)
        if betBox == "box4":
            box4.click()
            time.sleep(0.2)
        if betBox == "box5":
            box5.click()
            time.sleep(0.2)
        if betBox == "box6":
            box6.click()
            time.sleep(0.2)
        if betBox == "box7":
            box7.click()
            time.sleep(0.2)
        if betBox == "box8":
            box8.click()
            time.sleep(0.2)
    except:
        print(f'Cannot click {betBox}')
    
def Bet(round, betBox, betAmount):
    isDone = False
    while not isDone:
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
        
        keys = calculateKeys(int(betAmount))

        try:
            key50 = driver.find_element_by_xpath("//*[@id='container']/div/div[5]/div[2]/div[1]")
            key500 = driver.find_element_by_xpath("//*[@id='container']/div/div[5]/div[2]/div[2]")
            key1k = driver.find_element_by_xpath("//*[@id='container']/div/div[5]/div[2]/div[3]")
            key5k = driver.find_element_by_xpath("//*[@id='container']/div/div[5]/div[2]/div[4]")

            if keys["key5k"] > 0:
                key5k.click()
                time.sleep(0.2)
                boxClick(betBox)
                try:
                    checkbox = driver.find_element_by_xpath("//*[@id='container']/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div[4]/span")
                    confirm = driver.find_element_by_xpath("//*[@id='container']/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div[2]")
                    checkbox.click()
                    time.sleep(0.2)
                    confirm.click()
                    time.sleep(0.2)
                except:
                    print()
                for i in range (0, keys["key5k"] - 1):
                    boxClick(betBox)
            if keys["key1k"] > 0:
                key1k.click()
                time.sleep(0.2)
                boxClick(betBox)
                try:
                    checkbox = driver.find_element_by_xpath("//*[@id='container']/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div[4]/span")
                    confirm = driver.find_element_by_xpath("//*[@id='container']/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div[2]")
                    checkbox.click()
                    time.sleep(0.2)
                    confirm.click()
                    time.sleep(0.2)
                except:
                    print()
                for i in range (0, keys["key1k"]-1):
                    boxClick(betBox)
            if keys["key500"] > 0:
                key500.click()
                time.sleep(0.2)
                boxClick(betBox)
                try:
                    checkbox = driver.find_element_by_xpath("//*[@id='container']/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div[4]/span")
                    confirm = driver.find_element_by_xpath("//*[@id='container']/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div[2]")
                    checkbox.click()
                    time.sleep(0.2)
                    confirm.click()
                    time.sleep(0.2)
                except:
                    print()
                for i in range (0, keys["key500"]-1):
                    boxClick(betBox)
            if keys["key50"] > 0:
                key50.click()
                time.sleep(0.2)
                for i in range (0, keys["key50"]):
                    boxClick(betBox)
            isDone = True
        except:
            continue
        
        


isbet = -1
isFollowing = Case.notFollowing
isBoxCalculated = False
while(True):
    # driver.refresh()
    # time.sleep(5)

    calculatedBox = list(calculationCollection.find({}).sort("time", -1).limit(1))[0]
    lastLogBox = list(boxCollection.find({}).sort("time", -1).limit(1))[0]
    if calculatedBox["round"] != lastLogBox["round"] and calculatedBox["time"].date() != lastLogBox["time"].date():
        pushCalculation(lastLogBox["round"])
        isBoxCalculated = True
        time.sleep(1)
    
    
    curRound = int(GetCurRound())
    betRound = int(GetLastestcalculationBox())
    
    if(betRound != isbet and (curRound == betRound+1 or curRound == 1)):
            
        chosenBox = []
        # Add box to play
        # print("Current Round: " + str(curRound))
        lastestBox = list(calculationCollection.find({}).sort("time", -1).limit(1))[0]

        # Case 1: bet the x45 box
        x45Turn = int(lastestBox["Boxes"]["box8"]["notAppearFor"]) + 1
        x25Turn = int(lastestBox["Boxes"]["box7"]["notAppearFor"]) + 1
        x15Turn = int(lastestBox["Boxes"]["box6"]["notAppearFor"]) + 1
        x10Turn = int(lastestBox["Boxes"]["box5"]["notAppearFor"]) + 1

        row2Turn = int(lastestBox["x50AppearFor"]) + 1
        row1AllTurn = int(lastestBox["x50NotAppearFor"]) + 1
        
        box1NotAppear = int(lastestBox["Boxes"]["box1"]["notAppearFor"]) + 1
        box2NotAppear = int(lastestBox["Boxes"]["box2"]["notAppearFor"]) + 1
        box3NotAppear = int(lastestBox["Boxes"]["box3"]["notAppearFor"]) + 1
        box4NotAppear = int(lastestBox["Boxes"]["box4"]["notAppearFor"]) + 1

        Box1Appear = int(lastestBox["Boxes"]["box1"]["appearFor"]) + 1
        Box2Appear = int(lastestBox["Boxes"]["box2"]["appearFor"]) + 1
        Box3Appear = int(lastestBox["Boxes"]["box3"]["appearFor"]) + 1
        Box4Appear = int(lastestBox["Boxes"]["box4"]["appearFor"]) + 1

        if x45Turn >= int(x45BreakPoint):
            if isFollowing == Case.notFollowing or isFollowing == Case.x45:
                isFollowing = Case.x45
                betAmount = -1
                for item in x45Dict:
                    if int(item["turn"]) == int(x45Turn):
                        betAmount = int(item["bet"])
                if betAmount != -1:
                    Bet(betRound, "box8", betAmount)
        
        elif x25Turn >= int(x25BreakPoint):
            if isFollowing == Case.notFollowing or isFollowing == Case.x25:
                isFollowing = Case.x25
                betAmount = -1
                for item in x25Dict:
                    if int(item["turn"]) == int(x25Turn):
                        betAmount = int(item["bet"])
                if betAmount != -1:
                    Bet(betRound, "box7", betAmount)
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
                        box5Amount = int(item["box5"])
                        box6Amount = int(item["box6"])
                        box7Amount = int(item["box7"])
                        box8Amount = int(item["box8"])
                if box5Amount != -1 and box6Amount != -1 and box7Amount != -1 and box8Amount != -1:
                    Bet(betRound, "box5", box5Amount)
                    Bet(betRound, "box6", box6Amount)
                    Bet(betRound, "box7", box7Amount)
                    Bet(betRound, "box8", box8Amount)

        elif x15Turn >= int(x15BreakPoint):
            if isFollowing == Case.notFollowing or isFollowing == Case.x15:
                isFollowing = Case.x15
                betAmount = -1
                for item in x15Dict:
                    if int(item["turn"]) == int(x15Turn):
                        betAmount = int(item["bet"])
                if betAmount != -1:
                    Bet(betRound, "box6", betAmount)

        elif x10Turn >= int(x10BreakPoint):
            if isFollowing == Case.notFollowing or isFollowing == Case.x10:
                isFollowing = Case.x10
                betAmount = -1
                for item in x10Dict:
                    if int(item["turn"]) == int(x10Turn):
                        betAmount = int(item["bet"])
                if betAmount != -1:
                    Bet(betRound, "box5", betAmount)
        
        elif row1AllTurn >= int(row1BreakPoint):
            if isFollowing == Case.notFollowing or isFollowing == Case.row1All:
                isFollowing = Case.row1All
                betAmount = -1
                for item in row1Dict:
                    if int(item["turn"]) == int(row1AllTurn):
                        betAmount = int(item["bet"])
                if betAmount != -1:
                    Bet(betRound, "box1", betAmount)
                    Bet(betRound, "box2", betAmount)
                    Bet(betRound, "box3", betAmount)
                    Bet(betRound, "box4", betAmount)
        
        elif box1NotAppear >= int(Row1_1BoxBreakPoint):
            if isFollowing == Case.notFollowing or isFollowing == Case.box1:
                isFollowing = Case.box1
                betAmount = -1
                for item in Row1_1BoxDict:
                    if int(item["turn"]) == int(box1NotAppear):
                        betAmount = int(item["bet"])
                if betAmount != -1:
                    Bet(betRound, "box1", betAmount)
        
        elif box2NotAppear >= int(Row1_1BoxBreakPoint):
            if isFollowing == Case.notFollowing or isFollowing == Case.box2:
                isFollowing = Case.box2
                betAmount = -1
                for item in Row1_1BoxDict:
                    if int(item["turn"]) == int(box2NotAppear):
                        betAmount = int(item["bet"])
                if betAmount != -1:
                    Bet(betRound, "box2", betAmount)
        
        elif box3NotAppear >= int(Row1_1BoxBreakPoint):
            if isFollowing == Case.notFollowing or isFollowing == Case.box3:
                isFollowing = Case.box3
                betAmount = -1
                for item in Row1_1BoxDict:
                    if int(item["turn"]) == int(box3NotAppear):
                        betAmount = int(item["bet"])
                if betAmount != -1:
                    Bet(betRound, "box3", betAmount)

        elif box4NotAppear >= int(Row1_1BoxBreakPoint):
            if isFollowing == Case.notFollowing or isFollowing == Case.box4:
                isFollowing = Case.box4
                betAmount = -1
                for item in Row1_1BoxDict:
                    if int(item["turn"]) == int(box4NotAppear):
                        betAmount = int(item["bet"])
                if betAmount != -1:
                    Bet(betRound, "box4", betAmount)
        else:
            isFollowing = Case.notFollowing

        isbet = curRound
        CalculateBetResult(betRound)
        # time.sleep(5)
    else:
        continue
    
    