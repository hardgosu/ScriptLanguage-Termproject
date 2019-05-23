#https://api.neople.co.kr/df/items?itemName=<itemName>&q=minLevel:<minLevel>,maxLevel:<maxLevel>,rarity:<rarity>,trade:<trade>&limit=<limit>&wordType=<wordType>&apikey=ppMk2pUeHbk6Wi0dazKt7YM4PvkTnzDB
import webbrowser
import urllib.request
import urllib.parse

import json
import os
from tkinter import *
from tkinter.ttk import *

from tkinter.font import *
import http.client

#JSON 파일을 딕셔너리로 파싱하기

class DNFAPIProcess:

    def GetItemInfoFromMarket(self,itemName):

        if (itemName == ""):
            print("비어있는입력")
            return

        #파싱 ..
        itemName = urllib.parse.quote(itemName)

        server = "api.neople.co.kr"  # 물음표까지 다써도됌


        conn = http.client.HTTPSConnection(server)

        conn.request("GET","/df/items?itemName=" +itemName +  "&q=minLevel:<minLevel>,maxLevel:<maxLevel>,rarity:<rarity>,trade:<trade>&limit=<limit>&wordType=<wordType>&apikey=ppMk2pUeHbk6Wi0dazKt7YM4PvkTnzDB")

        response = conn.getresponse()
        cLen = response.getheader("Content-Length")  # 헤더에서 Content-Length 즉 얼만큼 읽었는지 추출
        result = response.read(int(cLen)).decode('utf-8')

        jsonData = ParsingDataOfItems(result) #파싱한 JSON 데이터를 요소별로 객체에 저장ㅇ한 클래스


        if len(jsonData.jsonData["rows"]) == 0:
            return  #파싱한 데이터가 하나도 없으면 반환한다


	#이미지 파일 얻어오는코드
        url = "https://img-api.neople.co.kr/df/items/" + jsonData.itemID
        outpath = "images/"
        outfile = "image_" +jsonData.itemName + ".png"

        if not os.path.isdir(outpath):
            os.makedirs(outpath)

        urllib.request.urlretrieve(url, outpath + outfile)
	#여기까지

        print(jsonData)
        webbrowser.open_new(url)

        pass




class ParsingDataOfItems:
    def __init__(self,JSON):
        self.jsonData = json.loads(JSON) #string 형태의 JSON 객체를 딕셔너리로 바꾼다


        if len(self.jsonData["rows"]) == 0:
            return

        self.itemID = self.jsonData["rows"][0]["itemId"]
        self.itemName = self.jsonData["rows"][0]["itemName"]
        self.itemRarity = self.jsonData["rows"][0]["itemRarity"]
        self.itemType = self.jsonData["rows"][0]["itemType"]
        self.itemDetail = str(self.jsonData["rows"][0]["itemTypeDetail"])
        self.itemAvailableLevel = str(self.jsonData["rows"][0]["itemAvailableLevel"])

    def __str__(self):
        if len(self.jsonData["rows"]) == 0:
            return ""
        return " [아이템 고유코드 : " + self.itemID + "]\n [아이템이름 : " + self.itemName + "]\n [아이템 레어도 : " + self.itemRarity + "]\n [아이템 타입 : " + self.itemType + "]\n [아이템 타입상세 : " + self.itemDetail + "]\n [아이템 착용레벨 : " + self.itemAvailableLevel + "]\n"


DNFAPIProcess().GetItemInfoFromMarket("흑천의 주인 - 대검")