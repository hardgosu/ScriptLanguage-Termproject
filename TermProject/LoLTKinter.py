from tkinter import * # import tkinter
import tkinter.ttk as ttk
import urllib.request
from io import BytesIO
from PIL import Image, ImageTk
import json # import json module
import http.client
from tkinter.font import *

## 테스트 용도로 만든 py

def URLdataDecode(urlpath):
    # json 객체로 리턴하는 스태틱 함수
    return json.loads(urllib.request.urlopen(urlpath).read().decode('utf-8'))


#############################################################################################
# 사전 처리 부분
# 현재 롤 클라이언트 버전을 확인하기 위해 데이터 드래곤 url의 한국서버 json 파일을 받아온다.
recentData_url = "https://ddragon.leagueoflegends.com/realms/kr.json"
data = URLdataDecode(recentData_url)
version_champion = data["n"]["champion"]
version_profileicon = data["n"]["profileicon"]
version_language = data["l"]

recentData_Champion_url = "http://ddragon.leagueoflegends.com/cdn/" + version_champion + "/data/" + version_language + "/champion.json"
recentData_Champion = URLdataDecode(recentData_Champion_url)
Champion_List = list(recentData_Champion['data'].keys()) # 현재 챔피언 리스트
##############################################################################################

class SummonerData:
    # 검색한 소환사를 출력하기 위한 클래스
    def __init__(self, _Name, _EncrytedID, _AccountID, _ProfileIconID, _SummonerLevel):
        self.name = _Name
        self.id_Encryted = _EncrytedID
        self.id_Account = _AccountID
        self.id_Profile = _ProfileIconID
        self.level = _SummonerLevel

        self.GetLeagueInfo()
        pass

    def GetLeagueInfo(self):
        server = "kr.api.riotgames.com"
        apiKey = "RGAPI-354e7489-f932-4a39-90ab-24069b93c837"
        conn = http.client.HTTPSConnection(server)
        conn.request("GET",
                     "/lol/league/v4/entries/by-summoner/" + self.id_Encryted + "?api_key=" + apiKey)

        request = conn.getresponse()
        print("Summoner Info Response Code:" + str(request.status))
        if int(request.status) == 200:  # 정상 응답코드는 200
            response_body = request.read().decode('utf-8')

        if response_body == "[]":
            # 리그 정보가 없을 때
            print("검색된 소환사의 리그정보가 없습니다.")
            self.isActive = False
        else:
            # 리그 정보가 있을 때
            jsonData = json.loads(response_body)[0]  # list에 0번 인덱스에 존재하기 때문에.
            print(jsonData)
            self.win = int(jsonData['wins'])
            self.queue = jsonData['queueType']
            self.loss = int(jsonData['losses'])
            self.total = self.win + self.loss
            self.tier = jsonData['tier']
            self.rank = jsonData['rank']
            self.lp = jsonData['leaguePoints']
            self.id_League = jsonData['leagueId']
            self.isActive = True


class RankingSummoner:
    # 챌린저 리그 소환사 객체를 위한 정보 클래스
    def __init__(self, _Name, _LeaguePoints, _Wins, _Losses, _EncrytedID):
        self.name = _Name
        self.lp = _LeaguePoints
        self.win = _Wins
        self.loss = _Losses
        self.id_Encryted = _EncrytedID


def findChampionName(champID):
    # json으로 읽어온 챔피언 리스트에서 입력받은 챔피언 ID값과 일치하는 챔피언 이름을 리턴한다.
    global Champion_List, recentData_Champion
    for string in Champion_List:
        if int(recentData_Champion['data'][string]['key']) == champID:
            return string

def drawChampionImage(champName, img_width, img_height):
    # url로 챔피언 이미지를 가져와 image 객체를 리턴한다.
    filepath = "http://ddragon.leagueoflegends.com/cdn/img/champion/loading/" + str(champName) + "_0.jpg"
    with urllib.request.urlopen(filepath) as url:
        rawData = url.read()
    imgData = Image.open(BytesIO(rawData))
    imgData_resize = imgData.resize((img_width, img_height))
    image = ImageTk.PhotoImage(imgData_resize)
    return image

class MainWindow:
    global newimg
    offset_x = 10
    offset_y = 10

    def MakeChampionLabels(self):
        # 이미지 리스트와 라벨 리스트를 형성하고 라벨 리스트에 라벨 객체들을 적절하게 생성한다.
        # 사이즈 조절 필요성이 있다. ##################################################
        self.LabelList = list()
        self.imageList = list()
        n_Champion = self.rotation_NumberOfChampions
        for idx in range(n_Champion):
            self.imageList.append(drawChampionImage(self.rotation_FileNameList[idx], 86, 200))
            self.LabelList.append(Label(self.RotationFrame, image=self.imageList[idx]))

        for idx in range(n_Champion):
            self.LabelList[idx].place(x=idx * 86, y=40)

    def ResetCanvas(self):
        # 검색 엔트리 초기화
        self.search_Entry.delete(0, len(self.search_Entry.get()))
        pass

    def __init__(self):

        self.mainWindow = Tk()
        self.mainWindow.resizable(False, False)
        self.mainWindow.geometry("1280x800+100+100")
        self.mainWindow.wm_iconbitmap('DNF.ico')
        self.mainWindow.title("useful")

        self.notebook = ttk.Notebook(self.mainWindow, width=1230, height=750)
        self.notebook.pack()

        self.tabFrame = Frame(self.mainWindow) # 이곳에 배치한다.
        self.notebook.add(self.tabFrame, text = "롤 전적검색")

        self.TopFrame = Frame(self.tabFrame)
        self.BottomFrame = Frame(self.tabFrame)

        self.TopFrame.pack(side="top")
        self.BottomFrame.pack(side="bottom")

        self.profileFrame = Frame(self.TopFrame, width = 640, height = 400, relief = "raised", bd = 5)
        self.RankingFrame = Frame(self.TopFrame, width = 640, height = 400, relief = "raised", bd = 5)
        self.RotationFrame = Frame(self.BottomFrame, width = 1280, height = 400, relief = "raised", bd = 5)
        self.profileFrame.pack(side="left", fill="both")
        self.RankingFrame.pack(side="top", fill="both")
        self.RotationFrame.pack(side="left", fill="both")

        ## frame 이름 라벨  #####################################################
        self.nameLabel_profile = Label(self.profileFrame, text = "Summoner Info.")
        self.nameLabel_profile.pack()
        self.nameLabel_profile.place(x = self.offset_x, y = self.offset_y + 40)

        self.nameLabel_ChampionRotation = Label(self.RotationFrame, text = "Champion Rotation")
        self.nameLabel_ChampionRotation.pack()
        self.nameLabel_ChampionRotation.place(x = self.offset_x, y = self.offset_y)

        self.nameLabel_Ranking = Label(self.RankingFrame, text="Ranking Top 5")
        self.nameLabel_Ranking.pack()
        self.nameLabel_Ranking.place(x=self.offset_x, y=self.offset_y)
        ########################################################################

        ## 로테이션 정보를 가져와 라벨을 생성하고 로테이션 챔피언 그림들을 라벨에 할당한다 #
        self.GetChampionRotation()
        self.MakeChampionLabels()

        ########################################################################
        ## 검색 엔트리, 검색 버튼, 리셋 버튼 #######################################

        self.search_Image = PhotoImage(file="search2.png").subsample(6, 6)
        self.search_Image_Label = Label(self.profileFrame, image=self.search_Image)
        self.search_Image_Label.grid(row = 2, column = 0)

        TempFont = Font(self.profileFrame, size=15, weight='bold', family='Consolas')

        self.search_Entry = Entry(self.profileFrame, font=TempFont, width=50, relief='ridge', borderwidth=5)
        self.search_Entry.grid(row = 2, column = 1)

        self.search_Button = Button(self.profileFrame, text="검색",
                                   command = lambda: self.SearchSummonerName(str(self.search_Entry.get())))
        self.search_Button.grid(row = 2, column = 2)

        self.search_ResetButton = Button(self.profileFrame, text="리셋", command=self.ResetCanvas)
        self.search_ResetButton.grid(row = 2, column = 3)


        self.info_Label_profileIcon = Label(self.profileFrame, relief = "sunken")
        self.info_Label_Name = Label(self.profileFrame, text = "")
        self.info_Label_profileIcon.place(x = 10, y= 70)
        self.info_Label_Name.place(x = 10 + 100 + 10, y= 70)

        #########################################################################

        self.mainWindow.mainloop()
        pass

    def SearchSummonerName(self, summonerName):
        global version_profileicon
        if (summonerName == ""):
            print("비어있는입력")
            return

        # 한글 -> utf-8 인코딩
        encText = urllib.parse.quote(summonerName)

        server = "kr.api.riotgames.com"
        apiKey = "RGAPI-354e7489-f932-4a39-90ab-24069b93c837"
        conn = http.client.HTTPSConnection(server)
        conn.request("GET",
                     "/lol/summoner/v4/summoners/by-name/" + encText + "?api_key=" + apiKey)

        request = conn.getresponse()
        print("First Searching Response Code:" + str(request.status))
        if int(request.status) == 200: # 정상 응답코드는 200
            response_body = request.read().decode('utf-8')
        jsonData = json.loads(response_body)
        print(jsonData)
        print("검색 소환사명:" + jsonData['name'])

        self.data_Search_Summoner = SummonerData(jsonData['name'], jsonData['id'], jsonData['accountId'], jsonData['profileIconId'], jsonData['summonerLevel'] )
        # 이름 출력
        self.info_Label_Name.config(text=self.data_Search_Summoner.name)
        # 레벨 출력
        # ..

        # 프로필 아이콘 출력
        filepath = "http://ddragon.leagueoflegends.com/cdn/"+version_profileicon+"/img/profileicon/" + str(self.data_Search_Summoner.id_Profile) + ".png"
        with urllib.request.urlopen(filepath) as url:
            rawData = url.read()
        imgData = Image.open(BytesIO(rawData))
        imgData_resize = imgData.resize((100, 100))
        self.profileIconImage = ImageTk.PhotoImage(imgData_resize)
        self.info_Label_profileIcon.config(image = self.profileIconImage, relief = "raised", bd = 3)

        # 리그 아이콘 출력


    def GetChampionRotation(self):
        # url과 api-key를 이용해서 챔피언 id 리스트를 가져옵니다.
        # 이를 통해 챔피언 이름 리스트(파일용으로 사용할 용도)를 생성합니다.
        self.rotation_FileNameList = list()
        self.rotation_IDList = list()
        self.rotation_NumberOfChampions = 0

        server = "kr.api.riotgames.com"
        apiKey = "RGAPI-354e7489-f932-4a39-90ab-24069b93c837"
        conn = http.client.HTTPSConnection(server)
        conn.request("GET",
                     "/lol/platform/v3/champion-rotations?api_key=" + apiKey)

        request = conn.getresponse()
        print("RotationChmps Response Code:" + str(request.status))
        if int(request.status) == 200:  # 정상 응답코드는 200
            response_body = request.read().decode('utf-8')
        jsonData = json.loads(response_body)
        self.rotation_IDList = jsonData["freeChampionIds"]

        for ID in self.rotation_IDList:
            self.rotation_FileNameList.append(findChampionName(ID))
        self.rotation_NumberOfChampions = len(self.rotation_FileNameList)
        print(self.rotation_FileNameList) # 검증 용도. 챔피언 리스트를 프린팅합니다.


object = MainWindow()

