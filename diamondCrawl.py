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
boxCollection = db["DiamondBoxes"]

url = 'https://www.nimo.tv/mkt/act/super/box_lottery'
driver.get(url)
time.sleep(2)

PRIZE = "prize-box"
NOPRIZE = "no-prize-box"

# Return the current Round
def GetCurRound():
    return driver.find_element_by_xpath("//*[@id='container']/div/div[2]/div[2]/div/em").text

# Return the lasted Round in logs
def GetLastestLogRound():
    return list(boxCollection.find({}).sort("time",-1).limit(1))[0]["round"]

def pushToMongo(box):
    boxCollection.insert_one(box)

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
       
        time.sleep(5)
    

