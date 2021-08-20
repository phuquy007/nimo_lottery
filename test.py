import pymongo
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time

CONNECTION_STRING = "mongodb+srv://Ryan:trantran2312@cluster0.pwc6h.mongodb.net/NimoLottery?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client["NimoLottery"]
calculationCollection = db["BeanAnalyst"]
boxCollection = db["BeanBoxesv2"]

print(list(boxCollection.find({"round": "599"})))