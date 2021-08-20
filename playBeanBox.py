import pymongo
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time

# Connect to Mongo
CONNECTION_STRING = "mongodb+srv://Ryan:trantran2312@cluster0.pwc6h.mongodb.net/NimoLottery?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client["NimoLottery"]
boxCollection = db["BeanBoxes"]

# Selenium load the website
chrome_options = Options()
# chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=10x10")  
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:\chromedriver\chromedriver.exe")
url = 'https://www.nimo.tv/mkt/act/super/bean_box_lottery'
driver.get(url)
time.sleep(20)

totalCount = boxCollection.count_documents({})

types = ["x5", "x10", "x15", "x25", "x45"]
breakPoints = {"x5": 200, "x10": 200, "x15": 150, "x25": 100, "x45": 80}

# 8 times x1 box
# 9 times x1 box
# 10 times x2 box
# 11 times x4 box
# 12 times x8 box
def isX50notAppear():
    notX5Count = 0
    lastestBoxes = list(boxCollection.find().sort("time",-1).limit(10))
    for box in lastestBoxes:
        if box["type"] != "x5":
            notX5Count += 1
        else:
            return notX5Count
    return notX5Count

def isX5OccurAlot():
    x5Count = 0
    x5LastestBoxes = list(boxCollection.find().sort("time",-1).limit(20))
    for x5Box in x5LastestBoxes:
        if x5Box["type"] == "x5":
            x5Count += 1
        else:
            return x5Count
    return x5Count
isbet = -1

# count how many times x5 appear in a row
while(True):
    driver.refresh()
    time.sleep(5)
    curRound = driver.find_element_by_xpath("//*[@id='container']/div/div[2]/div[2]/div/em").text
    logRound = list(boxCollection.find({}).sort("time",-1).limit(1))[0]["round"]
    
    if(curRound == logRound and curRound != isbet):
        try:
            box1 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[1]")
            box2 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[2]")
            box3 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[3]")
            box4 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[4]")
            box5 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[5]")
            box6 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[6]")
            box7 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[7]")
            box8 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[8]")

            # x500Key = driver.find_element_by_xpath("//*[@id='container']/div/div[5]/div[2]/div[2]")
            # x500Key.click()
        except:
            continue
        chosenBox = []
        if isX5OccurAlot() >= 13:
            for i in range (13, isX5OccurAlot()+1):
                chosenBox.append("x10")
                chosenBox.append("x15")
                chosenBox.append("x25")
                chosenBox.append("x45")    
            print("x5 appear " + str(isX5OccurAlot()) + " times in a row")

        if isX50notAppear() > 3:
            for i in range(3, isX50notAppear()+1):
                chosenBox.append("x5")

        sortedCollection = list(boxCollection.find({}).sort("time",-1))
        for type in types:
            basePercent = round(boxCollection.count_documents({"type": type})/totalCount * 100, 3)
            curPos = sortedCollection.index(next(i for i in sortedCollection if i["type"]==type)) + 1
            baseOccur = 100 / basePercent
            occurDiff = curPos - baseOccur
            distanceDiffPecent = round(occurDiff/baseOccur * 100, 3)
            print("baseOccur: " + str(baseOccur) + " curPos: " + str(curPos) + " occurDiff:" + str(occurDiff) + " occurDiffPecent:" + str(distanceDiffPecent) )
            if distanceDiffPecent > breakPoints[type] and len(chosenBox) < 4:
                percentTimes = round(distanceDiffPecent / breakPoints[type])
                print("Percent Times:" + str(percentTimes))
                for i in range(0, percentTimes):
                    chosenBox.append(type)
        if len(chosenBox) <= 1:
            chosenBox.append("x5")
        print("Current Round: " + str(curRound))
        for box in chosenBox:
            print(box)
        for box in chosenBox:
            if "x5" in box:
                try:
                    box1.click()
                    time.sleep(0.5)
                    box2.click()
                    time.sleep(0.5)
                    box3.click()
                    time.sleep(0.5)
                    box4.click()
                    time.sleep(0.5)
                    print("Box 1,2,3,4 Clicked")
                except:
                    continue
            if "x10" in box:
                try:
                    box5.click()
                    time.sleep(0.5)
                    print("Box 5 Clicked")
                except:
                    continue
            if "x15" in box:
                try:
                    box6.click()
                    time.sleep(0.5)
                    print("Box 6 Clicked")
                except:
                    continue
            if "x25" in box:
                try:
                    box7.click()
                    time.sleep(0.5)
                    print("Box 7 Clicked")
                except:
                    continue
            if "x45" in box:
                try:
                    box8.click()
                    time.sleep(0.5)
                    print("Box 8 Clicked")
                except:
                    continue
        isbet = curRound
        time.sleep(15)
    else:
        continue
    
    