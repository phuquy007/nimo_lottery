from os import getcwd
import pymongo
from pymongo import MongoClient
from pymongo import message
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
calculationCollection = db["DiamondAnalyst"]
boxCollection = db["DiamondBoxes"]
Emulator = db["DiamondGameEmulation"]
BetHistory = db["DiamondBetHistory"]

def CalculateBetResult(round):
    try:
        round -= 1
        myDiamondID = "quytran"
        myDiamond = int(Emulator.find_one({"id": myDiamondID})["diamond"])
        myBet = list(BetHistory.find({"round": int(round)}).sort("time", -1))[0]
        result = list(boxCollection.find({"round": str(round)}).sort("time", -1))[0]

        if(myBet["time"].date() == result["time"].date() == datetime.today().date()):
            # print("Checking Win")
            win = "not win"
            winBet = 0
            totalBetDiamond = 0
            for box, betAmt in myBet["bets"].items():
                if(result["box"] == box):
                    win = box
                    winBet = betAmt
                totalBetDiamond += betAmt

            if win != "not win":
                print(f'Round: {round} Winning Box: {result["box"]} - selected Box: {myBet["bets"]} ---> Win')
                print("")
                print("----------------------------------------------------------------")
                print("")
                return "win"
            else:
                myDiamond = myDiamond - int(totalBetDiamond)
                print(f'Round: {round} Winning Box: {result["box"]} - selected Box: {myBet["bets"]} ---> Lose')
                print("")
                print("----------------------------------------------------------------")
                print("")
                return "lose"

        else:
            print(f'Round {round} is not bet')
            print("")
            print("----------------------------------------------------------------")
            print("")
    except Exception as error:
        # print(error)
        print(f'Round {round} is not bet')
        print("")
        print("----------------------------------------------------------------")
        print("")