# -*- coding: utf-8 -*-
#https://api.neople.co.kr/df/servers?apikey=fS1DhnBRYjp0EIzzj2pMONApSNSkhOYV
#캐릭터 이미지 URL : https://img-api.neople.co.kr/df/servers/<serverId>/characters/<characterId>?zoom=<zoom>
import urllib.request
import urllib.parse
import json
import os
from tkinter import *
import tkinter.ttk as ttk

from tkinter.font import *
import http.client

## 송민수 코드 추가, 19.06.16 ##
import LOL_Mainframe
import Animator
import math
##############################

_WINDOW_WIDTH = 1280
_WINDOW_HEIGHT = 800
_FRAME_WIDTH = 1230
_FRAME_HEIGHT = 750


class MainWindow:
    global _WINDOW_HEIGHT, _WINDOW_WIDTH, _FRAME_HEIGHT, _FRAME_WIDTH
    def __init__(self):
        self.window = Tk()
        self.window.resizable(False, False)
        self.frame = 1.0
        self.count = 1

        # 중앙 배치를 위한 오프셋 계산
        _WINDOW_OFFSET_X = int(self.window.winfo_screenwidth()/2 - _WINDOW_WIDTH/2)
        _WINDOW_OFFSET_Y = int(self.window.winfo_screenheight()/2 - _WINDOW_HEIGHT/2)
        # 스크린 중앙 배치
        setGeometry = "{0}x{1}+{2}+{3}".format(_WINDOW_WIDTH, _WINDOW_HEIGHT, _WINDOW_OFFSET_X, _WINDOW_OFFSET_Y)
        self.window.geometry(setGeometry)
        self.window.wm_iconbitmap('DNF.ico')
        self.window.title("useful")

        # 밑배경 애니메이션을 위한 캔버스
        self.canvas = Canvas(self.window, bg="gray1", width = _WINDOW_WIDTH, height = _WINDOW_HEIGHT, bd = 0)
        self.canvas.place(x = 0, y = 0)
        self.canvas.after(0, self.frameAnimation)

        self.notebook = ttk.Notebook(self.window, width = _FRAME_WIDTH, height = _FRAME_HEIGHT, padding = 0)
        self.notebook.pack()

    def frameAnimation(self):
        animSpeed = 1
        self.frame += 0.016 * animSpeed
        value = (math.sin(self.frame * 2 * 3.141592) + 1.0) * 0.5 * 99

        self.count = int(value)
        setBackground = "gray" + str(self.count)
        self.canvas.configure(bg=setBackground)
        self.canvas.after(16, self.frameAnimation)

class Interface:
    def __init__(self,window):
        #self.window = window
        pass
    def Run(self):
        print("Interface")
        pass
    def Show(self):
        pass
    pass

class ButtonFunction:
    def __init__(self,itemID,process):
        self.itemID = itemID
        self.jsonData = None
        self.process = process
        pass
    def GetItemDetailInfoFromDatabase(self):
        if (self.itemID == ""):
            print("비어있는입력")
            return
        itemId = urllib.parse.quote(self.itemID)
        server = "api.neople.co.kr"  # 물음표까지 다써도됌
        client_id = ""
        client_secret = "su795WU14mjFeoFzOitaqgPYKXzXF5BI"
        conn = http.client.HTTPSConnection(server)
        conn.request("GET","/df/items/" + itemId  + "?apikey=su795WU14mjFeoFzOitaqgPYKXzXF5BI")
        response = conn.getresponse()
        cLen = response.getheader("Content-Length")  # 헤더에서 Content-Length 즉 얼만큼 읽었는지 추출
        result = response.read(int(cLen)).decode('utf-8')
        #파싱
        jsonData = ParsingData2(result)

        if len(jsonData.jsonData) == 0:
            return

        url = "https://img-api.neople.co.kr/df/items/" + jsonData.itemID
        outpath = "images/"
        outfile = "image_" +jsonData.itemName + ".png"

        if not os.path.isdir(outpath):
            os.makedirs(outpath)

        urllib.request.urlretrieve(url, outpath + outfile)

        self.jsonData = jsonData
        self.process.InsertSideCanvas(self.jsonData)

class ParsingData:
    def __init__(self):
        #기본
        self.itemID = None
        self.itemName = None
        self.itemRarity = None
        self.itemType = None
        self.itemDetail = None
        self.itemAvailableLevel = None



    def __str__(self):

        return " [아이템 고유코드 : " + self.itemID + "]\n [아이템이름 : " + self.itemName + "]\n [아이템 레어도 : " + self.itemRarity + "]\n [아이템 타입 : " + self.itemType + "]\n [아이템 타입상세 : " + self.itemDetail + "]\n [아이템 착용레벨 : " + self.itemAvailableLevel + "]\n"

class ParsingDataOfItems:
    def __init__(self,JSON):
        self.jsonData = json.loads(JSON)


        self.itemList= []

        for i in range(len(self.jsonData["rows"])):
            self.itemList.append(ParsingData())
            self.itemList[-1].itemID = self.jsonData["rows"][i]["itemId"]
            self.itemList[-1].itemName = self.jsonData["rows"][i]["itemName"]
            self.itemList[-1].itemRarity = self.jsonData["rows"][i]["itemRarity"]
            self.itemList[-1].itemType = self.jsonData["rows"][i]["itemType"]
            self.itemList[-1].itemDetail = str(self.jsonData["rows"][i]["itemTypeDetail"])
            self.itemList[-1].itemAvailableLevel = str(self.jsonData["rows"][i]["itemAvailableLevel"])


class ParsingDataOfMarkets:
    def __init__(self,JSON):
        self.jsonData = json.loads(JSON)

        self.itemList = []
        for i in range(len(self.jsonData["rows"])):
            self.itemList.append(ParsingData3())
            self.itemList[-1].itemID = self.jsonData["rows"][i]["itemId"]
            self.itemList[-1].itemName = self.jsonData["rows"][i]["itemName"]
            self.itemList[-1].itemRarity = self.jsonData["rows"][i]["itemRarity"]
            self.itemList[-1].itemType = self.jsonData["rows"][i]["itemType"]
            self.itemList[-1].itemDetail = str(self.jsonData["rows"][i]["itemTypeDetail"])
            self.itemList[-1].itemAvailableLevel = str(self.jsonData["rows"][i]["itemAvailableLevel"])

            self.itemList[-1].auctionNo = self.jsonData["rows"][i]["auctionNo"]
            self.itemList[-1].regData = self.jsonData["rows"][i]["regDate"]
            self.itemList[-1].expireData = self.jsonData["rows"][i]["expireDate"]
            self.itemList[-1].refine = self.jsonData["rows"][i]["refine"]
            self.itemList[-1].reinforce = self.jsonData["rows"][i]["reinforce"]
            self.itemList[-1].amplificationName = self.jsonData["rows"][i]["amplificationName"]
            self.itemList[-1].count = self.jsonData["rows"][i]["count"]
            self.itemList[-1].price = self.jsonData["rows"][i]["price"]
            self.itemList[-1].currentPrice = self.jsonData["rows"][i]["currentPrice"]
            self.itemList[-1].unitPrice = self.jsonData["rows"][i]["unitPrice"]
            self.itemList[-1].averagePrice = self.jsonData["rows"][i]["averagePrice"]



class ParsingData2:
    def __init__(self,JSON):
        self.jsonData = json.loads(JSON)
        if len(self.jsonData) == 0:
            return

        self.itemID = self.jsonData["itemId"]
        self.itemName = self.jsonData["itemName"]
        self.itemRarity = self.jsonData["itemRarity"]
        self.itemType = self.jsonData["itemType"]
        self.itemTypeDetail = str(self.jsonData["itemTypeDetail"])
        self.itemAvailableLevel = str(self.jsonData["itemAvailableLevel"])
        self.itemObtainInfo = self.jsonData["itemObtainInfo"]
        self.itemExplain = self.jsonData["itemExplain"]
        self.itemExplainDetail = self.jsonData["itemExplainDetail"]
        self.itemFlavorText = self.jsonData["itemFlavorText"]
        self.setItemId = self.jsonData["setItemId"]
        self.setItemName = self.jsonData["setItemName"]
        self.itemStatus = None
        if "itemStatus" in self.jsonData.keys():
            self.itemStatus = self.jsonData["itemStatus"]

        self.itemReinforceSkill = None
        if "itemReinforceSkill" in self.jsonData.keys():
            self.itemReinforceSkill = self.jsonData["itemReinforceSkill"]
#        print(type(self.itemReinforceSkill))



    def __str__(self):

        newLine =40

        if len(self.jsonData) == 0:
            return ""

        returnString = " [아이템 고유코드 : " + self.itemID + "]\n [아이템이름 : " + self.itemName + "]\n [아이템 레어도 : " + self.itemRarity + "]\n [아이템 타입 : " + self.itemType + "]\n [아이템 타입상세 : " + self.itemTypeDetail + "]\n [아이템 착용레벨 : " + self.itemAvailableLevel + "]\n"


        if(self.itemObtainInfo != None):
            if len(self.itemObtainInfo) // newLine > 0:
                lst = list(self.itemObtainInfo)
                temp = len(self.itemObtainInfo) // newLine
                self.itemObtainInfo = ""
                for i in range(temp):
                    lst.insert(newLine * (i + 1),'\n')
                for i in lst:
                    self.itemObtainInfo += i
            returnString += "[" + self.itemObtainInfo + "]\n"


        if(self.itemExplain != None):

            if len(self.itemExplain) // newLine > 0:
                lst = list(self.itemExplain)
                temp = len(self.itemExplain) // newLine
                self.itemExplain = ""
                for i in range(temp):
                    lst.insert(newLine * (i + 1),'\n')
                for i in lst:
                    self.itemExplain += i

            returnString += "[" + self.itemExplain + "]\n"

        if(self.itemExplainDetail != None):

            if len(self.itemExplainDetail) // newLine > 0:
                lst = list(self.itemExplainDetail)
                temp = len(self.itemExplainDetail) // newLine
                self.itemExplainDetail = ""
                for i in range(temp):
                    lst.insert(newLine * (i + 1),'\n')
                for i in lst:
                    self.itemExplainDetail += i

            returnString += "[" + self.itemExplainDetail + "]\n"


        if(self.itemFlavorText != None):

            if len(self.itemFlavorText) // newLine > 0:
                lst = list(self.itemFlavorText)
                temp = len(self.itemFlavorText) // newLine
                self.itemFlavorText = ""
                for i in range(temp):
                    lst.insert(newLine * (i + 1),'\n')
                for i in lst:
                    self.itemFlavorText += i

            returnString +=  "[" + self.itemFlavorText + "]\n"

        if(self.setItemName != None):
            returnString += "[" + self.setItemName + "]\n"

        return returnString

class ParsingData3():
    def __init__(self):
        #기본
        self.itemID = None
        self.itemName = None
        self.itemRarity = None
        self.itemType = None
        self.itemDetail = None
        self.itemAvailableLevel = None


        #경매장
        self.auctionNo = None
        self.regData = None
        self.expireData = None
        self.refine = None
        self.reinforce = None
        self.amplificationName = None
        self.count = None
        self.price = None
        self.currentPrice = None
        self.unitPrice = None
        self.averagePrice = None
    def __str__(self):

        return "[아이템이름 : " + self.itemName + "]\n [아이템 레어도 : " + self.itemRarity + "]\n [아이템 타입 : " + self.itemType + "]\n [아이템 타입상세 : " + self.itemDetail + "]\n [아이템 착용레벨 : " + self.itemAvailableLevel + "]\n"\
                + "[가격 : " + str(self.currentPrice) +"]\n"

    def GetItemName(self):

        return "[ " + self.itemName + " ]"

    def GetAuctionNo(self):

        return "[ " + self.auctionNo + " ]"
    def GetRefine(self):

        return "[ +" + str(self.refine) + " ]"

    def GetReinforce(self):

        return "[ +" + str(self.reinforce) + " ]"
    def GetCurrentPrice(self):
        return "[ " + str(self.currentPrice) + " ]"
    def GetRemainDate(self):
        #시간차를 구한다!
        import datetime
        expire = datetime.datetime.strptime(self.expireData,'%Y-%m-%d %H:%M:%S')

        reg = datetime.datetime.now()
        import spam


        difference = expire - reg

        difference = spam.division(difference.total_seconds(), 3600)

        difference = "%.1f" % difference

        return "[ " + str(difference) + "h ]"
    def GetCount(self):

        return "[ " + str(self.count) + " ]"

class DNFMarketProcess(Interface):
    # 버튼 이미지를 받아온다.
    global buttondrawer

    # 이벤트 함수 바인딩을 위해 정의했다. - 송민수#########################################
    def Change_Search_IN(self, event):
        self.searchButton.configure(image = buttondrawer.img_button_search_over_teal)
    def Change_Search_OUT(self, event):
        self.searchButton.configure(image = buttondrawer.img_button_search)
    def Change_Reset_IN(self, event):
        self.resetButton.configure(image = buttondrawer.img_button_reset_over_teal)
    def Change_Reset_OUT(self, event):
        self.resetButton.configure(image = buttondrawer.img_button_reset)
    ###################################################################################

    def __init__(self,mainWindow):
        self.mainWindowClass = mainWindow
        self.tabFrame1 = Canvas(mainWindow.window)
        self.notebook = mainWindow.notebook
        self.notebook.add(self.tabFrame1, image = buttondrawer.img_tab_market)

        self.image = PhotoImage(file = "mapleGold.png").subsample(8,8)
        self.imageLabel = Label(self.tabFrame1,image = self.image)
        self.imageLabel.grid(row = 2,column = 0)

        tempFont = Font(mainWindow.window, size=15, weight='bold', family='Consolas')

        self.searchEntry = Entry(self.tabFrame1,font = tempFont, width = 50,relief = 'ridge',borderwidth = 5)
        self.searchEntry.grid(row = 2, column = 1)

        ### 색깔 애니메이션
        self.colorCount = 0
        self.colorCountLimit = 30
        self.colorIncreaseDirection = True

        ###

        ### 프레임 애니메이션
        self.frameImage = []
        self.currentBackgroundFrame = 0
        self.LoadItemBaseImageFile()

        self.tabFrame1.create_image(615,375,image = self.frameImage[self.currentBackgroundFrame],tag = "background")
        ###




        # 검색
        self.searchButton = Button(self.tabFrame1, image = buttondrawer.img_button_search, bd = 0)
        self.searchButton.grid(row = 2,column = 2)

        # 이벤트 함수 바인딩
        self.searchButton.bind("<Enter>", self.Change_Search_IN)
        self.searchButton.bind("<Leave>", self.Change_Search_OUT)


        # 리셋
        self.resetButton = Button(self.tabFrame1, image = buttondrawer.img_button_reset, bd = 0)
        self.resetButton.grid(row = 2,column = 3)

        # 이벤트 함수 바인딩
        self.resetButton.bind("<Enter>", self.Change_Reset_IN)
        self.resetButton.bind("<Leave>", self.Change_Reset_OUT)


        #   오름차순,내림차순 정렬
        self.sortButton = Button(self.tabFrame1,text = "정렬",width = 15,relief = 'groove')
        self.sortButton.grid(row = 4,column =  5)


###


###     라벨들(아이콘   이름     레벨  마감   가격)
        font2 = Font(family="배달의민족 주아", size=20)

        self.labelText = ["강화","재련","이름","마감","가격(골드)","수량"]
        self.labels = [Label(self.tabFrame1,text = self.labelText[i],font = font2) for i in range(len(self.labelText))]


        self.offsetX = 140
        self.offsetY = 120

        self.labels[0].place(x = self.offsetX,y = self.offsetY)
        self.labels[1].place(x = self.offsetX + 60,y = self.offsetY)
        self.labels[2].place(x = self.offsetX + 140,y = self.offsetY)
        self.labels[3].place(x = self.offsetX + 740,y = self.offsetY)
        self.labels[4].place(x = self.offsetX + 830,y = self.offsetY)
        self.labels[5].place(x=self.offsetX + 660, y=self.offsetY)

###


        self.emptyCanvas = Canvas(self.tabFrame1,width = 20,height = 15)
        self.emptyCanvas.grid(row = 2,column = 4)

        self.sortCategory = ["이름 순","가격 순","레벨 순"]
        self.sortCategoryCombobox = ttk.Combobox(self.tabFrame1, height = 15, values = self.sortCategory)
        self.sortCategoryCombobox.grid(row =2, column = 5)
        self.sortCategoryCombobox.set("이름 순")
        #랜덤으로 최근에 올라온 아이템 20개씩 보여주는 기능


###     combobox

        self.rarityCategoryList = ["커먼","언커먼","레어","유니크","크로니클","레전더리","에픽","암거나"]

        self.emptyCanvas2 = Canvas(self.tabFrame1,width = 20,height = 15)
        self.emptyCanvas2.grid(row = 2,column = 6)

        self.rarityCombobox = ttk.Combobox(self.tabFrame1,height = 15,values = self.rarityCategoryList)
        self.rarityCombobox.grid(row =2 , column = 7)
        self.rarityCombobox.set("암거나")
###


###     levelEntry

        self.emptyCanvas3 = Canvas(self.tabFrame1,width = 10,height = 15)
        self.emptyCanvas3.grid(row = 2,column = 8)

        self.levelLabel = Label(self.tabFrame1,text = "레벨")
        self.levelLabel.grid(row =2 , column = 9)

        self.levelEntry = Entry(self.tabFrame1,width = 3)
        self.levelEntry.grid(row = 2,column = 10)

        self.levelLabel2 = Label(self.tabFrame1,text = "~")
        self.levelLabel2.grid(row =2 , column = 11)


        self.levelEntry2 = Entry(self.tabFrame1,width = 3)
        self.levelEntry2.grid(row = 2,column = 12)
###

###     canvas
        self.innerFrame = Frame(self.tabFrame1)
        self.innerFrame.place(x = 25,y = 150)

        #self.textBoard = Text(self.innerFrame)
        #self.textBoard.pack()
        self.canvasWidth = 1150
        self.canvasHeight = 500
        self.canvasScrollbarWidth = 500
        self.canvasScrollbarHeight = 2000

        #self.canvasBackground = PhotoImage(file="background.png")
        # self.canvas = Canvas(self.innerFrame,bg = "#FFF0F0",relief = "solid",bd = 2,width = 800,height = 300,scrollregion = (0,0,500,500))
        self.canvas = Canvas(self.innerFrame, bg="#FFF0F0", relief="solid", bd=2, width=self.canvasWidth,
                             height=self.canvasHeight,
                             scrollregion=(0, 0, self.canvasScrollbarWidth, self.canvasScrollbarHeight))
        #self.canvas.create_image(self.canvasWidth / 2, self.canvasHeight / 2, image=self.canvasBackground)
        self.canvas.create_image(self.canvasWidth / 2, self.canvasHeight / 2)

        self.scrollbar = Scrollbar(self.innerFrame)
        self.scrollbar.pack(fill="y", side=RIGHT)
        self.scrollbar.config(command=self.canvas.yview)

        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=LEFT)

        self.scrollbar["command"] = self.canvas.yview
        # self.entry.lower()


###


### 검색버튼 configure
        self.searchButton.configure(command = lambda  : self.GetItemInfoFromMarket(str(self.searchEntry.get()),self.levelEntry.get(),self.levelEntry2.get(),self.rarityCombobox.get()))
###

### 경매장 바디 출력 관련 파라미터
        self.imageOffsetX = 70
        self.imageOffsetY = 40
        self.imageIntervalY = 60

        #이름
        self.itemNameTextOffsetX = 370
        self.itemNameOffsetY = 40
        self.itemNameIntervalY = 60

        #재련
        self.refineOffsetX = 200
        self.refineOffsetY = 40
        self.refineIntervalY = 60

        #강화
        self.reinforceOffsetX = 130
        self.reinforceOffsetY = 40
        self.reinforceIntervalY = 60

        #가격
        self.currentPriceOffsetX = 1000
        self.currentPriceOffsetY = 40
        self.currentPriceOffIntervalY = 60

        #남은기간
        self.remainDateOffsetX = 880
        self.remainDateOffsetY = 40
        self.remainDateIntervalY = 60

        #남은기간
        self.countOffsetX = 800
        self.countOffsetY = 40
        self.countIntervalY = 60


        self.textCurrentX = self.canvasWidth / 2
        self.textCurrentY = self.canvasHeight * 0.12
        self.textHeight = self.canvasHeight * 0.24
        self.textMaxHeight = self.canvasScrollbarHeight
###

### parsingDataList
        self.parsingDataList = []
        # self.buttonFunctionInstances = []
###

### 버튼에 묶을 함수들 재설정..
        self.resetButton.configure(command = self.ClearCanvas)
###


### 그래프 그리기를 위한 파라미터

###

### 이미지는 왜 업데이트를 해줘야해 귀찮게
        self.tabFrame1.update()

        self.ItemBaseAnimation()

        self.itemImages = []

###


    def LoadItemBaseImageFile(self):
        for i in range(1, 30):
            fname = "great/great (" + str(i) + ").png"
            self.frameImage += [PhotoImage(file=fname)]

    def ItemBaseAnimation(self):


        self.currentBackgroundFrame = (self.currentBackgroundFrame + 1) % 29
        self.tabFrame1.delete("background")
        ### 프레임 애니메이션
        self.tabFrame1.create_image(615,375,image = self.frameImage[self.currentBackgroundFrame],tag = "background")


        if self.colorIncreaseDirection:
            self.colorCount +=1
            if self.colorCount >= self.colorCountLimit:
                self.colorIncreaseDirection = False
        else:
            self.colorCount -=1
            if self.colorCount <= 0:
                self.colorIncreaseDirection = True


        color = 0xCCF435 + self.colorCount * 5

        colorString = str(hex(color))

        colorString = colorString.replace("0x","#")
        colorString = colorString.upper()

        self.canvas.configure(bg=colorString)

        self.tabFrame1.update()
        self.mainWindowClass.window.after(50,self.ItemBaseAnimation)
        ###

        pass


    def ResetCanvas(self):
        self.textCurrentX = self.canvasWidth/2
        self.textCurrentY = self.canvasHeight*0.12
        self.canvas.delete(ALL)
        #self.canvas.create_image(self.canvasWidth/2,self.canvasHeight/2,image = self.canvasBackground)
        self.canvas.create_image(self.canvasWidth / 2, self.canvasHeight / 2)
        pass

    def ClearCanvas(self):
        self.parsingDataList.clear()
        self.ResetCanvas()


    def Sort(self,sortingStandard = "가격 순"):

        #이름
        if sortingStandard == self.sortCategory[0]:
            def Temp():
                return
            self.parsingDataList.sort( )
            pass
        #가격
        elif sortingStandard == self.sortCategory[1]:
            pass
        #레벨
        elif sortingStandard == self.sortCategory[2]:
            pass


        pass

    def DrawMarketGraph(self):

        priceList = [int(self.parsingDataList[i].currentPrice) for i in range(len(self.parsingDataList))]

        minimum = min(priceList)
        maximum = max(priceList)
        print("그려라고")
        rate = 0.01
        difference = maximum - minimum

        interval = int(rate * difference)

        priceList2 = [ ((priceList[i] - minimum)//interval) * interval  for i in range(len(priceList))]

        unOverlappedList = []




        for i in range(len(priceList2)):
            if not priceList2[i] in unOverlappedList:
                unOverlappedList.append(priceList2[i])


        frequencyList = [0] * len(unOverlappedList)
        #중복횟수 세기
        for i in range(len(frequencyList)):
            frequencyList[i] += priceList2.count(unOverlappedList[i])


        print(frequencyList)

        print(unOverlappedList)


        offsetX = self.canvasWidth * 0.48
        offsetY = (self.canvasHeight  + self.canvasScrollbarHeight) * 0.77

        graphHeight = 100
        grapthWidth = 15

        print(minimum)
        print(maximum)
        print(interval)

        for i in range(len(unOverlappedList)):
            self.canvas.create_rectangle(offsetX + i * grapthWidth,offsetY,offsetX +(i + 1) * grapthWidth ,offsetY -(unOverlappedList[i] / maximum) * graphHeight )
            self.canvas.create_text(offsetX + i * grapthWidth + 0.5 * grapthWidth,offsetY -(unOverlappedList[i] / maximum) * graphHeight- graphHeight*0.1,text = str(frequencyList[i]) )

        self.canvas.create_text(offsetX + (len(unOverlappedList) * grapthWidth)/2,offsetY + graphHeight * 0.2, text = "가장 높은 가격 : " + str(maximum))
        self.canvas.create_text(offsetX + (len(unOverlappedList) * grapthWidth)/2,offsetY + graphHeight * 0.4, text = "가장 낮은 가격 : " + str(minimum))
        self.canvas.create_text(offsetX + (len(unOverlappedList) * grapthWidth)/2,offsetY + graphHeight * 0.6, text = "그래프의 구간은" + str(interval))
        pass
    def SendEmail(self,gmailID,password,address):
        pass

    def ShowMainCanvas(self):

        self.ResetCanvas()


        #images = []



        #canvasFrames = []
        #canvasFrame = Frame(self.canvas)
        # self.canvas.create_window(self.canvasWidth - 100,100,window = canvasFrame)
        #s = Button(canvasFrame,text = "아!!!")
        #s.pack()
        count = 0

        self.itemImages.clear()

        for i in range(len(self.parsingDataList)):
            if (self.textCurrentY > self.textMaxHeight):
                print("캔버스 높이 초과")
                self.parsingDataList.pop()
                #self.mainWindowClass.window.mainloop()
                self.tabFrame1.update()
                self.canvas.update()
                return

            outfile = "images/" + "image_" + self.parsingDataList[i].itemName + ".png"
            print(outfile)
            outfile = outfile.replace(":", "-")
            self.itemImages.append(PhotoImage(file=outfile))

            self.canvas.create_image(self.imageOffsetX , self.imageOffsetY+ i*self.imageIntervalY , image=self.itemImages[-1])
            self.canvas.create_rectangle(self.imageOffsetX - 20,self.imageOffsetY - 20 + i*self.imageIntervalY,self.imageOffsetX + 20, self.imageOffsetY + 20 + i*self.imageIntervalY , outline = "#FFB400" , width = 3)



            boldFont = Font(family="배달의민족 한나체 pro", size=14, weight="bold")

            self.canvas.create_text(self.itemNameTextOffsetX, self.itemNameOffsetY + i * self.itemNameIntervalY, text=self.parsingDataList[i].GetItemName(), font=boldFont)
            self.canvas.create_text(self.currentPriceOffsetX,self.currentPriceOffsetY + i*self.currentPriceOffIntervalY,text = self.parsingDataList[i].GetCurrentPrice(),font = boldFont)
            self.canvas.create_text(self.refineOffsetX,self.refineOffsetY + i*self.refineIntervalY,text = self.parsingDataList[i].GetRefine(),font = boldFont)
            self.canvas.create_text(self.reinforceOffsetX,self.reinforceOffsetY + i*self.reinforceIntervalY,text = self.parsingDataList[i].GetReinforce(),font = boldFont)
            self.canvas.create_text(self.remainDateOffsetX,self.remainDateOffsetY + i*self.remainDateIntervalY,text = self.parsingDataList[i].GetRemainDate(),font = boldFont)
            self.canvas.create_text(self.countOffsetX,self.countOffsetY + i*self.countIntervalY,text = self.parsingDataList[i].GetCount(),font = boldFont)


            self.textCurrentY += self.imageIntervalY

            #canvasFrames.append(Frame(self.canvas))
            #self.canvas.create_window(self.textCurrentX + 250,self.textCurrentY -105,window = canvasFrames[-1])

            #self.detailButtonList.append(Button(canvasFrames[-1],text = "상세보기" ,command = self.buttonFunctionInstances[i].GetItemDetailInfoFromDatabase))
            #self.detailButtonList.append(Button(canvasFrames[-1], text="상세보기", command=lambda: self.GetItemDetailInfoFromDatabase(self.parsingDataList[i])))
            #self.detailButtonList[-1].pack()
            count +=1

        #trie 자료구조를 만들어야
        #검색 자동완성기능을 만들수있음
        #그건 패스
        self.DrawMarketGraph()
        #self.mainWindowClass.window.mainloop()
        self.tabFrame1.update()
        self.canvas.update()

        pass


        pass
    def GetItemInfoFromMarket(self,itemName,minLevel = "0",maxLevel = "999",rarity = "암거나",itemType = "암거나"):
        if (itemName == ""):
            print("비어있는입력")
            return




        #URL인코딩?

        #경매장:
        #https://api.neople.co.kr/df/auction?itemName=<itemName>&q=minLevel:<minLevel>,maxLevel:<maxLevel>,rarity:<rarity>,minReinforce:<minReinforce>,maxReinforce:<maxReinforce>,minRefine:<minRefine>,maxRefine:<maxRefine>&sort=unitPrice:<unitPrice>,reinforce:<reinforce>,auctionNo:<auctionNo>&limit=<limit>&wordType=<wordType>&apikey=su795WU14mjFeoFzOitaqgPYKXzXF5BI

        server = "api.neople.co.kr"  # 물음표까지 다써도됌
        client_id = ""
        client_secret = "su795WU14mjFeoFzOitaqgPYKXzXF5BI"
        conn = http.client.HTTPSConnection(server)
        conn.request("GET","/df/auction?itemName=" +urllib.parse.quote(itemName) + "&q=minLevel:" + minLevel + ",maxLevel:" + maxLevel  + ",rarity:" + urllib.parse.quote(rarity) + ",minReinforce:<minReinforce>,maxReinforce:<maxReinforce>,minRefine:<minRefine>,maxRefine:<maxRefine>&sort=unitPrice:<unitPrice>,reinforce:<reinforce>,auctionNo:<auctionNo>&limit=33&wordType=front&apikey=su795WU14mjFeoFzOitaqgPYKXzXF5BI")
        response = conn.getresponse()
        cLen = response.getheader("Content-Length")  # 헤더에서 Content-Length 즉 얼만큼 읽었는지 추출

        result = response.read(int(cLen)).decode('utf-8')

        jsonData = ParsingDataOfMarkets(result)

        print(result)

        from pathlib import Path
        for i in range(len(jsonData.itemList)):
            if(itemType != "암거나" and jsonData.itemList[i].itemType != itemType):
                print(jsonData.itemList[i].itemType)
                print(itemType)
                continue
            elif(rarity != "암거나" and jsonData.itemList[i].itemRarity != rarity):
                print(jsonData.itemList[i].itemType)
                print(itemType)
                continue


            url = "https://img-api.neople.co.kr/df/items/" + jsonData.itemList[i].itemID
            outpath = "images/"
            outfile = "image_" +jsonData.itemList[i].itemName + ".png"

            outfile = outfile.replace(":","-")

            if not os.path.isdir(outpath):
                os.makedirs(outpath)



            filePath = Path(outfile)
            if not filePath.is_file():
                urllib.request.urlretrieve(url, outpath + outfile)

            self.parsingDataList.append(jsonData.itemList[i])
            #self.buttonFunctionInstances.append(ButtonFunction(jsonData.itemList[i].itemID, self))
        self.ShowMainCanvas()
        pass

    def GetItemInfoFromDatabase(self, itemName,minLevel = "0",maxLevel = "999",rarity = "암거나",itemType = "암거나"):

        if (itemName == ""):
            print("비어있는입력")
            return

        #URL인코딩?




        print(itemType)

        server = "api.neople.co.kr"  # 물음표까지 다써도됌
        client_id = ""
        client_secret = "su795WU14mjFeoFzOitaqgPYKXzXF5BI"
        conn = http.client.HTTPSConnection(server)
        # conn.request("GET", "/df/servers/cain/characters?characterName=dog&jobId=<jobId>&jobGrowId=<jobGrowId>&limit=<limit>&wordType=<wordType>&apikey=fS1DhnBRYjp0EIzzj2pMONApSNSkhOYV")
        #conn.request("GET", "/df/servers?apikey=su795WU14mjFeoFzOitaqgPYKXzXF5BI")
        conn.request("GET","/df/items?itemName=" +urllib.parse.quote(itemName) +  "&q=minLevel:" + minLevel + ",maxLevel:" + maxLevel + ",rarity:" + urllib.parse.quote(rarity) +",trade:<trade>&limit=<limit>&wordType=front&apikey=su795WU14mjFeoFzOitaqgPYKXzXF5BI")
        # 서버에 GET 요청
        # GET은 정보를 달라는것
        # {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}
        # 이거는 http connection 문법인데,헤더에다가 클라이언트 아이디,시크릿을 추가했다

        response = conn.getresponse()


        cLen = response.getheader("Content-Length")  # 헤더에서 Content-Length 즉 얼만큼 읽었는지 추출

        result = response.read(int(cLen)).decode('utf-8')
        print(result)
        jsonData = ParsingDataOfItems(result)

        #print(type(result)) #<class 'bytes'>
        #self.canvas.create_text()
        from pathlib import Path
        for i in range(len(jsonData.itemList)):
            if(itemType != "암거나" and jsonData.itemList[i].itemType != itemType):
                print(jsonData.itemList[i].itemType)
                print(itemType)
                continue
            elif(rarity != "암거나" and jsonData.itemList[i].itemRarity != rarity):
                print(jsonData.itemList[i].itemType)
                print(itemType)
                continue


            url = "https://img-api.neople.co.kr/df/items/" + jsonData.itemList[i].itemID
            outpath = "images/"
            outfile = "image_" +jsonData.itemList[i].itemName + ".png"

            outfile = outfile.replace(":","-")

            if not os.path.isdir(outpath):
                os.makedirs(outpath)

            filePath = Path(outfile)
            if not filePath.is_file():
                urllib.request.urlretrieve(url, outpath + outfile)

            self.parsingDataList.append(jsonData.itemList[i])
            #self.buttonFunctionInstances.append(ButtonFunction(jsonData.itemList[i].itemID, self))



        pass





#503 시스템 점검
class DNFAPIProcess(Interface):
    global buttondrawer

    # 이벤트 함수 바인딩을 위해 정의했다. - 송민수#########################################
    def Change_Search_IN(self, event):
        self.searchButton.configure(image=buttondrawer.img_button_search_over_teal)

    def Change_Search_OUT(self, event):
        self.searchButton.configure(image=buttondrawer.img_button_search)

    def Change_Reset_IN(self, event):
        self.resetButton.configure(image=buttondrawer.img_button_reset_over_teal)

    def Change_Reset_OUT(self, event):
        self.resetButton.configure(image=buttondrawer.img_button_reset)

    def Change_Send_IN(self, event):
        self.gmailSendButton.configure(image=buttondrawer.img_button_send_over_teal)

    def Change_Send_OUT(self, event):
        self.gmailSendButton.configure(image=buttondrawer.img_button_send)
        ###################################################################################

    def __init__(self, mainWindow):
        self.mainWindowClass = mainWindow

        self.notebook = mainWindow.notebook


        self.tabFrame1 = Canvas(mainWindow.window)
        #self.tabFrame2 = Frame(window)
        #self.tabFrame3 = Frame(window)
        #self.tabFrame4 = Frame(window)
        self.notebook.add(self.tabFrame1, image = buttondrawer.img_tab_dnf)
        #self.notebook.add(self.tabFrame2,text = "던파 경매장")
        #self.notebook.add(self.tabFrame3,text = "네이버 도서검색")
        #self.notebook.add(self.tabFrame4,text = "롤 전적검색")
        #self.tabFrame1.create_oval(0,0,55,55)

        ### 프레임 애니메이션
        self.frameImage = []
        self.currentBackgroundFrame = 0
        self.LoadItemBaseImageFile()

        self.tabFrame1.create_image(615,375,image = self.frameImage[self.currentBackgroundFrame],tag = "background")
        ###


        self.image = PhotoImage(file = "search4.png").subsample(6,6)
        self.imageLabel = Label(self.tabFrame1,image = self.image)
        self.imageLabel.grid(row = 2,column = 0)

        TempFont = Font(mainWindow.window, size=15, weight='bold', family='Consolas')

        self.searchEntry = Entry(self.tabFrame1,font = TempFont, width = 50,relief = 'solid',borderwidth = 5)
        self.searchEntry.grid(row = 2, column = 1)

        self.searchButton = Button(self.tabFrame1, image = buttondrawer.img_button_search, bd = 0)
        self.searchButton.grid(row = 2,column = 2)

        # 이벤트 함수 바인딩
        self.searchButton.bind("<Enter>", self.Change_Search_IN)
        self.searchButton.bind("<Leave>", self.Change_Search_OUT)

        self.resetButton = Button(self.tabFrame1,image = buttondrawer.img_button_reset, command = self.ClearCanvas, bd = 0)
        self.resetButton.grid(row = 2,column = 3)

        # 이벤트 함수 바인딩
        self.resetButton.bind("<Enter>", self.Change_Reset_IN)
        self.resetButton.bind("<Leave>", self.Change_Reset_OUT)




        self.rarityCategoryList = ["커먼","언커먼","레어","유니크","크로니클","레전더리","에픽","암거나"]

        self.emptyCanvas = Canvas(self.tabFrame1,width = 20,height = 15)
        self.emptyCanvas.grid(row = 2,column = 4)

        self.rarityCombobox = ttk.Combobox(self.tabFrame1,height = 15,values = self.rarityCategoryList)
        self.rarityCombobox.grid(row =2 , column = 5)
        self.rarityCombobox.set("무기 등급")




        self.weaponCategoryList = ["무기","방어구","악세사리","특수장비","재료","아바타","암거나"]

        self.emptyCanvas2 = Canvas(self.tabFrame1,width = 20,height = 15)
        self.emptyCanvas2.grid(row = 2,column = 6)

        self.weaponCategoryCombobox = ttk.Combobox(self.tabFrame1,height = 15,values = self.weaponCategoryList)
        self.weaponCategoryCombobox.grid(row =2 , column = 7)
        self.weaponCategoryCombobox.set("장비 종류")



###     canvas

        self.canvasWidth = 800
        self.canvasHeight = 600
        self.canvasScrollbarWidth = 500
        self.canvasScrollbarHeight = 1000


        self.innerFrame = Canvas(self.tabFrame1,width = self.canvasWidth ,height = self.canvasHeight)
        self.innerFrame.place(x = 25,y = 100)


        #self.textBoard = Text(self.innerFrame)
        #self.textBoard.pack()



        self.canvasBackground = PhotoImage(file = "background.png")
        #self.canvas = Canvas(self.innerFrame,bg = "#FFF0F0",relief = "solid",bd = 2,width = 800,height = 300,scrollregion = (0,0,500,500))
        self.canvas = Canvas(self.innerFrame, bg="#FFF0F0", relief="solid", bd=1, width=self.canvasWidth, height=self.canvasHeight,scrollregion=(0, 0, self.canvasScrollbarWidth, self.canvasScrollbarHeight))
        self.canvas.create_image(self.canvasWidth/2,self.canvasHeight/2,image = self.canvasBackground)
        self.canvas.grid(row = 0,column = 1)
        #self.canvas.grid(row=0, column=0, sticky="news")



        self.scrollbar = Scrollbar(self.innerFrame, command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=2, sticky='ns')

        #self.scrollbar = Scrollbar(self.canvas, command=self.canvas.yview)
        #self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')

        self.canvas.config(yscrollcommand = self.scrollbar.set)





        #self.scrollbar["command"] = self.canvas.yview
        #self.entry.lower()

        self.textCurrentX = self.canvasWidth/2
        self.textCurrentY = self.canvasHeight*0.12
        self.textHeight = self.canvasHeight*0.24
        self.textMaxHeight = self.canvasScrollbarHeight

        self.detailButtonList = []

###




        self.parsingDataList = []
        self.parsingDataList2 = []

### sideCanvas
        self.sideCanvasWidth = 400
        self.sideCanvasHeight = 800
        self.sideFrame = Frame(self.tabFrame1)
        self.sideFrame.place(x = 850,y = 100)
        self.sideCanvas = Canvas(self.sideFrame, relief="groove", bd=2, width=self.sideCanvasWidth,
                                 height=self.sideCanvasHeight)
        self.sideCanvas.pack(side = LEFT)


### buttonFunctionInstance

        self.buttonFunctionInstances = []

###


### searchOptionCombobox

        self.emptyCanvas2 = Canvas(self.tabFrame1,width = 8,height = 15)
        self.emptyCanvas2.grid(row = 2,column = 9)

        self.searchOptionCategory = ["front","full"]
        self.searchOptionCombobox = ttk.Combobox(self.tabFrame1,height = 15, values = self.searchOptionCategory )
        self.searchOptionCombobox.grid(row =2 , column = 10)
        self.searchOptionCombobox.set("검색 옵션")


        self.searchButton.configure( command = lambda: self.GetItemInfoFromDatabase(str(self.searchEntry.get()),str(0),str(999), str(self.rarityCombobox.get()),str(self.weaponCategoryCombobox.get()),str(self.searchOptionCombobox.get())))


###

### 메일전송

        self.gmailFrame = Frame(self.tabFrame1)
        self.gmailFrame.grid(row = 4,column = 1)

        self.gmailLabel = Label(self.gmailFrame,text = "메일주소")
        self.gmailLabel.pack(side = LEFT)

        self.gmailEntry = Entry(self.gmailFrame)
        self.gmailEntry.pack(side = LEFT)

        self.gmailSendButton = Button(self.gmailFrame, image = buttondrawer.img_button_send, command = lambda : self.SendEmail(self.gmailEntry.get()), bd = 0)
        self.gmailSendButton.pack(side = LEFT)

        # 이벤트 함수 바인딩
        self.gmailSendButton.bind("<Enter>", self.Change_Send_IN)
        self.gmailSendButton.bind("<Leave>", self.Change_Send_OUT)
###

## 배경 이미지 애니메이션의 시작
        self.tabFrame1.update()

        self.ItemBaseAnimation()
###
        
## 아이템 이미지
        self.itemImages = []
        self.itemSideImage = None
        pass

    def LoadItemBaseImageFile(self):
        for i in range(1, 30):
            fname = "great/great (" + str(i) + ").png"
            self.frameImage += [PhotoImage(file=fname)]

    def ItemBaseAnimation(self):


        self.currentBackgroundFrame = (self.currentBackgroundFrame + 1) % 29
        self.tabFrame1.delete("background")
        ### 프레임 애니메이션
        self.tabFrame1.create_image(615,375,image = self.frameImage[self.currentBackgroundFrame],tag = "background")
        self.tabFrame1.update()
        self.mainWindowClass.window.after(50,self.ItemBaseAnimation)
        ###

        pass

    def SendEmail(self,address):

        import mimetypes
        import mysmtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.base import MIMEBase
        from email.mime.text import MIMEText
        from email.mime.image import MIMEImage
        from pathlib import Path
        from email.message import EmailMessage
        # global value
        host = "smtp.gmail.com"  # Gmail STMP 서버 주소.
        port = "587"
        htmlFileName = "logo.html"

        senderAddr = "deven0425@gmail.com"  # 보내는 사람 email 주소.
        recipientAddr = address # 받는 사람 email 주소.

        # msg = MIMEBase("multipart", "alternative")

        s = ""
        name = "제목 : "
        imageName = ""
        for i in range(len(self.parsingDataList2)):
            s += str(self.parsingDataList2[i])
            s += '\n'
            name += self.parsingDataList2[i].itemName
            imageName = "images/image_" + self.parsingDataList2[i].itemName + ".png"


        msg = MIMEText(s, _charset='UTF-8')
        msg['Subject'] = name
        msg['From'] = senderAddr
        msg['To'] = recipientAddr



        # MIME 문서를 생성합니다.
        # htmlFD = open(htmlFileName, 'rb')
        # HtmlPart = MIMEText(htmlFD.read(),'html', _charset = 'UTF-8' )
        # htmlFD.close()

        # 만들었던 mime을 MIMEBase에 첨부 시킨다.
        # msg.attach(HtmlPart)

        # 메일을 발송한다.
        s = mysmtplib.MySMTP(host, port)
        # s.set_debuglevel(1)        # 디버깅이 필요할 경우 주석을 푼다.
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(senderAddr, "xhzkxk0425%")
        s.sendmail(senderAddr, [recipientAddr], msg.as_string())
        s.close()
        print("메일 전송 완료")
        pass
    def ResetCanvas(self):
        self.textCurrentX = self.canvasWidth/2
        self.textCurrentY = self.canvasHeight*0.12
        self.canvas.delete(ALL)
        self.canvas.create_image(self.canvasWidth/2,self.canvasHeight/2,image = self.canvasBackground)

    def ClearCanvas(self):
        self.parsingDataList.clear()
        self.buttonFunctionInstances.clear()
        for i in self.detailButtonList:
            i.destroy()
        self.ResetCanvas()

    def ClearSideCanvas(self):
        self.sideCanvas.delete(ALL)
        pass

    def InsertSideCanvas(self,args):

        self.parsingDataList2.clear()
        self.parsingDataList2.append(args)
        print(args)
        self.ClearSideCanvas()

        outfile = "images/" + "image_" +args.itemName + ".png"
        print(outfile)
        outfile = outfile.replace(":", "-")

        del self.itemSideImage

        self.itemSideImage = PhotoImage(file =  outfile)


        self.sideCanvas.create_image(50,50,image = self.itemSideImage)

        boldFont = Font(family="Helvetica", size=8, weight="bold")

        self.sideCanvas.create_rectangle(25,25, 75,75, outline = "#FFB400" )
        self.sideCanvas.create_text( 200,400,text = str(args),font = boldFont)


        #trie 자료구조를 만들어야
        #검색 자동완성기능을 만들수있음
        #그건 패스

        self.tabFrame1.update()

        pass

    def Test(self,i):
        print(i)


    def ShowMainCanvas(self):

        self.ResetCanvas()


        #images = []




        canvasFrames = []
        #canvasFrame = Frame(self.canvas)
        # self.canvas.create_window(self.canvasWidth - 100,100,window = canvasFrame)
        #s = Button(canvasFrame,text = "아!!!")
        #s.pack()
        count = 0

        self.itemImages.clear()

        for i in range(len(self.parsingDataList)):
            if (self.textCurrentY > self.textMaxHeight):
                print("캔버스 높이 초과")
                self.parsingDataList.pop()
                #self.mainWindowClass.window.mainloop()
                self.tabFrame1.update()
                self.canvas.update()
                return

            outfile = "images/" + "image_" + self.parsingDataList[i].itemName + ".png"
            print(outfile)
            outfile = outfile.replace(":", "-")
            self.itemImages.append(PhotoImage(file=outfile))

            self.canvas.create_image(self.textCurrentX - 300, self.textCurrentY, image=self.itemImages[-1])

            boldFont = Font(family="Helvetica", size=12, weight="bold")

            self.canvas.create_rectangle(self.textCurrentX - 350, self.textCurrentY - 50, self.textCurrentX - 250,
                                         self.textCurrentY + 50)
            self.canvas.create_text(self.textCurrentX, self.textCurrentY, text=str(self.parsingDataList[i]), font=boldFont)
            self.textCurrentY += self.textHeight

            canvasFrames.append(Frame(self.canvas))
            self.canvas.create_window(self.textCurrentX + 250,self.textCurrentY -105,window = canvasFrames[-1])

            self.detailButtonList.append(Button(canvasFrames[-1],text = "상세보기" ,command = self.buttonFunctionInstances[i].GetItemDetailInfoFromDatabase))
            #self.detailButtonList.append(Button(canvasFrames[-1], text="상세보기", command=lambda: self.GetItemDetailInfoFromDatabase(self.parsingDataList[i])))
            self.detailButtonList[-1].pack()
            count +=1


        #trie 자료구조를 만들어야
        #검색 자동완성기능을 만들수있음
        #그건 패스
        #self.mainWindowClass.window.mainloop()
        self.tabFrame1.update()
        self.canvas.update()
        pass

    def get(self,str):
        print(str)



    def GetItemDetailInfoFromDatabase(self,itemId):
        if (itemId == ""):
            print("비어있는입력")
            return
        itemId = urllib.parse.quote(itemId)
        server = "api.neople.co.kr"  # 물음표까지 다써도됌
        client_id = ""
        client_secret = "su795WU14mjFeoFzOitaqgPYKXzXF5BI"
        conn = http.client.HTTPSConnection(server)
        conn.request("GET","/df/items/" + itemId  + "?apikey=su795WU14mjFeoFzOitaqgPYKXzXF5BI")
        response = conn.getresponse()
        cLen = response.getheader("Content-Length")  # 헤더에서 Content-Length 즉 얼만큼 읽었는지 추출
        result = response.read(int(cLen)).decode('utf-8')
        #파싱
        jsonData = ParsingData2(result)

        if len(jsonData.jsonData) == 0:
            return

        from pathlib import Path
        url = "https://img-api.neople.co.kr/df/items/" + jsonData.itemID
        outpath = "images/"
        outfile = "image_" +jsonData.itemName + ".png"
        outfile = outfile.replace(":", "-")

        print(outfile)

        if not os.path.isdir(outpath):
            os.makedirs(outpath)

        filePath = Path(outfile)
        if not filePath.is_file():
            urllib.request.urlretrieve(url, outpath + outfile)

        self.InsertSideCanvas(jsonData)


    def ShowDetailInfomationOnSideCanvas(self):
        pass


    def GetItemInfoFromDatabase(self, itemName,minLevel = "0",maxLevel = "999",rarity = "암거나",itemType = "암거나",searchOption = "full"):

        if (itemName == ""):
            print("비어있는입력")
            return

        #URL인코딩?




        print(itemType)

        server = "api.neople.co.kr"  # 물음표까지 다써도됌
        client_id = ""
        client_secret = "su795WU14mjFeoFzOitaqgPYKXzXF5BI"
        conn = http.client.HTTPSConnection(server)
        # conn.request("GET", "/df/servers/cain/characters?characterName=dog&jobId=<jobId>&jobGrowId=<jobGrowId>&limit=<limit>&wordType=<wordType>&apikey=fS1DhnBRYjp0EIzzj2pMONApSNSkhOYV")
        #conn.request("GET", "/df/servers?apikey=su795WU14mjFeoFzOitaqgPYKXzXF5BI")
        conn.request("GET","/df/items?itemName=" +urllib.parse.quote(itemName) +  "&q=minLevel:" + urllib.parse.quote(minLevel) + ",maxLevel:" + urllib.parse.quote(maxLevel) + ",rarity:" + urllib.parse.quote(rarity) +",trade:<trade>&limit=<limit>&wordType=" + searchOption +"&apikey=su795WU14mjFeoFzOitaqgPYKXzXF5BI")
        # 서버에 GET 요청
        # GET은 정보를 달라는것
        # {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}
        # 이거는 http connection 문법인데,헤더에다가 클라이언트 아이디,시크릿을 추가했다

        response = conn.getresponse()


        cLen = response.getheader("Content-Length")  # 헤더에서 Content-Length 즉 얼만큼 읽었는지 추출

        result = response.read(int(cLen)).decode('utf-8')
        print(result)
        jsonData = ParsingDataOfItems(result)

        #print(type(result)) #<class 'bytes'>
        #self.canvas.create_text()
        from pathlib import Path
        for i in range(len(jsonData.itemList)):
            if(itemType != "암거나" and jsonData.itemList[i].itemType != itemType):
                print(jsonData.itemList[i].itemType)
                print(itemType)
                continue
            elif(rarity != "암거나" and jsonData.itemList[i].itemRarity != rarity):
                print(jsonData.itemList[i].itemType)
                print(itemType)
                continue


            url = "https://img-api.neople.co.kr/df/items/" + jsonData.itemList[i].itemID
            outpath = "images/"
            outfile = "image_" +jsonData.itemList[i].itemName + ".png"

            outfile = outfile.replace(":","-")

            if not os.path.isdir(outpath):
                os.makedirs(outpath)



            filePath = Path(outfile)
            if not filePath.is_file():
                urllib.request.urlretrieve(url, outpath + outfile)

            self.parsingDataList.append(jsonData.itemList[i])
            self.buttonFunctionInstances.append(ButtonFunction(jsonData.itemList[i].itemID, self))

        self.ShowMainCanvas()

        pass


    #사실 이미 Run을 하고있음
    def Run(self):
        pass

def Test():
    outfile = "images/" + "image_" + "발뭉" + ".png"
    print(outfile)
    image = PhotoImage(file=outfile)
    canvas = Canvas(mainWindow.window, relief="solid", bd=2)

    canvas.create_rectangle(200, 200, 300, 300)
    canvas.create_oval(0,0,30,30)
    canvas.create_image(20, 20, image=image)
    canvas.pack()
    mainWindow.window.mainloop()

bool = True

#a = DNFAPIProcess(mainWindow.window)

#a.Run()
#Test()

# 인트로 씬 재생
introscene = Animator.IntroSceneAnimator()
while introscene.animationFlag == True:
    introscene.window.mainloop()



# 씬이 끝나야 메인 윈도우 생성
mainWindow = MainWindow()

buttondrawer = Animator.ButtonDrawer(mainWindow)

gol = DNFAPIProcess(mainWindow)
asd = DNFMarketProcess(mainWindow)
lol = LOL_Mainframe.MainWindow(mainWindow, buttondrawer)
mainWindow.window.mainloop()