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
time.sleep(30)



totalCount = boxCollection.count_documents({})

types = ["x5", "x10", "x15", "x25", "x45"]
breakPoints = {"x5": 200, "x10": 100, "x15": 90, "x25": 80, "x45": 60}

# baseBoxes = []
# for type in types:
#     baseBoxes.append({"type": type, "percentage": round(boxCollection.count_documents({"type": type})/totalCount * 100, 3)})

# print("Total Count: " + str(totalCount))
# for box in baseBoxes:
#     print("Box Type: " + box["type"] + " - Percentage: " + str(round(box["percentage"], 2)))

# 8 times x1 box
# 9 times x1 box
# 10 times x2 box
# 11 times x4 box
# 12 times x8 box

def isX5OccurAlot():
    x5Count = 0
    x5LastestBoxes = list(boxCollection.find().sort("time",-1).limit(12))
    for x5Box in x5LastestBoxes:
        if x5Box["type"] == "x5":
            x5Count += 1
        else:
            return x5Count
    return x5Count

# count how many times x5 appear in a row
while(True):
    driver.refresh()
    time.sleep(1)
    box1 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[1]")
    box2 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[2]")
    box3 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[3]")
    box4 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[4]")
    box5 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[5]")
    box6 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[6]")
    box7 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[7]")
    box8 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[8]")
    chosenBox = []
    if isX5OccurAlot() > 7:
        chosenBox.append("x10")
        chosenBox.append("x15")
        chosenBox.append("x25")
        chosenBox.append("x45")
        print("x5 appear " + str(isX5OccurAlot()) + " times in a row")
#else if if 2 or more 2nd row have the distanceDiffPercent > 30%, add these box to the chosenBoxes
    sortedCollection = list(boxCollection.find({}).sort("time",-1))
    for type in types:
        basePercent = round(boxCollection.count_documents({"type": type})/totalCount * 100, 3)
        curPos = sortedCollection.index(next(i for i in sortedCollection if i["type"]==type)) + 1
        baseOccur = 100 / basePercent
        occurDiff = curPos - baseOccur
        distanceDiffPecent = round(occurDiff/baseOccur * 100, 3)
        print("baseOccur: " + str(baseOccur) + " curPos: " + str(curPos) + " occurDiff:" + str(occurDiff) + " occurDiffPecent:" + str(distanceDiffPecent) )
        if distanceDiffPecent > breakPoints[type]:
            chosenBox.append(type)
    if len(chosenBox) <= 1:
        chosenBox.append("x5")
    for box in chosenBox:
        print(box)
    for box in chosenBox:
        if "x5" in box:
            try:
                box1.click()
                time.sleep(0.1)
                box2.click()
                time.sleep(0.1)
                box3.click()
                time.sleep(0.1)
                box4.click()
                time.sleep(0.1)
                print("Box 1,2,3,4 Clicked")
            except:
                continue
        if "x10" in box:
            try:
                box5.click()
                time.sleep(0.1)
                print("Box 5 Clicked")
            except:
                continue
        if "x15" in box:
            try:
                box6.click()
                time.sleep(0.1)
                print("Box 6 Clicked")
            except:
                continue
        if "x25" in box:
            try:
                box7.click()
                time.sleep(0.1)
                print("Box 7 Clicked")
            except:
                continue
        if "x45" in box:
            try:
                box8.click()
                time.sleep(0.1)
                print("Box 8 Clicked")
            except:
                continue
    time.sleep(38.5)
    
    