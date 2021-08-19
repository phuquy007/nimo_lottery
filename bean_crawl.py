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
boxCollection = db["BeanBoxes"]

url = 'https://www.nimo.tv/mkt/act/super/bean_box_lottery'
driver.get(url)
time.sleep(3)

prize = "prize-box"
noPrize = "no-prize-box"

def pushToMongo(box):
    boxCollection.insert_one(box)
    
def printBox(box):
    print("Round: " + box["round"] + " Type: " + box["type"])

while(True):
    driver.refresh()
    time.sleep(2)
    curRound = driver.find_element_by_xpath("//*[@id='container']/div/div[2]/div[2]/div/em").text
    previousRound = boxCollection.find({}).sort("time",-1).limit(1)["round"]
    if(curRound != previousRound):
        boxes = driver.find_elements_by_xpath("//*[@id='container']/div/div[3]//picture/img")
        imgs = [el.get_attribute("src") for el in boxes]
        lastImg = imgs[0]
        type = "";
        if "box0" in lastImg:
            type = "x5"
        if "box4" in lastImg:
            type = "x10"
        if "box5" in lastImg:
            type = "x15"
        if "box6" in lastImg:
            type = "x25"
        if "box7" in lastImg:
            type = "x45"
        newBox = {"round": curRound, "type": type, "time": datetime.now()}
        pushToMongo(newBox)
        printBox(newBox)
    else: 
        continue
    

