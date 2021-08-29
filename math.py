from helper import WriteLog
# def calculateKeys(betAmt):
#     key5k = betAmt // 5000
#     betAmt = betAmt % 5000
#     key1k = betAmt // 1000
#     betAmt = betAmt % 1000
#     key500 = betAmt // 500
#     betAmt = betAmt % 500
#     key50 = betAmt // 50
#     return {"key5k": key5k, "key1k": key1k, "key500": key500, "key50": key50}


# result = calculateKeys(37650)
# for times in range(0, result["key5k"]):
#     print(f'Click {times}')
 
# if result["key5k"] > 0:
#     print("> 0 ")

from datetime import datetime


def changeText(input):
    input[0] = False

try:
    avb = "You:216540"
    result = avb / 3
except Exception as error:
    # print(error)
    WriteLog(error, "test")

