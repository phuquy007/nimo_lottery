from typing import Counter
from playBeanBoxV2 import GetCurRound
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pymongo
from pymongo import MongoClient
from datetime import datetime

# chrome_options = Options()

# chrome_options.add_argument("--window-size=10x10")  
# driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:\chromedriver\chromedriver.exe")

CONNECTION_STRING = "mongodb+srv://Ryan:trantran2312@cluster0.pwc6h.mongodb.net/NimoLottery?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client["NimoLottery"]
calculationCollection = db["BeanCalculation"]
boxCollection = db["BeanBoxesv2"]

# url = 'https://www.nimo.tv/mkt/act/super/bean_box_lottery'
# driver.get(url)
# time.sleep(3)

PRIZE = "prize-box"
NOPRIZE = "no-prize-box"
BOXES = ["box1", "box2", "box3", "box4", "box5", "box6", "box7", "box8"]

# Return the current Round
# def GetCurRound():
#     return driver.find_element_by_xpath("//*[@id='container']/div/div[2]/div[2]/div/em").text

# Return the lasted Round in logs
def GetLastestLogRound():
    return list(boxCollection.find({}).sort("time",-1).limit(1))[0]["round"]

def pushToMongo(box):
    boxCollection.insert_one(box)
    
def printBox(box):
    print("Round: " + box["round"] + " Type: " + box["type"])

def pushCalculation():
    totalCount = boxCollection.count_documents({})
    # newCalculation = {GetLastestLogRound() : {

    # }}
    List100 = boxCollection.find({}).sort("time", -1).limit(100)
    for box in BOXES:
        basePercentage = round(boxCollection.count_documents({"box": box})/totalCount * 100, 3)
        print(box + " - " +str(basePercentage))
        # curPercentage = 0
        # for item in List100:
        #     if item["box"] == box:
        #         curPercentage += 1
        # print(curPercentage)

pushCalculation()
# round = None
# while(True):
#     # driver.refresh()
#     # time.sleep(0.1)
#     curRound = driver.find_element_by_xpath("//*[@id='container']/div/div[2]/div[2]/div/em").text
#     prizebox = None
#     boxes = []
#     try:
#         for i in range(1, 9):
#             box = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div["+str(i)+"]")
#             if PRIZE in box.get_attribute("class")and NOPRIZE not in box.get_attribute("class"):
#                 if not prizebox:
#                     prizebox = "box" + str(i)
#     except: 
#         continue
#     if prizebox and round != curRound:
#         round = curRound
#         newBox = {"round": round, "box": prizebox, "time": datetime.now()}
#         pushToMongo(newBox)
#         print("Round: " + round +" - box: " + str(prizebox))
#         time.sleep(5)