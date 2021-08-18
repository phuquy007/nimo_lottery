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
boxCollection = db["BoxesByType"]

# Selenium load the website
chrome_options = Options()
# chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=10x10")  
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:\chromedriver\chromedriver.exe")
url = 'https://www.nimo.tv/mkt/act/super/bean_box_lottery'
driver.get(url)
time.sleep(30)

box1 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[1]")
box2 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[2]")
box3 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[3]")
box4 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[4]")
box5 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[5]")
box6 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[6]")
box7 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[7]")
box8 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[8]")

totalCount = boxCollection.count_documents({})

types = ["x5", "x10", "x15", "x25", "x45"]
breakPoints = {"x5": 200, "x10": 150, "x15": 100, "x25": 80, "x45": 50}

baseBoxes = []
for type in types:
    baseBoxes.append({"type": type, "percentage": round(boxCollection.count_documents({"type": type})/totalCount * 100, 3)})

# print("Total Count: " + str(totalCount))
# for box in baseBoxes:
#     print("Box Type: " + box["type"] + " - Percentage: " + str(round(box["percentage"], 2)))

def isX5OccurAlot():
    x5LastestBoxes = list(boxCollection.find().sort("time",-1).limit(8))
    for box in x5LastestBoxes:
        if box["type"] != "x5":
            return False
    return True

while(True):
    chosenBox = []
    if isX5OccurAlot():
        chosenBox.append("x10")
        chosenBox.append("x15")
        chosenBox.append("x25")
        chosenBox.append("x45")
#else if if 2 or more 2nd row have the distanceDiffPercent > 30%, add these box to the chosenBoxes
    else:
        sortedCollection = list(boxCollection.find({}).sort("time",-1))
        for type in types:
            curPos = sortedCollection.index(next(i for i in sortedCollection if i["type"]==type)) + 1
            basePercent = next((x for x in baseBoxes if x["type"] == type), None)["percentage"]
            baseOccur = 100 / basePercent
            occurDiff = curPos - baseOccur
            distanceDiffPecent = round(occurDiff/baseOccur * 100, 3)
            print("baseOccur: " + str(baseOccur) + " curPos: " + str(curPos) + " occurDiff:" + str(occurDiff) + " occurDiffPecent:" + str(distanceDiffPecent) )
            if distanceDiffPecent > breakPoints[type]:
                chosenBox.append(type)
    if len(chosenBox) <= 1:
        chosenBox.append("x5")
    for box in chosenBox:
        if box == "x5":
            box1.click()
            box2.click()
            box3.click()
            box4.click()
            print("Box 1,2,3,4 CLicked")
        if box == "x10":
            box5.click()
            print("Box 5 CLicked")
        if box == "x15":
            box6.click()
            print("Box 6 CLicked")
        if box == "x25":
            box7.click()
            print("Box 7 CLicked")
        if box == "x45":
            box8.click()
            print("Box 8 CLicked")
    time.sleep(35)
    # driver.refresh()
    time.sleep(5)