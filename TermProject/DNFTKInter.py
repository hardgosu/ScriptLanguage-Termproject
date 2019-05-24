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

class MainWindow:
    def __init__(self):
        self.window = Tk()
        self.window.resizable(False,False)
        self.window.geometry("1280x800+100+100")
        self.window.wm_iconbitmap('DNF.ico')
        self.window.title("useful")


        self.notebook = ttk.Notebook(self.window,width = 1230,height = 750)
        self.notebook.pack()
        #self.window.mainloop()

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

class ParsingDataOfItems:
    def __init__(self,JSON):
        self.jsonData = json.loads(JSON)
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


class LeagueOfLegendSearchProcess(Interface):
    def __init__(self,mainWindow):
        self.mainWindowClass = mainWindow
        self.tabFrame = Frame(mainWindow.window)
        self.notebook = mainWindow.notebook
        self.notebook.add(self.tabFrame,text = "롤 전적검색")




    pass

class DNFMarketProcess(Interface):
    def __init__(self,mainWindow):
        self.mainWindowClass = mainWindow
        self.tabFrame1 = Frame(mainWindow.window)
        self.notebook = mainWindow.notebook
        self.notebook.add(self.tabFrame1,text = "던파 경매장")

        self.image = PhotoImage(file = "mapleGold.png").subsample(8,8)
        self.imageLabel = Label(self.tabFrame1,image = self.image)
        self.imageLabel.grid(row = 2,column = 0)

        tempFont = Font(mainWindow.window, size=15, weight='bold', family='Consolas')

        self.searchEntry = Entry(self.tabFrame1,font = tempFont, width = 50,relief = 'ridge',borderwidth = 5)
        self.searchEntry.grid(row = 2, column = 1)

        self.searchButton = Button(self.tabFrame1, text = "검색", command = lambda  : self.GetItemInfoFromDatabase(str(self.searchEntry.get())))
        self.searchButton.grid(row = 2,column = 2)

        self.resetButton = Button(self.tabFrame1,text = "리셋",command = self.ResetCanvas)
        self.resetButton.grid(row = 2,column = 3)




        #   오름차순,내림차순 정렬
        self.sortButtonText = ["정렬↑","정렬↓"]
        self.sortButtonTextIndex = 0
        self.sortButton = Button(self.tabFrame1,text = self.sortButtonText[self.sortButtonTextIndex],width = 15,relief = 'groove')
        self.sortButton.grid(row = 5,column =  5)





        self.emptyCanvas = Canvas(self.tabFrame1,width = 20,height = 15)
        self.emptyCanvas.grid(row = 2,column = 4)

        self.sortCategory = ["이름 순","가격 순","레벨 순"]
        self.sortCategoryCombobox = ttk.Combobox(self.tabFrame1, height = 15, values = self.sortCategory)
        self.sortCategoryCombobox.grid(row =2, column = 5)
        self.sortCategoryCombobox.set("정렬 기준")
        #랜덤으로 최근에 올라온 아이템 20개씩 보여주는 기능


###
        self.rarityCategoryList = ["커먼","언커먼","레어","유니크","크로니클","레전더리","에픽"]

        self.emptyCanvas2 = Canvas(self.tabFrame1,width = 20,height = 15)
        self.emptyCanvas2.grid(row = 2,column = 6)

        self.rarityCombobox = ttk.Combobox(self.tabFrame1,height = 15,values = self.rarityCategoryList)
        self.rarityCombobox.grid(row =2 , column = 7)
        self.rarityCombobox.set("무기 등급")



###

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


    def ResetCanvas(self):
        self.textCurrentX = self.canvasWidth/2
        self.textCurrentY = self.canvasHeight*0.12
        self.canvas.delete(ALL)
        self.canvas.create_image(self.canvasWidth/2,self.canvasHeight/2,image = self.canvasBackground)





        pass

#503 시스템 점검
class DNFAPIProcess(Interface):
    def __init__(self, mainWindow):
        self.mainWindowClass = mainWindow

        self.notebook = mainWindow.notebook


        self.tabFrame1 = Frame(mainWindow.window)
        #self.tabFrame2 = Frame(window)
        #self.tabFrame3 = Frame(window)
        #self.tabFrame4 = Frame(window)
        self.notebook.add(self.tabFrame1,text = "던파 아이템 정보검색")
        #self.notebook.add(self.tabFrame2,text = "던파 경매장")
        #self.notebook.add(self.tabFrame3,text = "네이버 도서검색")
        #self.notebook.add(self.tabFrame4,text = "롤 전적검색")

        self.image = PhotoImage(file = "search2.png").subsample(6,6)
        self.imageLabel = Label(self.tabFrame1,image = self.image)
        self.imageLabel.grid(row = 2,column = 0)

        TempFont = Font(mainWindow.window, size=15, weight='bold', family='Consolas')

        self.searchEntry = Entry(self.tabFrame1,font = TempFont, width = 50,relief = 'ridge',borderwidth = 5)
        self.searchEntry.grid(row = 2, column = 1)

        self.searchButton = Button(self.tabFrame1, text = "검색", command = lambda  : self.GetItemInfoFromDatabase(str(self.searchEntry.get())))
        self.searchButton.grid(row = 2,column = 2)

        self.resetButton = Button(self.tabFrame1,text = "리셋",command = self.ClearCanvas)
        self.resetButton.grid(row = 2,column = 3)






        self.rarityCategoryList = ["커먼","언커먼","레어","유니크","크로니클","레전더리","에픽"]

        self.emptyCanvas = Canvas(self.tabFrame1,width = 20,height = 15)
        self.emptyCanvas.grid(row = 2,column = 4)

        self.rarityCombobox = ttk.Combobox(self.tabFrame1,height = 15,values = self.rarityCategoryList)
        self.rarityCombobox.grid(row =2 , column = 5)
        self.rarityCombobox.set("무기 등급")




        self.weaponCategoryList = ["무기","방어구","악세사리","특수장비"]

        self.emptyCanvas2 = Canvas(self.tabFrame1,width = 20,height = 15)
        self.emptyCanvas2.grid(row = 2,column = 6)

        self.weaponCategoryCombobox = ttk.Combobox(self.tabFrame1,height = 15,values = self.weaponCategoryList)
        self.weaponCategoryCombobox.grid(row =2 , column = 7)
        self.weaponCategoryCombobox.set("장비 종류")






        self.innerFrame = Frame(self.tabFrame1)
        self.innerFrame.place(x = 25,y = 100)

        #self.textBoard = Text(self.innerFrame)
        #self.textBoard.pack()

        self.canvasWidth = 800
        self.canvasHeight = 600
        self.canvasScrollbarWidth = 500
        self.canvasScrollbarHeight = 1000

        self.canvasBackground = PhotoImage(file = "background.png")
        #self.canvas = Canvas(self.innerFrame,bg = "#FFF0F0",relief = "solid",bd = 2,width = 800,height = 300,scrollregion = (0,0,500,500))
        self.canvas = Canvas(self.innerFrame, bg="#FFF0F0", relief="solid", bd=2, width=self.canvasWidth, height=self.canvasHeight,scrollregion=(0, 0, self.canvasScrollbarWidth, self.canvasScrollbarHeight))
        self.canvas.create_image(self.canvasWidth/2,self.canvasHeight/2,image = self.canvasBackground)

        self.scrollbar = Scrollbar(self.innerFrame)
        self.scrollbar.pack(fill = "y",side = RIGHT)
        self.scrollbar.config(command = self.canvas.yview)

        self.canvas.config(yscrollcommand = self.scrollbar.set)
        self.canvas.pack(side = LEFT)


        self.scrollbar["command"] = self.canvas.yview
        #self.entry.lower()

        self.textCurrentX = self.canvasWidth/2
        self.textCurrentY = self.canvasHeight*0.12
        self.textHeight = self.canvasHeight*0.24
        self.textMaxHeight = self.canvasScrollbarHeight

        self.count = 0


        self.detailButtonList = []

        self.parsingDataList = []

        pass
    def ResetCanvas(self):
        self.textCurrentX = self.canvasWidth/2
        self.textCurrentY = self.canvasHeight*0.12
        self.canvas.delete(ALL)
        self.canvas.create_image(self.canvasWidth/2,self.canvasHeight/2,image = self.canvasBackground)

    def ClearCanvas(self):
        self.ResetCanvas()
        self.textCurrentX = self.canvasWidth/2
        self.textCurrentY = self.canvasHeight*0.12
        self.canvas.delete(ALL)
        self.canvas.create_image(self.canvasWidth/2,self.canvasHeight/2,image = self.canvasBackground)

    def ShowItemSearchResult(self):
        output = ""
        #output +=

        pass

    def InsertCanvas2(self,args):

        if(self.textCurrentY > self.textMaxHeight):
            print("캔버스 높이 초과")
            return

        outfile = "images/" + "image_" +args.itemName + ".png"
        print(outfile)
        image = PhotoImage(file =  outfile)


        self.canvas.create_image(self.textCurrentX - 300,self.textCurrentY,image = image)

        boldFont = Font(family="Helvetica", size=12, weight="bold")

        self.canvas.create_rectangle(self.textCurrentX-350,self.textCurrentY - 50,self.textCurrentX -250,self.textCurrentY+ 50)
        self.canvas.create_text(self.textCurrentX,self.textCurrentY,text = str(args),font = boldFont)
        self.textCurrentY += self.textHeight


        #trie 자료구조를 만들어야
        #검색 자동완성기능을 만들수있음
        #그건 패스

        self.mainWindowClass.window.mainloop()

        pass


    def InsertCanvas(self,args):

        self.ResetCanvas()
        self.parsingDataList.append(args)

        images = []

        for i in self.parsingDataList:
            if (self.textCurrentY > self.textMaxHeight):
                print("캔버스 높이 초과")
                self.parsingDataList.pop()
                self.mainWindowClass.window.mainloop()
                return

            outfile = "images/" + "image_" + i.itemName + ".png"
            print(outfile)
            images.append(PhotoImage(file=outfile))

            self.canvas.create_image(self.textCurrentX - 300, self.textCurrentY, image=images[-1])

            boldFont = Font(family="Helvetica", size=12, weight="bold")

            self.canvas.create_rectangle(self.textCurrentX - 350, self.textCurrentY - 50, self.textCurrentX - 250,
                                         self.textCurrentY + 50)
            self.canvas.create_text(self.textCurrentX, self.textCurrentY, text=str(i), font=boldFont)
            self.textCurrentY += self.textHeight


        #trie 자료구조를 만들어야
        #검색 자동완성기능을 만들수있음
        #그건 패스
        self.mainWindowClass.window.mainloop()


        pass

    def get(self,str):
        print(str)
    def GetItemInfoFromDatabase(self, itemName):

        if (itemName == ""):
            print("비어있는입력")
            return

        #파싱 ..
        itemName = urllib.parse.quote(itemName)

        server = "api.neople.co.kr"  # 물음표까지 다써도됌
        client_id = ""
        client_secret = "su795WU14mjFeoFzOitaqgPYKXzXF5BI"
        conn = http.client.HTTPSConnection(server)
        # conn.request("GET", "/df/servers/cain/characters?characterName=dog&jobId=<jobId>&jobGrowId=<jobGrowId>&limit=<limit>&wordType=<wordType>&apikey=fS1DhnBRYjp0EIzzj2pMONApSNSkhOYV")
        #conn.request("GET", "/df/servers?apikey=su795WU14mjFeoFzOitaqgPYKXzXF5BI")
        conn.request("GET","/df/items?itemName=" +itemName +  "&q=minLevel:<minLevel>,maxLevel:<maxLevel>,rarity:<rarity>,trade:<trade>&limit=<limit>&wordType=<wordType>&apikey=su795WU14mjFeoFzOitaqgPYKXzXF5BI")
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

        if len(jsonData.jsonData["rows"]) == 0:
            return

        url = "https://img-api.neople.co.kr/df/items/" + jsonData.itemID
        outpath = "images/"
        outfile = "image_" +jsonData.itemName + ".png"

        if not os.path.isdir(outpath):
            os.makedirs(outpath)

        urllib.request.urlretrieve(url, outpath + outfile)

        print(jsonData)
        self.InsertCanvas(jsonData)



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
mainWindow = MainWindow()

gol = DNFAPIProcess(mainWindow)
asd = DNFMarketProcess(mainWindow)
lol = LeagueOfLegendSearchProcess(mainWindow)

#a = DNFAPIProcess(mainWindow.window)

#a.Run()
#Test()

mainWindow.window.mainloop()

