import json




with open("data.json") as file:
    print(type(file))
    data = json.load(file)
    print(type(data))
    print(data)
    #loads 를 스면 문자열을 dict로.