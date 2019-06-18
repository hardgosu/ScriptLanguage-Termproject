from tkinter import * # import tkinter
import urllib.request
import json # import json module
from tkinter.font import *
import time
import math

import LOL_Parse

#############################################################################################
# 사전 처리 부분 - 가장 먼저 실행되어야 한다.
server = "kr.api.riotgames.com"
apiKey = "RGAPI-354e7489-f932-4a39-90ab-24069b93c837"
# 파서 객체 생성, apikey와 server는 정해져 있다.
parser = LOL_Parse.Parser(server, apiKey)

# 현재 롤 클라이언트 버전을 확인하기 위해 데이터 드래곤 url의 한국서버 json 파일을 받아온다.
recentData_url = "https://ddragon.leagueoflegends.com/realms/kr.json"
data = parser.Decode_URLtoJson(recentData_url)
version_champion = data["n"]["champion"]
version_profileicon = data["n"]["profileicon"]
version_language = data["l"]

recentData_Champion_url = "http://ddragon.leagueoflegends.com/cdn/" + version_champion + "/data/" + version_language + "/champion.json"
recentData_Champion = parser.Decode_URLtoJson(recentData_Champion_url)
Champion_List = list(recentData_Champion['data'].keys())
##############################################################################################

_WHITE_IN   = 1
_WHITE_OUT  = 2
_BLACK_IN   = 3
_BLACK_OUT  = 4

class SearchedSummoner:
    # 검색한 소환사를 출력하기 위한 클래스
    global parser
    def __init__(self, _Name, _EncrytedID, _AccountID, _ProfileIconID, _SummonerLevel):
        self.name = _Name
        self.id_Encryted = _EncrytedID
        self.id_Account = _AccountID
        self.id_Profile = _ProfileIconID
        self.level = _SummonerLevel

        self.GetLeagueInfo()

    def GetLeagueInfo(self):
        data = parser.Get_API_League_ofSummoner(self.id_Encryted)
        self.isActive = data[0]
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

        jsonData = parser.Get_API_Search_byName(self.name)

        self.id_Profile = jsonData['profileIconId']
        self.level = jsonData['summonerLevel']
        # 프로필 아이콘 이미지를 리턴합니다.
        image = parser.Get_ProfileIcon(version_profileicon, self.id_Profile, self.iconSize)

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
    return image


class MainWindow:
    global parser, _WHITE_IN, _WHITE_OUT, _BLACK_IN, _BLACK_OUT
    mainWidth = 1230
    mainHeight = 750
    offset_x = 10
    offset_y = 10

    def ResetSearchData(self):
        pass

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

    def Button_ResetCanvas(self):
        # 소환사 정보 출력부와 검색 엔트리를 초기화한다.
        pass

    def Button_SendEmail(self):
        # Gmail을 전송한다.
        pass

    def Button_OpenSearchFrame(self):
        # 검색창 프레임을 활성화한다.
        pass

    def Button_OpenRotationInfo(self):
        # 챔피언 로테이션창 프레임을 활성화한다.
        pass

    def Button_OpenRankingInfo(self):
        # 랭킹 정보창 프레임을 활성화한다.
        pass

    ## 이벤트 함수 정의문 ####

    def Event_search_IN(self, event):
        self.label_search.configure(image = self.buttondrawer.img_label_search_over)
    def Event_search_OUT(self, event):
        self.label_search.configure(image = self.buttondrawer.img_label_search)
    def Event_search_CLICK(self, event):
        pass
    def Event_rotation_IN(self, event):
        self.label_rotation.configure(image = self.buttondrawer.img_label_rotation_over)
    def Event_rotation_OUT(self, event):
        self.label_rotation.configure(image = self.buttondrawer.img_label_rotation)
    def Event_rotation_CLICK(self, event):
        pass
    def Event_challenger_IN(self, event):
        self.label_challenger.configure(image = self.buttondrawer.img_label_challenger_over)
    def Event_challenger_OUT(self, event):
        self.label_challenger.configure(image = self.buttondrawer.img_label_challenger)
    def Event_challenger_CLICK(self, event):
        pass

    def Event_tab_Click(self, event):
        clicked_tab = self.notebook.tk.call(self.notebook._w, "identify", "tab", event.x, event.y)
        if clicked_tab != 2: # 2번째 인덱스로 더해졌기 때문에
            return
        if self.main_animationflag:
            return

        self.frame = 0.0
        self.main_animationflag = True
        self.main_animationtype = _WHITE_OUT
        self.main_canvas.after(0, self.Animate_mainscene)
        print("\x1b[1;34mLOL Scene blend Start\x1b[0;m")

    ########################

    ## 애니메이션 함수 정의문 ####

    def Animate_mainscene(self):
        animSpeed = 5
        self.frame += 0.016 * animSpeed

        if self.main_animationtype == _BLACK_OUT:
            self.Animate_blackout()
        elif self.main_animationtype == _BLACK_IN:
            self.Animate_blackin()
        elif self.main_animationtype == _WHITE_IN:
            self.Animate_whitein()
        elif self.main_animationtype == _WHITE_OUT:
            self.Animate_whiteout()

        self.main_canvas.delete("background")
        self.main_canvas.create_image(615, 375, image = self.main_background_blended, tags="background")
        if self.main_animationflag:
            self.main_canvas.after(16, self.Animate_mainscene)
        else:
            print("\x1b[1;34mLOL Scene blend Ended\x1b[0;m")
            self.Enable_mainlabels()

    def Animate_whitein(self):
        if math.floor(self.frame) <= 2:
            self.main_background_blended = self.buttondrawer.Get_BlendedImageFromImages(self.buttondrawer.img_background,
                                                                                        self.buttondrawer.img_whitebackground,
                                                                                        self.frame/3.0)
        else:
            self.main_background_blended = self.buttondrawer.img_background_raw
            self.main_animationflag = False

    def Animate_whiteout(self):
        #
        if math.floor(self.frame) <= 2:
            self.main_background_blended = self.buttondrawer.Get_BlendedImageFromImages(self.buttondrawer.img_whitebackground,
                                                                                        self.buttondrawer.img_background,
                                                                                        self.frame/3.0)
        else:
            self.main_background_blended = self.buttondrawer.img_background_raw
            self.main_animationflag = False

    def Animate_blackin(self):
        if math.floor(self.frame) <= 2:
            self.main_background_blended = self.buttondrawer.Get_BlendedImageFromImages(self.buttondrawer.img_background,
                                                                                        self.buttondrawer.img_blackbackground,
                                                                                        self.frame/3.0)
        else:
            self.main_background_blended = self.buttondrawer.img_blackbackground_raw
            self.main_animationflag = False

    def Animate_blackout(self):
        if math.floor(self.frame) <= 2:
            self.main_background_blended = self.buttondrawer.Get_BlendedImageFromImages(self.buttondrawer.img_background,
                                                                                        self.buttondrawer.img_blackbackground,
                                                                                        self.frame/3.0)
        else:
            self.main_background_blended = self.buttondrawer.img_blackbackground_raw
            self.main_animationflag = False

    def Animate_lolscene(self):
        pass

    ###########################

    def Enable_mainlabels(self):
        self.label_search.place(x=30, y=200)
        self.label_rotation.place(x=440, y=200)
        self.label_challenger.place(x=850, y=200)

    def Disable_mainlabels(self):
        self.label_search.place_forget()
        self.label_rotation.place_forget()
        self.label_challenger.place_forget()

    def __init__(self, in_mainWindow, in_buttondrawer):
        global parser
        self.frame = 0.0
        self.buttondrawer = in_buttondrawer

        # main frame
        self.main_frame = Frame(in_mainWindow.window)
        self.notebook = in_mainWindow.notebook
        self.notebook.add(self.main_frame, image = self.buttondrawer.img_tab_lol, text ="lol")
        self.notebook.bind("<Button-1>", self.Event_tab_Click)

        self.main_canvas = Canvas(self.main_frame, width = self.mainWidth, height = self.mainHeight, bd = 0, relief="raised")
        #in_mainWindow.window.wm_attributes("-transparentcolor", "SystemButtonFace")
        self.main_canvas.place(x=0, y=0)
        self.main_canvas.create_image(615, 375, image = self.buttondrawer.img_blackbackground_raw, tags = "background")
        # Main Scene label
        self.label_search = Label(self.main_canvas, width = 350, height = 350, bd = 0, image = self.buttondrawer.img_label_search)
        self.label_rotation = Label(self.main_canvas, width = 350, height = 350, bd = 0, image = self.buttondrawer.img_label_rotation)
        self.label_challenger = Label(self.main_canvas, width = 350, height = 350, bd = 0, image = self.buttondrawer.img_label_challenger)

        self.Enable_mainlabels()

        # 이벤트 함수 바인딩
        self.label_search.bind("<Enter>", self.Event_search_IN)
        self.label_search.bind("<Leave>", self.Event_search_OUT)
        self.label_search.bind("<Button-1>", self.Event_search_CLICK)
        self.label_rotation.bind("<Enter>", self.Event_rotation_IN)
        self.label_rotation.bind("<Leave>", self.Event_rotation_OUT)
        self.label_rotation.bind("<Button-1>", self.Event_rotation_CLICK)
        self.label_challenger.bind("<Enter>", self.Event_challenger_IN)
        self.label_challenger.bind("<Leave>", self.Event_challenger_OUT)
        self.label_challenger.bind("<Button-1>", self.Event_challenger_CLICK)

        # main scene 관련 변수 선언
        self.main_animationflag = False
        self.main_animationtype = 0

        # rank 관련 변수 선언
        self.data_rank_rankerlist_raw = list()
        self.data_rank_rankerlist = list()
        self.data_challenger_profileiconlist = list()
        self.challenger_animationflag = False
        self.challenger_frame = Frame(self.main_frame)

        # rotation 관련 변수 선언
        self.data_rotation_imagelist = list()

        # search 관련 변수 선언
        self.search_isEmpty = True
        self.search_animationflag = False




    def SearchSummonerName(self, summonerName):
        global version_profileicon

        self.isEmpty = False
        self.info_Canvas.delete('info')
        self.info_Canvas.update()

        jsonData = parser.Get_API_Search_byName(summonerName)
        if jsonData == None:
            self.isEmpty = True
            return
        #print(jsonData)
        #print("검색 소환사명:" + jsonData['name'])

        self.data_summoner_searched = SearchedSummoner(jsonData['name'], jsonData['id'], jsonData['accountId'], jsonData['profileIconId'], jsonData['summonerLevel'] )
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
        self.info_img_profileIcon = parser.Get_ProfileIcon(version_profileicon, self.data_summoner_searched.id_Profile, (100,100))
        self.info_Label_profileIcon.config(image = self.info_img_profileIcon, relief = "raised", bd = 3)

        # 리그 아이콘 출력
        if self.data_summoner_searched.isActive:
            Emblemfilepath = "./lol_images/Emblem_" + str(self.data_summoner_searched.tier) + ".png"
        else:
            Emblemfilepath = "./lol_images/Emblem_" + "UNRANKED" + ".png"

        self.img_Emblem = parser.Get_ImageFromFile(Emblemfilepath, (140, 159))
        self.info_Label_Emblem.config(image = self.img_Emblem, relief = "flat")
        self.info_Canvas.create_image(200, 200, image=self.background)

        if self.data_summoner_searched.isActive:
            self.isAnimationing = True
            self.DrawGraph()

    def DrawGraph(self):
        self.WinRate = self.data_summoner_searched.win * 360 / self.data_summoner_searched.total
        self.LossRate = 360 - self.WinRate
        self.currWinRate = 0.0
        self.currLossRate = 0.0
        while self.isAnimationing:

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

            self.info_Canvas.create_arc(5, 5, 195, 195, start=0, extent=self.currWinRate, fill="RoyalBlue2",
                                        tags='info')
            self.info_Canvas.create_arc(5, 5, 195, 195, start=self.WinRate, extent=self.currLossRate, fill="red3",
                                        tags='info')
            self.info_Canvas.create_oval(65, 65, 135, 135, fill="white", width=0, tags='info')
            self.info_Canvas.update()

    def GetChampionRotation(self):
        # url과 api-key를 이용해서 챔피언 id 리스트를 가져옵니다.
        # 이를 통해 챔피언 이름 리스트(파일용으로 사용할 용도)를 생성합니다.
        self.rotation_FileNameList = list()
        self.rotation_IDList = list()
        self.rotation_NumberOfChampions = 0

        jsonData = parser.Get_API_ChampionRotations()
        self.rotation_IDList = jsonData["freeChampionIds"]

        for ID in self.rotation_IDList:
            self.rotation_FileNameList.append(findChampionName(ID))
        self.rotation_NumberOfChampions = len(self.rotation_FileNameList)
        print(self.rotation_FileNameList)

