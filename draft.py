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
boxCollection = db["Boxes"]

url = 'https://www.nimo.tv/mkt/act/super/box_lottery'
driver.get(url)
time.sleep(3)

prize = "prize-box"
noPrize = "no-prize-box"

def pushToMongo(box):
    boxCollection.insert_one(box)

def printBox(box):
    print("Round: " + box.round + " Type: " + box.type)


while(True):
    try:
        round = driver.find_element_by_xpath("//*[@id='container']/div/div[2]/div[2]/div/em").text
        box1 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[1]").get_attribute("class")
        box2 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[2]").get_attribute("class")
        box3 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[3]").get_attribute("class")
        box4 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[4]").get_attribute("class")
        box5 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[5]").get_attribute("class")
        box6 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[6]").get_attribute("class")
        box7 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[7]").get_attribute("class")
        box8 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[8]").get_attribute("class")

        if prize in box1 and noPrize not in box1:
            newBox = {"round": round, "type": "box1", "time": datetime.now()}
            pushToMongo(newBox)
            printBox(newBox)
        if prize in box2 and noPrize not in box2:
            newBox = {"round": round, "type": "box2", "time": datetime.now()}
            pushToMongo(newBox)
            printBox(newBox)
        if prize in box3 and noPrize not in box3:
            newBox = {"round": round, "type": "box3", "time": datetime.now()}
            pushToMongo(newBox)
            printBox(newBox)
        if prize in box4 and noPrize not in box4:
            newBox = {"round": round, "type": "box4", "time": datetime.now()}
            pushToMongo(newBox)
            printBox(newBox)
        if prize in box5 and noPrize not in box5:
            newBox = {"round": round, "type": "box5", "time": datetime.now()}
            pushToMongo(newBox)
            printBox(newBox)
        if prize in box6 and noPrize not in box6:
            newBox = {"round": round, "type": "box6", "time": datetime.now()}
            pushToMongo(newBox)
            printBox(newBox)
        if prize in box7 and noPrize not in box7:
            newBox = {"round": round, "type": "box7", "time": datetime.now()}
            pushToMongo(newBox)
            printBox(newBox)
        if prize in box8 and noPrize not in box8:
            newBox = {"round": round, "type": "box8", "time": datetime.now()}
            pushToMongo(newBox)
            printBox(newBox)
    except Exception as e:
        continue
    
#get all the data for every 45s
#then save all the data to the database - maybe use mongoDB
#calculate the percentage of everybox