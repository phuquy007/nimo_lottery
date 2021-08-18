# testList = [{"type":"x10", "value": 10},{"type":"x5", "value": 5},{"type":"x35", "value": 35},{"type":"x15", "value": 15},{"type":"x5", "value": 5},{"type":"x25", "value": 25}]

# result = testList.index(next(x for x in testList if x["type"] == "x15"))
# print(result)

types = ["x5", "x10", "x15", "x25", "x45"]
breakpoints = {"x5": 200, "x10": 150, "x15": 100, "x25": 80, "x45": 50}

for type in types:
    print(breakpoints[type])