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
boxCollection = db["BeanBoxes"]


boxes = list(boxCollection.find({}).sort("time", 1))

calculationCollection.delete_many({})

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