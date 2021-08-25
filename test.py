import pymongo
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date, datetime
import time

CONNECTION_STRING = "mongodb+srv://Ryan:trantran2312@cluster0.pwc6h.mongodb.net/NimoLottery?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client["NimoLottery"]
calculationCollection = db["BeanAnalyst"]
boxCollection = db["BeanBoxesv2"]


boxes = list(boxCollection.find({}).sort("time", -1))
box = list(calculationCollection.find({}).sort("time", -1).limit(1))

def minMaxAppear(minOrMax, inputBox):
    allBoxes = boxCollection.find({})
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

def minBox(inputBox):
    allBoxes = boxCollection.find({}).sort("time", -1)
    result = 0
    count = 0
    for box in allBoxes:
        if box["box"] != inputBox:
            count += 1
            if count > result:
                result = count
        else:
            count = 0
    return result

def maxBox(inputBox):
    allBoxes = boxCollection.find({}).sort("time", -1)
    result = 0
    count = 0
    for box in allBoxes:
        if box["box"] == inputBox:
            count += 1
            if count > result:
                result = count
        else:
            count = 0
    return result

print("Min box 1: " + str(minMaxAppear("min", "box1")) + " - Max box 1: " + str(minMaxAppear("max", "box1")))

print("Min box 1: " + str(minBox("box1")) + " - Max box 1: " + str(maxBox("box1")))
# max = 0
# count = 0
# times = 0
# for box in boxes:
#     if box["type"] != "x5":
#         count += 1
#         if(count > max):
#             max = count
#             print("cur Max: " + str(max) +" Round: " + box["round"] + " Time: " + str(box["time"]))
#     else:
#         if count > 2:
#             times += 1
#         count = 0

# print("Min x5: " + str(max) + " Happen: " + str(times))
# for box in boxes:
#     if int(box["round"]) > 704 and int(box["round"]) < 739 :

#         print("Round: " + box["round"] + " Type:" + box["type"] + " Time: " + str(box["time"]))