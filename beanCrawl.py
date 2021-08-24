from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pymongo
from pymongo import MongoClient
from datetime import datetime

chrome_options = Options()

chrome_options.add_argument("--window-size=10x10")  
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:\chromedriver\chromedriver.exe")

CONNECTION_STRING = "mongodb+srv://Ryan:trantran2312@cluster0.pwc6h.mongodb.net/NimoLottery?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client["NimoLottery"]
calculationCollection = db["BeanAnalyst"]
boxCollection = db["BeanBoxesv2"]

url = 'https://www.nimo.tv/mkt/act/super/bean_box_lottery'
driver.get(url)
time.sleep(1)

PRIZE = "prize-box"
NOPRIZE = "no-prize-box"
BOXES = ["box1", "box2", "box3", "box4", "box5", "box6", "box7", "box8"]

def GenerateBreakPoints():
    breakPoints = {"box1": 200, "box2": 200, "box3": 200, "box4": 200, "box5": 180, "box6": 160, "box7": 140, "box8":120}
    return breakPoints

def GetBreakPoint():
    try:
        document = list(calculationCollection.find({}).sort("time", -1).limit(1))[0]
    except:
        return GenerateBreakPoints()
    if(document["breakPoints"]):
        return document["breakPoints"]
    else:
        return GenerateBreakPoints()

# Return the current Round
def GetCurRound():
    return driver.find_element_by_xpath("//*[@id='container']/div/div[2]/div[2]/div/em").text

# Return the lasted Round in logs
def GetLastestLogRound():
    return list(boxCollection.find({}).sort("time",-1).limit(1))[0]["round"]

def pushToMongo(box):
    boxCollection.insert_one(box)
    
def printBox(box):
    print("Round: " + box["round"] + " Type: " + box["type"])

def GetCurBoxPercentage(input):
    list100 = boxCollection.find({}).sort("time", -1).limit(100)
    counter = 0
    for item in list100:
        if item["box"] == input:
            counter += 1
    return counter

# Return the number of times a box not appear
def BoxNotAppear(box):
    lastestBoxAppear = list(boxCollection.find({"box": box}).sort("time", -1).limit(1))
    return int(GetCurRound()) - int(lastestBoxAppear[0]["round"]) -1

def PrintBoxesCalculation(boxesCalculation):
    for box in boxesCalculation:
        print(box["box"] 
        + " - BasePercentage: " + box["basePercentage"]
        + " - curPercentage: " + box["curPercentage"]
        + " - percentageDiff: " + box["percentageDiff"]
        + " - baseOccur: " + box["baseOccur"]
        + "-  notOccurFor: " + box["notOccurFor"]
        + "-  occurDiffPercentage: " + box["occurDiffPercentage"])

def BoxX50NotAppearFor():
    counter = 0
    lastestBoxes = list(boxCollection.find().sort("time",-1).limit(50))
    for box in lastestBoxes:
        if box["box"] != "box1" and box["box"] != "box2" and box["box"] != "box3" and box["box"] != "box4":
            counter += 1
        else:
            return counter
    return counter

def BoxX50AppearFor():
    counter = 0
    lastestBoxes = list(boxCollection.find().sort("time",-1).limit(100))
    for box in lastestBoxes:
        if box["box"] == "box1" or box["box"] == "box2" or box["box"] == "box3" or box["box"] == "box4" :
            counter += 1
        else:
            return counter
    return counter

def BoxAppearInRow(inputBox):
    counter = 0
    lastestBoxes = list(boxCollection.find().sort("time",-1).limit(30))
    for box in lastestBoxes:
        if box["box"] == inputBox:
            counter += 1
        else:
            return counter
    return counter

# Get the max appear of a box: called max
# Get the max not appear of a box: called min
def minMaxAppear(minOrMax, inputBox):
    allBoxes = boxCollection.find()
    result = 0
    count = 0
    for box in allBoxes:
        if(minOrMax.lower() == max):
            if box["box"] == inputBox:
                count += 1
                if count > result:
                    result = count
            else:
                count = 0
        else:
            if box["box"] != inputBox:
                count += 1
                if count > result:
                    result = count
            else:
                count = 0
    return result

def Add1stRow(chosenBox):
    for i in range (1, 5):
        chosenBox.append("box"+str(i))

def Add2ndRow(chosenBox):
    for i in range (5, 9):
        chosenBox.append("box"+str(i))


# add more calculate the max not appear, max appear, curNotAppear, curAppear for each box and also for row
def pushCalculation():
    totalCount = boxCollection.count_documents({})
    BoxesCalculation = {}
    
    for box in BOXES:
        curCount = boxCollection.count_documents({"box": box})
        basePercentage = curCount/totalCount * 100
        curPercentage = GetCurBoxPercentage(box)
        percentageDiff = curPercentage - basePercentage
        baseAppear = 100/basePercentage
        notAppearFor = BoxNotAppear(box)
        appearFor = BoxAppearInRow(box)
        appearDiffPercentage = (notAppearFor - baseAppear) / baseAppear
        boxCalculation = {"basePercentage": basePercentage, "curPercentage": curPercentage, "percentageDiff": percentageDiff, 
        "baseAppear": baseAppear, "appearFor": appearFor, "notAppearFor": notAppearFor, "minAppear": minMaxAppear("min", box), "maxAppear": minMaxAppear("max", box),
         "appearDiffPercentage": appearDiffPercentage, "time": datetime.now()}
        BoxesCalculation[box] = boxCalculation
        breakPoints = GetBreakPoint()
   
    calculationCollection.insert_one({"Round": GetCurRound(), "Boxes": BoxesCalculation, "x50NotAppearFor": BoxX50NotAppearFor(), "x50AppearFor":BoxX50AppearFor(),
    "breakPoints": breakPoints})

    print(boxCalculation)

round = None
while(True):
    # driver.refresh()
    # time.sleep(0.1)
    curRound = driver.find_element_by_xpath("//*[@id='container']/div/div[2]/div[2]/div/em").text
    prizebox = None
    boxes = []
    try:
        for i in range(1, 9):
            box = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div["+str(i)+"]")
            if PRIZE in box.get_attribute("class")and NOPRIZE not in box.get_attribute("class"):
                if not prizebox:
                    prizebox = "box" + str(i)
    except: 
        continue
    if prizebox and round != curRound:
        round = curRound
        newBox = {"round": round, "box": prizebox, "time": datetime.now()}
        pushToMongo(newBox)
        print("Round: " + round +" - box: " + str(prizebox))
        pushCalculation()
       
        time.sleep(5)