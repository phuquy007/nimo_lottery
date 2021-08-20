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
boxCollection = db["BeanBoxesv2"]

# Selenium load the website
chrome_options = Options()
# chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=800x600")  
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:\chromedriver\chromedriver.exe")
url = 'https://www.nimo.tv/mkt/act/super/bean_box_lottery'
driver.get(url)
time.sleep(2)

totalCount = boxCollection.count_documents({})

boxes = ["box1", "box2", "box3", "box4", "box5", "box6", "box7", "box8"]
breakPoints = {"box1": 100, "box2": 100, "box3": 100, "box4": 100, "box5": 80, "box6": 60, "box7": 40, "box8":20}

# Return the current Round
def GetCurRound():
    return driver.find_element_by_xpath("//*[@id='container']/div/div[2]/div[2]/div/em").text

# Return the lasted Round in logs
def GetLastestLogRound():
    return list(boxCollection.find({}).sort("time",-1).limit(1))[0]["round"]

# Return the number of times a box not appear
def BoxNotAppear(box):
    lastestBoxAppear = list(boxCollection.find({"box": box}).sort("time", -1).limit(1))
    return int(GetCurRound()) - int(lastestBoxAppear[0]["round"]) -1

# Return the number of times box x5 not appear
# ex: history = x10 x15 x25 x5 => return 3
def BoxX5NotAppear():
    counter = 0
    lastestBoxes = list(boxCollection.find().sort("time",-1).limit(10))
    for box in lastestBoxes:
        if box["box"] != "box1" and box["box"] != "box2" and box["box"] != "box3" and box["box"] != "box4":
            counter += 1
        else:
            return counter
    return counter

# Return the number of times a box appear in row
def BoxAppearInRow(input):
    counter = 0
    lastestBoxes = list(boxCollection.find().sort("time",-1).limit(30))
    for box in lastestBoxes:
        if box["box"] == input:
            counter += 1
        else:
            return counter
    return counter


# count how many times x5 appear in a row
# while(True):
#     driver.refresh()
#     time.sleep(5)
#     curRound = driver.find_element_by_xpath("//*[@id='container']/div/div[2]/div[2]/div/em").text
#     logRound = list(boxCollection.find({}).sort("time",-1).limit(1))[0]["round"]
    
#     if(curRound == logRound and curRound != isbet):
#         try:
#             box1 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[1]")
#             box2 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[2]")
#             box3 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[3]")
#             box4 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[4]")
#             box5 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[5]")
#             box6 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[6]")
#             box7 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[7]")
#             box8 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[8]")

#             # x500Key = driver.find_element_by_xpath("//*[@id='container']/div/div[5]/div[2]/div[2]")
#             # x500Key.click()
#         except:
#             continue
#         chosenBox = []
#         if isX5OccurAlot() >= 13:
#             for i in range (13, isX5OccurAlot()+1):
#                 for i in range(2):
#                     chosenBox.append("x10")
#                     chosenBox.append("x15")
#                     chosenBox.append("x25")
#                     chosenBox.append("x45")    
#             print("x5 appear " + str(isX5OccurAlot()) + " times in a row")

#         if isX50notAppear() >= 5:
#             for i in range(40):
#                 chosenBox.append("x5")
#         if isX50notAppear() == 4:
#             for i in range(20):
#                 chosenBox.append("x5")
#         if isX50notAppear() == 3:
#             for i in range(10):
#                 chosenBox.append("x5")

#         # if isX50notAppear() > 3:
#         #     for i in range(3, isX50notAppear()+1):
#         #         chosenBox.append("x5")

#         sortedCollection = list(boxCollection.find({}).sort("time",-1))
#         for type in types:
#             basePercent = round(boxCollection.count_documents({"type": type})/totalCount * 100, 3)
#             curPos = sortedCollection.index(next(i for i in sortedCollection if i["type"]==type)) + 1
#             baseOccur = 100 / basePercent
#             occurDiff = curPos - baseOccur
#             distanceDiffPecent = round(occurDiff/baseOccur * 100, 3)
#             print("baseOccur: " + str(baseOccur) + " curPos: " + str(curPos) + " occurDiff:" + str(occurDiff) + " occurDiffPecent:" + str(distanceDiffPecent) )
#             # if distanceDiffPecent > breakPoints[type] and len(chosenBox) < 4:
#             #     percentTimes = round(distanceDiffPecent / breakPoints[type])
#             #     print("Percent Times:" + str(percentTimes))
#             #     for i in range(0, percentTimes):
#             #         chosenBox.append(type)
#         # if len(chosenBox) <= 1:
#         #     chosenBox.append("x5")
#         print("Current Round: " + str(curRound))
#         for box in chosenBox:
#             print(box)
#         for box in chosenBox:
#             if "x5" in box:
#                 try:
#                     box1.click()
#                     time.sleep(0.5)
#                     box2.click()
#                     time.sleep(0.5)
#                     box3.click()
#                     time.sleep(0.5)
#                     box4.click()
#                     time.sleep(0.5)
#                     print("Box 1,2,3,4 Clicked")
#                 except:
#                     continue
#             if "x10" in box:
#                 try:
#                     box5.click()
#                     time.sleep(0.5)
#                     print("Box 5 Clicked")
#                 except:
#                     continue
#             if "x15" in box:
#                 try:
#                     box6.click()
#                     time.sleep(0.5)
#                     print("Box 6 Clicked")
#                 except:
#                     continue
#             if "x25" in box:
#                 try:
#                     box7.click()
#                     time.sleep(0.5)
#                     print("Box 7 Clicked")
#                 except:
#                     continue
#             if "x45" in box:
#                 try:
#                     box8.click()
#                     time.sleep(0.5)
#                     print("Box 8 Clicked")
#                 except:
#                     continue
#         isbet = curRound
#         # time.sleep(5)
#     else:
#         continue
    
    