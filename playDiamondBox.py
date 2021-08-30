from csv import excel_tab
from os import truncate
import pymongo
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date, datetime
import time
from readFile import readFile
from helper import WriteLog
from enum import Enum
from diamondBetResult import CalculateBetResult
from diamondAnalystBox import pushCalculation

# Connect to Mongo
CONNECTION_STRING = "mongodb+srv://Ryan:trantran2312@cluster0.pwc6h.mongodb.net/NimoLottery?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client["NimoLottery"]
calculationCollection = db["DiamondAnalyst"]
boxCollection = db["DiamondBoxes"]
Emulator = db["DiamondGameEmulation"]
BetHistory = db["DiamondBetHistory"]

# Selenium load the website
chrome_options = Options()
# chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=800x600")  
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:\chromedriver\chromedriver.exe")
url = 'https://www.nimo.tv/mkt/act/super/box_lottery'
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

x45Dict = readFile("diamond - x45 bet.csv")
x45BreakPoint = x45Dict[0]["turn"]

x25Dict = readFile("diamond - x25 bet.csv")
x25BreakPoint = x25Dict[0]["turn"]

x15Dict = readFile("diamond - x15 bet.csv")
x15BreakPoint = x15Dict[0]["turn"]

x10Dict = readFile("diamond - x10 bet.csv")
x10BreakPoint = x10Dict[0]["turn"]

# caution: row 2 has a different structure
# row2Dict = readFile("diamond - row 2 bet.csv")
# row2BreakPoint = row2Dict[0]["turn"]

# row1Dict = readFile("diamond - row 1 bet.csv")
# row1BreakPoint = row1Dict[0]["turn"]

# Row1_3BoxesDict = readFile("diamond - 3 boxes row 1 bet.csv")
# Row1_3BoxesBreakPoint = Row1_3BoxesDict[0]["turn"]

Row1_1BoxDict = readFile("diamond - 1 box row 1 bet.csv")
Row1_1BoxBreakPoint = Row1_1BoxDict[0]["turn"]

def Login():
    try:
        driver.execute_script("window.scrollTo(0, 450)") 
        box1 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[1]")
        box1.click()
        time.sleep(1)
        areacode = driver.find_element_by_xpath("//i[contains(@class,'nimo-icon-caret-down')]")
        phoneNumber = driver.find_element_by_xpath("//input[contains(@class,'phone-number-input')]")
        password = driver.find_element_by_xpath("//input[@placeholder = 'Enter Password']")
        loginButton = driver.find_element_by_xpath("//button[contains(@class,'nimo-login-body-button')]")
        areacode.click()
        time.sleep(0.1)
        vietnameAreaCode = driver.find_element_by_xpath("//div[text()='Vietnam']")
        vietnameAreaCode.click()
        time.sleep(0.1)
        phoneNumber.send_keys("868242751")
        time.sleep(0.1)
        password.send_keys("4blablablabla")
        time.sleep(0.1)
        loginButton.click() 
        time.sleep(2.5)
        driver.execute_script("window.scrollTo(0, 420)") 
        time.sleep(0.3)
    except Exception as error:
        driver.refresh()
        time.sleep(2)
        Login()
        WriteLog(error, "Login Function")
    
Login()

# Return the current Round
def GetCurRound():
    try:
        return driver.find_element_by_xpath("//*[@id='container']/div/div[2]/div[2]/div/em").text
    except Exception as error:
        WriteLog(error, "GetCurRound Function")

# Return the lasted Round in logs
def GetLastestLogRound():
    try:
        return list(boxCollection.find({}).sort("time",-1).limit(1))[0]["round"]
    except Exception as error:
        WriteLog(error, "GetLastestLogRound Function")

# Return the lasted Bet Round in logs
def GetLastestcalculationBox():
    try:
        return list(calculationCollection.find({}).sort("time",-1).limit(1))[0]["round"]
    except Exception as error:
        WriteLog(error, "GetLastestCalculationBox Function")

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

        # while not box1 or not box2 or not box3 or not box4 or not box5 or not box6 or not box7 or not box8:
        #     box1 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[1]")
        #     box2 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[2]")
        #     box3 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[3]")
        #     box4 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[4]")
        #     box5 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[5]")
        #     box6 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[6]")
        #     box7 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[7]")
        #     box8 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[8]")

        if betBox == "box1":
            box1.click()
            print("Box 1 is clicked")
            time.sleep(0.5)
        if betBox == "box2":
            box2.click()
            print("Box 2 is clicked")
            time.sleep(0.5)
        if betBox == "box3":
            box3.click()
            print("Box 3 is clicked")
            time.sleep(0.5)
        if betBox == "box4":
            box4.click()
            print("Box 4 is clicked")
            time.sleep(0.5)
        if betBox == "box5":
            box5.click()
            print("Box 5 is clicked")
            time.sleep(0.5)
        if betBox == "box6":
            box6.click()
            print("Box 6 is clicked")
            time.sleep(0.5)
        if betBox == "box7":
            box7.click()
            print("Box 7 is clicked")
            time.sleep(0.5)
        if betBox == "box8":
            box8.click()
            print("Box 8 is clicked")
            time.sleep(0.5)
    except Exception as error:
        WriteLog(error, "BoxClick Function")
        

def CheckUnBet(round, betBox, betAmt):
    try:
        selectedBox = "You:0"
        if betBox == "box1":
            selectedBox = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[1]/div/div[2]").text
        if betBox == "box2":
            selectedBox = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[2]/div/div[2]").text
        if betBox == "box3":
            selectedBox = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[3]/div/div[2]").text
        if betBox == "box4":
            selectedBox = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[4]/div/div[2]").text
        if betBox == "box5":
            selectedBox = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[5]/div/div[2]").text
        if betBox == "box6":
            selectedBox = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[6]/div/div[2]").text
        if betBox == "box7":
            selectedBox = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[7]/div/div[2]").text
        if betBox == "box8":
            selectedBox = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[8]/div/div[2]").text
            
        BetedAmount = int(selectedBox[4:])
        if int(BetedAmount) < int(betAmt):
            Bet(round, betBox, int(betAmt - BetedAmount))
    except Exception as error:
        WriteLog(error, "CheckUnBet Function")
        CheckUnBet(round, betBox, betAmt)


firstBox = [True, True, True, True]
def Bet(round, betBox, betAmount):
    
    # print(f'Round {round} {betBox} betting...')
    isDone = False
    while not isDone:
        curID = -1
        try:
            bets = list(BetHistory.find({"round": round}).sort("time", -1))
            for bet in bets:
                if bet["time"].date() == datetime.today().date():
                    curID = bet["_id"]
        except Exception as error:
            print()
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
                key5k = driver.find_element_by_xpath("//*[@id='container']/div/div[5]/div[2]/div[4]")
                # print(firstBox[3])
                key5k.click()
                time.sleep(0.5)
                if firstBox[3]:
                    boxClick(betBox)
                    time.sleep(0.5)
                    while firstBox[3]:
                        try:
                            checkbox = driver.find_element_by_xpath("//*[@id='container']/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div[4]/span")
                            confirm = driver.find_element_by_xpath("//*[@id='container']/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div[2]")
                            checkbox.click()
                            time.sleep(0.5)
                            confirm.click()
                            time.sleep(0.5)
                            firstBox[3] = False
                        except:
                            break
                    for i in range (0, keys["key5k"] - 1):
                        boxClick(betBox)
                else:
                    for i in range(0, keys["key5k"]):
                        boxClick(betBox)
                
            if keys["key1k"] > 0:
                key1k = driver.find_element_by_xpath("//*[@id='container']/div/div[5]/div[2]/div[3]")
                # print(firstBox[2])
                key1k.click()
                time.sleep(0.5)
                if firstBox[2]:
                    boxClick(betBox)
                    time.sleep(0.5)
                    while firstBox[2]:
                        try:
                            checkbox = driver.find_element_by_xpath("//*[@id='container']/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div[4]/span")
                            confirm = driver.find_element_by_xpath("//*[@id='container']/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div[2]")
                            checkbox.click()
                            time.sleep(0.5)
                            confirm.click()
                            time.sleep(0.5)
                            firstBox[2] = False
                        except:
                            break
                    for i in range (0, keys["key1k"]-1):
                        boxClick(betBox)
                    
                else:
                    for i in range (0, keys["key1k"]):
                        boxClick(betBox)
            if keys["key500"] > 0:
                key500 = driver.find_element_by_xpath("//*[@id='container']/div/div[5]/div[2]/div[2]")
                # print(firstBox[1])
                key500.click()
                time.sleep(0.5)
                if firstBox[1]:
                    boxClick(betBox)
                    time.sleep(0.5)
                    while firstBox[1]:
                        try:
                            checkbox = driver.find_element_by_xpath("//*[@id='container']/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div[4]/span")
                            confirm = driver.find_element_by_xpath("//*[@id='container']/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div[2]")
                            checkbox.click()
                            time.sleep(0.5)
                            confirm.click()
                            time.sleep(0.5)
                            firstBox[1] = False
                        except:
                            break
                    for i in range (0, keys["key500"]-1):
                        boxClick(betBox)
                else:
                    for i in range(0, keys["key500"]):
                        boxClick(betBox)
            if keys["key50"] > 0:
                key50 = driver.find_element_by_xpath("//*[@id='container']/div/div[5]/div[2]/div[1]")
                # print(firstBox[0])
                key50.click()
                time.sleep(0.5)
                if firstBox[0]:
                    boxClick(betBox)
                    time.sleep(0.5)
                    while firstBox[0]:
                        try:
                            checkbox = driver.find_element_by_xpath("//*[@id='container']/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div[4]/span")
                            confirm = driver.find_element_by_xpath("//*[@id='container']/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div[2]")
                            checkbox.click()
                            time.sleep(0.5)
                            confirm.click()
                            time.sleep(0.5)
                            firstBox[0] = False
                        except:
                            break
                    for i in range (0, keys["key50"]-1):
                        boxClick(betBox)
                else:
                    for i in range (0, keys["key50"]):
                        boxClick(betBox)
            isDone = True
            print(f'Round {round} Bet {betBox} Amount {betAmount}')
        except Exception as error:
            WriteLog(error, "Bet Function (Key selecting)")
            CheckUnBet(round, betBox, betAmount)
            
           

isbet = -1
isNotBet = -1
isDisplayResult = -1
isFollowing = Case.notFollowing
isBoxCalculated = False
testing = False
testingRound = 1
while(True):
    
    try:
        curRound = int(GetCurRound())
        betRound = int(GetLastestcalculationBox())

        if(isDisplayResult != curRound):
            CalculateBetResult(curRound)
            isDisplayResult = curRound
        
        if(curRound != isbet and (curRound == betRound + 1 or curRound == 1 and betRound == 2160)):
            
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

            # Box1Appear = int(lastestBox["boxes"]["box1"]["appearFor"]) + 1
            # Box2Appear = int(lastestBox["boxes"]["box2"]["appearFor"]) + 1
            # Box3Appear = int(lastestBox["boxes"]["box3"]["appearFor"]) + 1
            # Box4Appear = int(lastestBox["boxes"]["box4"]["appearFor"]) + 1

            if x45Turn >= int(x45BreakPoint):
                print("Box 8 pre-betting")
                if isFollowing == Case.notFollowing or isFollowing == Case.x45:
                    isFollowing = Case.x45
                    betAmount = -1
                    for item in x45Dict:
                        if int(item["turn"]) == int(x45Turn):
                            betAmount = int(item["bet"])
                    if betAmount != -1:
                        Bet(curRound, "box8", betAmount)
                        # CalculateBetResult(betRound)
            elif x25Turn >= int(x25BreakPoint):
                print("Box 7 pre-betting")
                if isFollowing == Case.notFollowing or isFollowing == Case.x25:
                    isFollowing = Case.x25
                    betAmount = -1
                    for item in x25Dict:
                        if int(item["turn"]) == int(x25Turn):
                            betAmount = int(item["bet"])
                    if betAmount != -1:
                        Bet(curRound, "box7", betAmount)
                        # CalculateBetResult(betRound)
            # Right now: do not use it unless recalculate the database
            # this case is different from other cases
            # elif row2Turn >= int(row2BreakPoint):
            #     print("Row 2 pre-betting")
            #     if isFollowing == Case.notFollowing or isFollowing == Case.row2:
            #         isFollowing = Case.row2
            #         box5Amount = -1
            #         box6Amount = -1
            #         box7Amount = -1
            #         box8Amount = -1
            #         for item in row2Dict:
            #             if int(item["turn"]) == int(row2Turn):
            #                 box5Amount = int(item["box5"])
            #                 box6Amount = int(item["box6"])
            #                 box7Amount = int(item["box7"])
            #                 box8Amount = int(item["box8"])
            #         if box5Amount != -1 and box6Amount != -1 and box7Amount != -1 and box8Amount != -1:
            #             Bet(curRound, "box5", box5Amount)
            #             Bet(curRound, "box6", box6Amount)
            #             Bet(curRound, "box7", box7Amount)
            #             Bet(curRound, "box8", box8Amount)
                        # CalculateBetResult(betRound)
            elif x15Turn >= int(x15BreakPoint):
                print("Box 6 pre-betting")
                if isFollowing == Case.notFollowing or isFollowing == Case.x15:
                    isFollowing = Case.x15
                    betAmount = -1
                    for item in x15Dict:
                        if int(item["turn"]) == int(x15Turn):
                            betAmount = int(item["bet"])
                    if betAmount != -1:
                        Bet(curRound, "box6", betAmount)
                        # CalculateBetResult(betRound)
            elif x10Turn >= int(x10BreakPoint):
                print("Box 5 pre-betting")
                if isFollowing == Case.notFollowing or isFollowing == Case.x10:
                    isFollowing = Case.x10
                    betAmount = -1
                    for item in x10Dict:
                        if int(item["turn"]) == int(x10Turn):
                            betAmount = int(item["bet"])
                    if betAmount != -1:
                        Bet(curRound, "box5", betAmount)
                        # CalculateBetResult(betRound)
            #Right now do not use this, win only 50 gems if win (not worth)
            # elif row1AllTurn >= int(row1BreakPoint):
            #     print("Row 1 pre-betting")
            #     if isFollowing == Case.notFollowing or isFollowing == Case.row1All:
            #         isFollowing = Case.row1All
            #         betAmount = -1
            #         for item in row1Dict:
            #             if int(item["turn"]) == int(row1AllTurn):
            #                 betAmount = int(item["bet"])
            #         if betAmount != -1:
            #             Bet(curRound, "box1", betAmount)
            #             Bet(curRound, "box2", betAmount)
            #             Bet(curRound, "box3", betAmount)
            #             Bet(curRound, "box4", betAmount)
                        # CalculateBetResult(betRound)
            elif box1NotAppear >= int(Row1_1BoxBreakPoint):
                print("Box 1 pre-betting")
                if isFollowing == Case.notFollowing or isFollowing == Case.box1:
                    isFollowing = Case.box1
                    betAmount = -1
                    for item in Row1_1BoxDict:
                        if int(item["turn"]) == int(box1NotAppear):
                            betAmount = int(item["bet"])
                    if betAmount != -1:
                        Bet(curRound, "box1", betAmount)
                        # CalculateBetResult(betRound)
            elif box2NotAppear >= int(Row1_1BoxBreakPoint):
                print("Box 2 pre-betting")
                if isFollowing == Case.notFollowing or isFollowing == Case.box2:
                    isFollowing = Case.box2
                    betAmount = -1
                    for item in Row1_1BoxDict:
                        if int(item["turn"]) == int(box2NotAppear):
                            betAmount = int(item["bet"])
                    if betAmount != -1:
                        Bet(curRound, "box2", betAmount)
                        # CalculateBetResult(betRound)
            elif box3NotAppear >= int(Row1_1BoxBreakPoint):
                print("Box 3 pre-betting")
                if isFollowing == Case.notFollowing or isFollowing == Case.box3:
                    isFollowing = Case.box3
                    betAmount = -1
                    for item in Row1_1BoxDict:
                        if int(item["turn"]) == int(box3NotAppear):
                            betAmount = int(item["bet"])
                    if betAmount != -1:
                        Bet(curRound, "box3", betAmount)
                        # CalculateBetResult(betRound)
                
            elif box4NotAppear >= int(Row1_1BoxBreakPoint):
                print("Box 4 pre-betting")
                if isFollowing == Case.notFollowing or isFollowing == Case.box4:
                    isFollowing = Case.box4
                    betAmount = -1
                    for item in Row1_1BoxDict:
                        if int(item["turn"]) == int(box4NotAppear):
                            betAmount = int(item["bet"])
                    if betAmount != -1:
                        Bet(curRound, "box4", betAmount)
                        
                        # CalculateBetResult(betRound)
            elif testing:
                print("Testing pre-betting")
                if isFollowing == Case.notFollowing:
                    betAmount = -1
                    # for item in Row1_1BoxDict:
                    #     if int(item["turn"]) == int(box4NotAppear):
                    #         betAmount = int(item["bet"])
                    if testingRound == 1:
                        betAmount = 550
                        Bet(curRound, "box3", betAmount)
                        testingRound += 1
                    if testingRound == 2:
                        print("turn 2")
                        betAmount = 50
                        Bet(curRound, "box3", betAmount)
                testing = False
            else:
                isFollowing = Case.notFollowing
            isNotBet = curRound
            isbet = curRound
        else:
            continue
    except Exception as error:
        WriteLog(error, "Main Function")
        continue
    