import pymongo
from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://Ryan:trantran2312@cluster0.pwc6h.mongodb.net/NimoLottery?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client["NimoLottery"]
boxCollection = db["Boxes"]

totalCount = boxCollection.count_documents({})

box5 = boxCollection.find({"type": "x5"})
box5Count = boxCollection.count_documents({"type": "x5"})
box5BasePercentage = box5Count / totalCount

box10 = boxCollection.find({"type": "x10"})
box10Count = boxCollection.count_documents({"type": "x10"})
box10BasePercentage = box10Count / totalCount

box15 = boxCollection.find({"type": "x15"})
box15Count = boxCollection.count_documents({"type": "x15"})
box15BasePercentage = box15Count / totalCount

box25 = boxCollection.find({"type": "x25"})
box25Count = boxCollection.count_documents({"type": "x25"})
box25BasePercentage = box25Count / totalCount

box45 = boxCollection.find({"type": "x45"})
box45Count = boxCollection.count_documents({"type": "x45"})
box45BasePercentage = box45Count / totalCount

print("Total Count: " + str(totalCount))
print("Box 5 - Count: " + str(box5Count) + ", Base-Percentage: " + str(round(box5BasePercentage,3)))
print("Box 10 - Count: " + str(box10Count) + ", Base-Percentage: " + str(round(box10BasePercentage,3)))
print("Box 15 - Count: " + str(box15Count) + ", Base-Percentage: " + str(round(box15BasePercentage,3)))
print("Box 25 - Count: " + str(box25Count) + ", Base-Percentage: " + str(round(box25BasePercentage,3)))
print("Box 45 - Count: " + str(box45Count) + ", Base-Percentage: " + str(round(box45BasePercentage,3)))

#Get the newest 100
newestCollection = boxCollection.find().limit(100).sort({"time": 1})
for item in newestCollection:
    print(item.round + " - " + item.time)