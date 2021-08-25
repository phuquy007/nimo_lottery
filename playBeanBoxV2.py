import pymongo
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
from readFile import readFile

# Connect to Mongo
CONNECTION_STRING = "mongodb+srv://Ryan:trantran2312@cluster0.pwc6h.mongodb.net/NimoLottery?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client["NimoLottery"]
calculationCollection = db["BeanAnalyst"]
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

BOXES = ["box1", "box2", "box3", "box4", "box5", "box6", "box7", "box8"]

# Return the current Round
def GetCurRound():
    return driver.find_element_by_xpath("//*[@id='container']/div/div[2]/div[2]/div/em").text

# Return the lasted Round in logs
def GetLastestLogRound():
    return list(boxCollection.find({}).sort("time",-1).limit(1))[0]["round"]


# Check these case to choose the box to play
# 1 - If the second row appear for more than 3 times in row, play the 1st row until win
# 2 - If the 1st row appear for more than 15 times in row, play the 2nd row until win




def Play(chosenBox):
    for box in chosenBox:
        print(box)
    for box in chosenBox:
        if "box1" in box:
            try:
                box1.click()
                time.sleep(0.5)
                print("Box 1 Clicked")
            except:
                continue
    
    

isbet = -1
while(True):
    driver.refresh()
    time.sleep(5)
    curRound = GetCurRound()
    logRound = GetLastestLogRound()
    
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
        except:
            continue
        chosenBox = []
        # Add box to play
        print("Current Round: " + str(curRound))
        #
        isbet = curRound
        # time.sleep(5)
    else:
        continue
    
    