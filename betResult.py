from os import getcwd
import pymongo
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
from readFile import readFile
from enum import Enum

# Connect to Mongo
CONNECTION_STRING = "mongodb+srv://Ryan:trantran2312@cluster0.pwc6h.mongodb.net/NimoLottery?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client["NimoLottery"]
calculationCollection = db["BeanAnalyst"]
boxCollection = db["BeanBoxesv2"]
Emulator = db["GameEmulation"]
BetHistory = db["BetHistory"]


def CalculateBetResult(round):
    try:
        myDiamondID = "61273cb918a0e1938dd359ab"
        myDiamond = Emulator.find_one({"_id": myDiamondID})
        myBet = list(BetHistory.find({"round": round}).sort("time", -1).limit(1))[0]
        result = list(boxCollection.find({}).sort("time", -1).limit(1))[0]

        if myBet["round"] == result["round"]:
            win = "not win"
            winBet = 0
            totalBetDiamond = 0
            print(f'Round: {myBet["Round"]}')
            for box, betAmt in myBet["bets"].items():
                if(result["box"] == box):
                    win = box
                    winBet = betAmt
                    print(f'Box: {box} - Bet: {betAmt} -------- WIN')
                print(f'Box: {box} - Bet: {betAmt}')
                totalBetDiamond += betAmt
            print(f'Total Bet: {totalBetDiamond}')

            if win != "not win":
                if win == "box1" or win == "box2" or win == "box3" or win == "box4":
                    winBet = winBet * 5
                elif win == "box5":
                    winBet = winBet * 10
                elif win == "box6":
                    winBet = winBet * 15
                elif win == "box7":
                    winBet = winBet * 25
                elif win == "box8":
                    winBet = winBet * 45
                myDiamond += winBet
            else:
                myDiamond -= totalBetDiamond

            document = {"round": myBet["Round"], "bets": myBet["bets"], "result": win, "my diamond": myDiamond}
            Emulator.insert_one(document)

            return "success"
        else:
            return "fail"
    except:
        print("Not Bet yet!")


