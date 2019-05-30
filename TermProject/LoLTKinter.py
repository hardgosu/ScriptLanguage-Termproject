from tkinter import * # import tkinter
import urllib.request
from io import BytesIO
from PIL import Image, ImageTk
import json # import json module
import http.client
from tkinter.font import *
import time
import LOL_ParseJson

def URLtoJSONDecode(urlpath):
    # json 객체로 리턴하는 스태틱 함수
    return json.loads(urllib.request.urlopen(urlpath).read().decode('utf-8'))

#############################################################################################
# 사전 처리 부분 - 가장 먼저 실행되어야 한다.
# 현재 롤 클라이언트 버전을 확인하기 위해 데이터 드래곤 url의 한국서버 json 파일을 받아온다.
recentData_url = "https://ddragon.leagueoflegends.com/realms/kr.json"
data = URLtoJSONDecode(recentData_url)
version_champion = data["n"]["champion"]
version_profileicon = data["n"]["profileicon"]
version_language = data["l"]

recentData_Champion_url = "http://ddragon.leagueoflegends.com/cdn/" + version_champion + "/data/" + version_language + "/champion.json"
recentData_Champion = URLtoJSONDecode(recentData_Champion_url)
Champion_List = list(recentData_Champion['data'].keys()) # 현재 챔피언 리스트

server = "kr.api.riotgames.com"
apiKey = "RGAPI-354e7489-f932-4a39-90ab-24069b93c837"
parser = LOL_ParseJson.Parser(server, apiKey)
##############################################################################################

class SummonerData:
    # 검색한 소환사를 출력하기 위한 클래스
    global parser
    def __init__(self, _Name, _EncrytedID, _AccountID, _ProfileIconID, _SummonerLevel):
        self.name = _Name
        self.id_Encryted = _EncrytedID
        self.id_Account = _AccountID
        self.id_Profile = _ProfileIconID
        self.level = _SummonerLevel

        self.GetLeagueInfo()
        pass

    def GetLeagueInfo(self):
        data = parser.Get_API_League_ofSummoner(self.id_Encryted)
        self.isActive = data[0]
        #server = "kr.api.riotgames.com"
        #apiKey = "RGAPI-354e7489-f932-4a39-90ab-24069b93c837"
        #conn = http.client.HTTPSConnection(server)
        #conn.request("GET",
        #             "/lol/league/v4/entries/by-summoner/" + self.id_Encryted + "?api_key=" + apiKey)

        #request = conn.getresponse()
        #print("Summoner Info Response Code:" + str(request.status))
        #if int(request.status) == 200:  # 정상 응답코드는 200
        #    response_body = request.read().decode('utf-8')

        #if response_body == "[]":
        #    # 리그 정보가 없을 때
        #    print("검색된 소환사의 리그정보가 없습니다.")
        #    self.isActive = False
        #else:
        #    # 리그 정보가 있을 때
        #    jsonData = json.loads(response_body)[0]  # list에 0번 인덱스에 존재하기 때문에.
        #    print(jsonData)
        #    self.isActive = True
        if self.isActive:
            jsonData = data[1]
            self.win = int(jsonData['wins'])
            self.queue = jsonData['queueType']
            self.loss = int(jsonData['losses'])
            self.total = self.win + self.loss
            self.tier = jsonData['tier']
            self.rank = jsonData['rank']
            self.lp = jsonData['leaguePoints']
            self.id_League = jsonData['leagueId']



class RankingSummoner:
    global parser
    # 챌린저 리그 소환사 객체를 위한 정보 클래스
    def __init__(self, _Name, _LeaguePoints, _Wins, _Losses, _EncrytedID):
        self.name = _Name
        self.lp = int(_LeaguePoints)
        self.win = int(_Wins)
        self.loss = int(_Losses)
        self.id_Encryted = _EncrytedID
        self.total = self.win + self.loss

    def SetProfileIcon(self, idx):
        if idx == 0:
            self.iconSize = (150, 150)
        else:
            self.iconSize = (60, 60)

        {
        # 소환사 이름을 통해 프로필 아이콘 ID를 가져옵니다.
        #encText = urllib.parse.quote(self.name)
        #server = "kr.api.riotgames.com"
        #apiKey = "RGAPI-354e7489-f932-4a39-90ab-24069b93c837"
        #conn = http.client.HTTPSConnection(server)
        #conn.request("GET","/lol/summoner/v4/summoners/by-name/" + encText + "?api_key=" + apiKey)

        #request = conn.getresponse()
        #print("Top 5 Ranker Searching Response Code[{0}]:".format(idx) + str(request.status))
        #if int(request.status) == 200:  # 정상 응답코드는 200
        #    response_body = request.read().decode('utf-8')
        #jsonData = json.loads(response_body)
        }

        jsonData = parser.Get_API_Search_byName(self.name)

        self.id_Profile = jsonData['profileIconId']
        self.level = jsonData['summonerLevel']
        # 프로필 아이콘 이미지를 리턴합니다.
        image = parser.Get_ProfileIcon(version_profileicon, self.id_Profile, self.iconSize)
        {
        #filepath = "http://ddragon.leagueoflegends.com/cdn/" + version_profileicon + "/img/profileicon/" + str(
        #    self.id_Profile) + ".png"
        #with urllib.request.urlopen(filepath) as url:
        #    rawData = url.read()
        #imgData = Image.open(BytesIO(rawData))
        #imgData_resize = imgData.resize(self.iconSize)
        #image = ImageTk.PhotoImage(imgData_resize)
        }
        return image


def findChampionName(champID):
    # json으로 읽어온 챔피언 리스트에서 입력받은 챔피언 ID값과 일치하는 챔피언 이름을 리턴한다.
    global Champion_List, recentData_Champion
    for string in Champion_List:
        if int(recentData_Champion['data'][string]['key']) == champID:
            return string


def drawChampionImage(champName, img_width, img_height):
    # url로 챔피언 이미지를 가져와 image 객체를 리턴한다.
    global parser
    url = "http://ddragon.leagueoflegends.com/cdn/img/champion/loading/" + str(champName) + "_0.jpg"
    image = parser.Decode_ImagefromURL(url, (img_width, img_height))
    #with urllib.request.urlopen(filepath) as url:
    #    rawData = url.read()
    #imgData = Image.open(BytesIO(rawData))
    #imgData_resize = imgData.resize((img_width, img_height))
    #image = ImageTk.PhotoImage(imgData_resize)
    return image


class MainWindow:
    global parser
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

    def GetRankingInfo(self):
        # 랭킹 정보를 가져옵니다.
        {
        #server = "kr.api.riotgames.com"
        #apiKey = "RGAPI-354e7489-f932-4a39-90ab-24069b93c837"
        #conn = http.client.HTTPSConnection(server)
        #conn.request("GET",
        #             "/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + apiKey)
        #request = conn.getresponse()
        #print("Ranking Data Response Code:" + str(request.status))
        #if int(request.status) == 200:  # 정상 응답코드는 200
        #    response_body = request.read().decode('utf-8')
        #jsonData = json.loads(response_body)
        #print(jsonData)
        }
        jsonData = parser.Get_API_Challengerleagues()
        self.rawRankingList = jsonData['entries']
        for idx in range(len(self.rawRankingList)):
            self.TopRankingList.append(RankingSummoner(self.rawRankingList[idx]['summonerName'], self.rawRankingList[idx]['leaguePoints'], self.rawRankingList[idx]['wins'], self.rawRankingList[idx]['losses'], self.rawRankingList[idx]['summonerId']))

    def SortRankingInfo(self):
        self.TopRankingList = sorted(self.TopRankingList, key = lambda val : val.lp, reverse = True) # 내림차순 정렬
        print("Sorting Complete")

    def SetRankingProfileIcons(self):
        cycle = 5 # 5 순위까지
        for idx in range(cycle):
            self.rank_img_profileIcon.append(self.TopRankingList[idx].SetProfileIcon(idx))

    def ResetCanvas(self):
        self.isEmpty = True
        # 검색 엔트리 초기화

        self.search_Entry.delete(0, len(self.search_Entry.get()))
        filePath = "./lol_images/NoProfile.png"
        self.info_img_profileIcon = parser.Get_ImageFromFile(filePath, (100,100))
        self.info_Label_profileIcon.config(image = self.info_img_profileIcon, relief = "raised", bd = 3)

        pass

    def SendGmail(self):
        # gmail 보내기

        ## 미완성 #
        pass

    def DrawRanking(self):
        # 랭킹 프레임 그리기
        ## 상위 랭커 5위 출력 #####################################################

        # 1위
        self.rank_Label_First_profileIcon = Label(self.RankingFrame, image=self.rank_img_profileIcon[0],
                                                  relief="raised", bd=3)
        self.rank_Label_First_Name = Label(self.RankingFrame, text=self.TopRankingList[0].name)
        self.rank_Label_First_Level = Label(self.RankingFrame, text="Lv." + str(self.TopRankingList[0].level))
        self.rank_Label_First_LeaguePoints = Label(self.RankingFrame, text=str(self.TopRankingList[0].lp) + " LP")
        self.rank_Label_First_WinRate = Label(self.RankingFrame,
                                              text="{0}전 {1}승 {2}패 승률:{3:.1f}%".format(self.TopRankingList[0].total,
                                                                                       self.TopRankingList[0].win,
                                                                                       self.TopRankingList[0].loss,
                                                                                       self.TopRankingList[
                                                                                           0].win * 100 /
                                                                                       self.TopRankingList[0].total))
        # 2위
        self.rank_Label_Second_profileIcon = Label(self.RankingFrame, image=self.rank_img_profileIcon[1],
                                                   relief="raised", bd=3)
        self.rank_Label_Second_Name = Label(self.RankingFrame, text=self.TopRankingList[1].name)
        self.rank_Label_Second_Level = Label(self.RankingFrame, text="Lv." + str(self.TopRankingList[1].level))
        self.rank_Label_Second_LeaguePoints = Label(self.RankingFrame, text=str(self.TopRankingList[1].lp) + " LP")
        self.rank_Label_Second_WinRate = Label(self.RankingFrame,
                                               text="{0}전\n{1}승\n{2}패\n승률:{3:.1f}%".format(self.TopRankingList[1].total,
                                                                                           self.TopRankingList[1].win,
                                                                                           self.TopRankingList[1].loss,
                                                                                           self.TopRankingList[
                                                                                               1].win * 100 /
                                                                                           self.TopRankingList[
                                                                                               1].total))
        # 3위
        self.rank_Label_Third_profileIcon = Label(self.RankingFrame, image=self.rank_img_profileIcon[2],
                                                  relief="raised", bd=3)
        self.rank_Label_Third_Name = Label(self.RankingFrame, text=self.TopRankingList[2].name)
        self.rank_Label_Third_Level = Label(self.RankingFrame, text="Lv." + str(self.TopRankingList[2].level))
        self.rank_Label_Third_LeaguePoints = Label(self.RankingFrame, text=str(self.TopRankingList[2].lp) + " LP")
        self.rank_Label_Third_WinRate = Label(self.RankingFrame,
                                              text="{0}전\n{1}승\n{2}패\n승률:{3:.1f}%".format(self.TopRankingList[2].total,
                                                                                          self.TopRankingList[2].win,
                                                                                          self.TopRankingList[2].loss,
                                                                                          self.TopRankingList[
                                                                                              2].win * 100 /
                                                                                          self.TopRankingList[2].total))
        # 4위
        self.rank_Label_Fourth_profileIcon = Label(self.RankingFrame, image=self.rank_img_profileIcon[3],
                                                   relief="raised", bd=3)
        self.rank_Label_Fourth_Name = Label(self.RankingFrame, text=self.TopRankingList[3].name)
        self.rank_Label_Fourth_Level = Label(self.RankingFrame, text="Lv." + str(self.TopRankingList[3].level))
        self.rank_Label_Fourth_LeaguePoints = Label(self.RankingFrame, text=str(self.TopRankingList[3].lp) + " LP")
        self.rank_Label_Fourth_WinRate = Label(self.RankingFrame,
                                               text="{0}전\n{1}승\n{2}패\n승률:{3:.1f}%".format(self.TopRankingList[3].total,
                                                                                           self.TopRankingList[3].win,
                                                                                           self.TopRankingList[3].loss,
                                                                                           self.TopRankingList[
                                                                                               3].win * 100 /
                                                                                           self.TopRankingList[
                                                                                               3].total))
        # 5위
        self.rank_Label_Fifth_profileIcon = Label(self.RankingFrame, image=self.rank_img_profileIcon[4],
                                                  relief="raised", bd=3)
        self.rank_Label_Fifth_Name = Label(self.RankingFrame, text=self.TopRankingList[4].name)
        self.rank_Label_Fifth_Level = Label(self.RankingFrame, text="Lv." + str(self.TopRankingList[4].level))
        self.rank_Label_Fifth_LeaguePoints = Label(self.RankingFrame, text=str(self.TopRankingList[4].lp) + " LP")
        self.rank_Label_Fifth_WinRate = Label(self.RankingFrame,
                                              text="{0}전\n{1}승\n{2}패\n승률:{3:.1f}%".format(self.TopRankingList[4].total,
                                                                                          self.TopRankingList[4].win,
                                                                                          self.TopRankingList[4].loss,
                                                                                          self.TopRankingList[
                                                                                              4].win * 100 /
                                                                                          self.TopRankingList[4].total))

        self.rank_Label_First_profileIcon.place(x=320 - 150, y=20)
        self.rank_Label_First_Name.place(x=320 + 10, y=20)
        self.rank_Label_First_Level.place(x=320 + 10, y=40)
        self.rank_Label_First_LeaguePoints.place(x=320 + 10, y=60)
        self.rank_Label_First_WinRate.place(x=320 + 10, y=80)

        self.rank_Label_Second_profileIcon.place(x=0, y=190 + 40)
        self.rank_Label_Second_Name.place(x=70, y=190 + 20 + 20)
        self.rank_Label_Second_Level.place(x=70, y=190 + 20 + 40)
        self.rank_Label_Second_LeaguePoints.place(x=70, y=190 + 20 + 60)
        self.rank_Label_Second_WinRate.place(x=0, y=190 + 20 + 80 + 20)

        self.rank_Label_Third_profileIcon.place(x=100 + 50, y=190 + 40)
        self.rank_Label_Third_Name.place(x=100 + 120, y=190 + 20 + 20)
        self.rank_Label_Third_Level.place(x=100 + 120, y=190 + 20 + 40)
        self.rank_Label_Third_LeaguePoints.place(x=100 + 120, y=190 + 20 + 60)
        self.rank_Label_Third_WinRate.place(x=100 + 50, y=190 + 20 + 80 + 20)

        self.rank_Label_Fourth_profileIcon.place(x=300, y=190 + 40)
        self.rank_Label_Fourth_Name.place(x=100 + 270, y=190 + 20 + 20)
        self.rank_Label_Fourth_Level.place(x=100 + 270, y=190 + 20 + 40)
        self.rank_Label_Fourth_LeaguePoints.place(x=100 + 270, y=190 + 20 + 60)
        self.rank_Label_Fourth_WinRate.place(x=300, y=190 + 20 + 80 + 20)

        self.rank_Label_Fifth_profileIcon.place(x=450, y=190 + 40)
        self.rank_Label_Fifth_Name.place(x=100 + 420, y=190 + 20 + 20)
        self.rank_Label_Fifth_Level.place(x=100 + 420, y=190 + 20 + 40)
        self.rank_Label_Fifth_LeaguePoints.place(x=100 + 420, y=190 + 20 + 60)
        self.rank_Label_Fifth_WinRate.place(x=450, y=190 + 20 + 80 + 20)
        #########################################################################

    def __init__(self, in_mainWindow):
        global server, apiKey
        self.parser = LOL_ParseJson.Parser(server, apiKey)

        self.rawRankingList = list() # 가공 전 리스트
        self.TopRankingList = list() # 정렬용 리스트
        self.rank_img_profileIcon = list() # 프로필 아이콘 이미지 리스트

        self.isEmpty = True # 검색된 정보가 있는가?
        self.isAnimationing = True # 그래프 애니메이션 중인가?


        self.mainWindow = in_mainWindow
        #self.mainWindow.resizable(False, False)
        #self.mainWindow.geometry("1280x800+100+100")
        #self.mainWindow.wm_iconbitmap('DNF.ico')
        #self.mainWindow.title("useful")

        self.tabFrame = Frame(in_mainWindow.window)  # 이곳에 배치한다.
        self.notebook = in_mainWindow.notebook
        self.notebook.add(self.tabFrame, text = "롤 전적검색")

        self.TopFrame = Frame(self.tabFrame)
        self.BottomFrame = Frame(self.tabFrame)

        self.TopFrame.pack(side="top")
        self.BottomFrame.pack(side="bottom")

        self.profileFrame = Frame(self.TopFrame, width = 590, height = 400, relief = "raised", bd = 5)
        self.RankingFrame = Frame(self.TopFrame, width = 690, height = 400, relief = "raised", bd = 5)
        self.RotationFrame = Frame(self.BottomFrame, width = 1280, height = 400, relief = "raised", bd = 5)
        self.profileFrame.pack(side="left", fill="both")
        self.RankingFrame.pack(side="top", fill="both")
        self.RotationFrame.pack(side="left", fill="both")

        ## 캔버스 할당 ###########################################################
        self.info_Canvas = Canvas(self.profileFrame, width=200, height=200)
        self.info_Canvas.place(x=350, y=170)
        #########################################################################

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

        self.GetRankingInfo()
        self.SortRankingInfo()
        self.SetRankingProfileIcons()
        ########################################################################

        self.DrawRanking()


        ########################################################################
        ## 검색 엔트리, 검색 버튼, 리셋 버튼 #######################################

        self.search_Image = PhotoImage(file="search2.png").subsample(6, 6)
        self.search_Image_Label = Label(self.profileFrame, image=self.search_Image)
        self.search_Image_Label.place(x = 0, y = 0)

        TempFont = Font(self.profileFrame, size=15, weight='bold', family='Consolas')

        self.search_Entry = Entry(self.profileFrame, font=TempFont, width = 20, relief='ridge', borderwidth=5)
        self.search_Entry.place(x = 60, y = 5)

        self.search_Button = Button(self.profileFrame, text="검색",
                                   command = lambda: self.SearchSummonerName(str(self.search_Entry.get())), width = 5)
        self.search_Button.place(x = 60 + 200 + 25 + 10, y = 10)

        self.search_ResetButton = Button(self.profileFrame, text="리셋", command=self.ResetCanvas, width = 5)
        self.search_ResetButton.place(x = 60 + 200 + 75 + 10, y = 10)

        self.sendGmail_Button = Button(self.profileFrame, text="Gmail 전송",
                                       command = self.SendGmail, width = 10)
        self.sendGmail_Button.place(x = 640 - 150, y= 10)

        self.info_Label_profileIcon = Label(self.profileFrame, relief = "sunken")
        self.info_Label_Name = Label(self.profileFrame, text = "소환사 명")
        self.info_Label_Level = Label(self.profileFrame, text = "소환사 레벨:")
        self.info_Label_WinRate = Label(self.profileFrame, text = "전 승 패")
        self.info_Label_Emblem = Label(self.profileFrame, relief = "sunken")
        self.info_Label_Queuetype = Label(self.profileFrame, text = "큐 정보")
        self.info_Label_LeagueName = Label(self.profileFrame, text="리그 정보")
        self.info_Label_LeaguePoints = Label(self.profileFrame, text = "LP")


        self.info_Label_profileIcon.place(x = 10, y= 70)
        self.info_Label_Name.place(x = 10 + 100 + 10, y= 70)
        self.info_Label_Level.place(x = 10 + 100 + 10, y = 90)
        self.info_Label_WinRate.place(x= 10 + 100 + 10, y = 110)
        self.info_Label_Emblem.place(x = 10, y = 180)
        self.info_Label_Queuetype.place(x = 10 + 140, y = 180 + 20)
        self.info_Label_LeagueName.place(x= 10 + 140, y= 180 + 40)
        self.info_Label_LeaguePoints.place(x= 10 + 140, y= 180 + 60)

        #########################################################################


        pass

    def SearchSummonerName(self, summonerName):
        global version_profileicon

        #if (summonerName == ""):
        #    print("비어있는입력")
        #    return

        self.isEmpty = False
        self.info_Canvas.delete('info')

        # 한글 -> utf-8 인코딩
        #encText = urllib.parse.quote(summonerName)

        #server = "kr.api.riotgames.com"
        #apiKey = "RGAPI-354e7489-f932-4a39-90ab-24069b93c837"
        #conn = http.client.HTTPSConnection(server)
        #conn.request("GET",
        #             "/lol/summoner/v4/summoners/by-name/" + encText + "?api_key=" + apiKey)

        #request = conn.getresponse()
        #print("First Searching Response Code:" + str(request.status))
        #if int(request.status) == 200: # 정상 응답코드는 200
        #    response_body = request.read().decode('utf-8')
        #jsonData = json.loads(response_body)

        jsonData = self.parser.Get_API_Search_byName(summonerName)
        if jsonData == None:
            self.isEmpty = True
            return
        #print(jsonData)
        #print("검색 소환사명:" + jsonData['name'])

        self.data_summoner_searched = SummonerData(jsonData['name'], jsonData['id'], jsonData['accountId'], jsonData['profileIconId'], jsonData['summonerLevel'] )
        # 이름 출력
        self.info_Label_Name.config(text=self.data_summoner_searched.name)
        # 레벨 출력
        self.info_Label_Level.config(text="소환사 레벨: " + str(self.data_summoner_searched.level))
        # 전적 텍스트 출력
        if self.data_summoner_searched.isActive:
            self.info_Label_WinRate.config(text = str(self.data_summoner_searched.total) + "전 " + str(self.data_summoner_searched.win) + "승 " + str(self.data_summoner_searched.loss) + "패 승률:" + "{0:.1f}%".format(self.data_summoner_searched.win * 100 / self.data_summoner_searched.total))
            self.info_Label_Queuetype.config(text = self.data_summoner_searched.queue)
            self.info_Label_LeagueName.config(text = self.data_summoner_searched.tier + " " + self.data_summoner_searched.rank)
            self.info_Label_LeaguePoints.config(text = str(self.data_summoner_searched.lp) + " LP")
        else:
            self.info_Label_WinRate.config(text="승률 정보 없음")
            self.info_Label_Queuetype.config(text="큐 정보 없음")
            self.info_Label_LeagueName.config(text="배치 리그 정보 없음")
            self.info_Label_LeaguePoints.config(text="리그 포인트 정보 없음")
        # ..

        # 프로필 아이콘 출력
        #filepath = "http://ddragon.leagueoflegends.com/cdn/"+version_profileicon+"/img/profileicon/" + str(self.data_summoner_searched.id_Profile) + ".png"
        #with urllib.request.urlopen(filepath) as url:
        #    rawData = url.read()
        #imgData = Image.open(BytesIO(rawData))
        #imgData_resize = imgData.resize((100, 100))
        #self.img_profileIcon = ImageTk.PhotoImage(imgData_resize)
        self.info_img_profileIcon = parser.Get_ProfileIcon(version_profileicon, self.data_summoner_searched.id_Profile, (100,100))
        self.info_Label_profileIcon.config(image = self.info_img_profileIcon, relief = "raised", bd = 3)

        # 리그 아이콘 출력
        if self.data_summoner_searched.isActive:
            Emblemfilepath = "./lol_images/Emblem_" + str(self.data_summoner_searched.tier) + ".png"
        else:
            Emblemfilepath = "./lol_images/Emblem_" + "UNRANKED" + ".png"
        #imgData = Image.open(Emblemfilepath)
        #imgData_resize = imgData.resize((140, 159))
        #self.img_Emblem = ImageTk.PhotoImage(imgData_resize)
        self.img_Emblem = parser.Get_ImageFromFile(Emblemfilepath, (140, 159))
        self.info_Label_Emblem.config(image = self.img_Emblem, relief = "flat")

        if self.data_summoner_searched.isActive:
            self.isAnimationing = True
            self.DrawGraph()

    def DrawGraph(self):
        self.WinRate = self.data_summoner_searched.win * 360 / self.data_summoner_searched.total
        self.LossRate = 360 - self.WinRate
        self.currWinRate = 0.0
        self.currLossRate = 0.0
        while self.isAnimationing:
            self.info_Canvas.create_arc(5, 5, 195, 195, start=0, extent=self.currWinRate, fill="RoyalBlue2",
                                        tags='info')
            self.info_Canvas.create_arc(5, 5, 195, 195, start=self.WinRate, extent=self.currLossRate, fill="red3",
                                        tags='info')
            self.info_Canvas.create_oval(65, 65, 135, 135, fill="white", width=0, tags='info')
            self.info_Canvas.update()
            if ((self.currWinRate < self.WinRate) & (self.currLossRate < self.LossRate)):
                time.sleep(0.0025)
                self.currWinRate += float(self.WinRate) * 0.0025
                self.currLossRate += float(self.LossRate) * 0.0025
                self.info_Canvas.delete('info')
            else:
                self.currWinRate = self.WinRate
                self.currLossRate = self.LossRate
                self.isAnimationing = False
                self.currWinRate = 0.0
                self.currLossRate = 0.0


    def GetChampionRotation(self):
        # url과 api-key를 이용해서 챔피언 id 리스트를 가져옵니다.
        # 이를 통해 챔피언 이름 리스트(파일용으로 사용할 용도)를 생성합니다.
        self.rotation_FileNameList = list()
        self.rotation_IDList = list()
        self.rotation_NumberOfChampions = 0

        jsonData = parser.Get_API_ChampionRotations()

        #server = "kr.api.riotgames.com"
        #apiKey = "RGAPI-354e7489-f932-4a39-90ab-24069b93c837"
        #conn = http.client.HTTPSConnection(server)
        #conn.request("GET",
        #             "/lol/platform/v3/champion-rotations?api_key=" + apiKey)

        #request = conn.getresponse()
        #print("RotationChmps Response Code:" + str(request.status))
        #if int(request.status) == 200:  # 정상 응답코드는 200
        #    response_body = request.read().decode('utf-8')
        #jsonData = json.loads(response_body)
        self.rotation_IDList = jsonData["freeChampionIds"]

        for ID in self.rotation_IDList:
            self.rotation_FileNameList.append(findChampionName(ID))
        self.rotation_NumberOfChampions = len(self.rotation_FileNameList)
        print(self.rotation_FileNameList) # 검증 용도. 챔피언 리스트를 프린팅합니다.

