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

print(box[0])

def minBox(inputBox):
    allBoxes = boxCollection.find({}).sort("time", 1)
    result = 0
    count = 0
    times = 0
    for box in allBoxes:
        if box["box"] != inputBox:
            count += 1
            if count > result:
                result = count
                print("Min : " + str(result) + " - Round: " + box["round"])
        else:
            if count > 40:
                times += 1
            count = 0
    print(times)
    return result

def max1stRow():
    allBoxes = boxCollection.find({}).sort("time", 1)
    result = 0
    count = 0 
    time = 0
    for box in allBoxes:
        if box["box"] == "box1" or box["box"] == "box2" or box["box"] == "box3" or box["box"] == "box4":
            count += 1
            if count > result:
                result = count
        else:
            if count > 50:
                time += 1
            count = 0
    print(time)
    return result

def max2ndRow():
    allBoxes = boxCollection.find({}).sort("time", 1)
    result = 0
    count = 0 
    time = 0
    for box in allBoxes:
        if box["box"] == "box5" or box["box"] == "box6" or box["box"] == "box7" or box["box"] == "box8":
            count += 1
            if count > result:
                result = count
        else:
            if count > 2:
                time += 1
            count = 0
    print(time)
    return result

print(minBox("box6"))
# print(minBox("box2"))

# for box in boxes:
#     if int(box["round"]) > 1711 and int(box["round"]) < 1755:
#         print("Round: " + box["round"] + " - Box: " + box["box"])

# def maxBox(inputBox):
#     allBoxes = boxCollection.find({}).sort("time", -1)
#     result = 0
#     count = 0
#     for box in allBoxes:
#         if box["box"] == inputBox:
#             count += 1
#             if count > result:
#                 result = count
#         else:
#             count = 0
#     return result


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