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
            self.iconSize = (200, 200)
        else:
            self.iconSize = (100, 100)

        jsonData = parser.Get_API_Search_byName(self.name)
        self.id_Profile = jsonData['profileIconId']
        self.level = jsonData['summonerLevel']
        # 프로필 아이콘 이미지를 리턴g한다.
        image = parser.Get_ProfileIcon(version_profileicon, self.id_Profile, self.iconSize)
        return image


def findChampionName(champID):
    # json으로 읽어온 챔피언 리스트에서 입력받은 챔피언 ID값과 일치하는 챔피언 이름을 리턴한다.
    global Champion_List, recentData_Champion
    for string in Champion_List:
        if int(recentData_Champion['data'][string]['key']) == champID:
            return string


def Draw_rotation_images(champName, img_width, img_height):
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

    def Get_rankinginfo(self):
        # 랭킹 정보를 가져옵니다.
        jsonData = parser.Get_API_Challengerleagues()
        self.challenger_rankerlist_raw = jsonData['entries']
        for idx in range(len(self.challenger_rankerlist_raw)):
            self.challenger_rankerlist.append(RankingSummoner(self.challenger_rankerlist_raw[idx]['summonerName'], self.challenger_rankerlist_raw[idx]['leaguePoints'], self.challenger_rankerlist_raw[idx]['wins'], self.challenger_rankerlist_raw[idx]['losses'], self.challenger_rankerlist_raw[idx]['summonerId']))

    def Sort_rankinginfo(self):
        self.challenger_rankerlist = sorted(self.challenger_rankerlist, key = lambda val : val.lp, reverse = True) # 내림차순 정렬
        print("Sorting Complete")

    def Set_challenger_profileicon(self):
        cycle = 5 # 5 순위까지
        for idx in range(cycle):
            self.challenger_profileiconlist.append(self.challenger_rankerlist[idx].SetProfileIcon(idx))

    def ResetCanvas(self):
        self.isEmpty = True
        # 검색 엔트리 초기화

        self.search_Entry.delete(0, len(self.search_Entry.get()))
        filePath = "./lol_images/NoProfile.png"
        self.info_img_profileIcon = parser.Get_ImageFromFile(filePath, (100,100))
        self.info_Label_profileIcon.config(image = self.info_img_profileIcon, relief = "raised", bd = 3)

        pass

    def Set_challengers(self):
        # 랭킹 프레임 그리기
        ## 상위 랭커 5위 출력 #####################################################

        # 1위
        self.rank_Label_First_profileIcon = Label(self.main_canvas, image=self.challenger_profileiconlist[0],
                                                  relief="raised", bd=10, bg="black")
        self.rank_Label_First_Name = Label(self.main_canvas, text=self.challenger_rankerlist[0].name, bg="black", fg="white")
        self.rank_Label_First_Level = Label(self.main_canvas, text="Lv." + str(self.challenger_rankerlist[0].level), bg="black", fg="white")
        self.rank_Label_First_LeaguePoints = Label(self.main_canvas, text=str(self.challenger_rankerlist[0].lp) + " LP", bg="black", fg="white")
        self.rank_Label_First_WinRate = Label(self.main_canvas,
                                              text="{0}전 {1}승 {2}패 승률:{3:.1f}%".format(self.challenger_rankerlist[0].total,
                                                                                       self.challenger_rankerlist[0].win,
                                                                                       self.challenger_rankerlist[0].loss,
                                                                                       self.challenger_rankerlist[
                                                                                           0].win * 100 /
                                                                                       self.challenger_rankerlist[0].total), bg="black", fg="white")
        # 2위
        self.rank_Label_Second_profileIcon = Label(self.main_canvas, image=self.challenger_profileiconlist[1],
                                                   relief="raised", bd=5, bg="black")
        self.rank_Label_Second_Name = Label(self.main_canvas, text=self.challenger_rankerlist[1].name, bg="black", fg="white")
        self.rank_Label_Second_Level = Label(self.main_canvas, text="Lv." + str(self.challenger_rankerlist[1].level), bg="black", fg="white")
        self.rank_Label_Second_LeaguePoints = Label(self.main_canvas, text=str(self.challenger_rankerlist[1].lp) + " LP", bg="black", fg="white")
        self.rank_Label_Second_WinRate = Label(self.main_canvas,
                                               text="{0}전\n{1}승\n{2}패\n승률:{3:.1f}%".format(self.challenger_rankerlist[1].total,
                                                                                           self.challenger_rankerlist[1].win,
                                                                                           self.challenger_rankerlist[1].loss,
                                                                                           self.challenger_rankerlist[
                                                                                               1].win * 100 /
                                                                                           self.challenger_rankerlist[
                                                                                               1].total), bg="black", fg="white")
        # 3위
        self.rank_Label_Third_profileIcon = Label(self.main_canvas, image=self.challenger_profileiconlist[2],
                                                  relief="raised", bd=5, bg="black")
        self.rank_Label_Third_Name = Label(self.main_canvas, text=self.challenger_rankerlist[2].name, bg="black", fg="white")
        self.rank_Label_Third_Level = Label(self.main_canvas, text="Lv." + str(self.challenger_rankerlist[2].level), bg="black", fg="white")
        self.rank_Label_Third_LeaguePoints = Label(self.main_canvas, text=str(self.challenger_rankerlist[2].lp) + " LP", bg="black", fg="white")
        self.rank_Label_Third_WinRate = Label(self.main_canvas,
                                              text="{0}전\n{1}승\n{2}패\n승률:{3:.1f}%".format(self.challenger_rankerlist[2].total,
                                                                                          self.challenger_rankerlist[2].win,
                                                                                          self.challenger_rankerlist[2].loss,
                                                                                          self.challenger_rankerlist[
                                                                                              2].win * 100 /
                                                                                          self.challenger_rankerlist[2].total), bg="black", fg="white")
        # 4위
        self.rank_Label_Fourth_profileIcon = Label(self.main_canvas, image=self.challenger_profileiconlist[3],
                                                   relief="raised", bd=5, bg="black")
        self.rank_Label_Fourth_Name = Label(self.main_canvas, text=self.challenger_rankerlist[3].name, bg="black", fg="white")
        self.rank_Label_Fourth_Level = Label(self.main_canvas, text="Lv." + str(self.challenger_rankerlist[3].level), bg="black", fg="white")
        self.rank_Label_Fourth_LeaguePoints = Label(self.main_canvas, text=str(self.challenger_rankerlist[3].lp) + " LP", bg="black", fg="white")
        self.rank_Label_Fourth_WinRate = Label(self.main_canvas,
                                               text="{0}전\n{1}승\n{2}패\n승률:{3:.1f}%".format(self.challenger_rankerlist[3].total,
                                                                                           self.challenger_rankerlist[3].win,
                                                                                           self.challenger_rankerlist[3].loss,
                                                                                           self.challenger_rankerlist[
                                                                                               3].win * 100 /
                                                                                           self.challenger_rankerlist[
                                                                                               3].total), bg="black", fg="white")
        # 5위
        self.rank_Label_Fifth_profileIcon = Label(self.main_canvas, image=self.challenger_profileiconlist[4],
                                                  relief="raised", bd=5, bg="black")
        self.rank_Label_Fifth_Name = Label(self.main_canvas, text=self.challenger_rankerlist[4].name, bg="black", fg="white")
        self.rank_Label_Fifth_Level = Label(self.main_canvas, text="Lv." + str(self.challenger_rankerlist[4].level), bg="black", fg="white")
        self.rank_Label_Fifth_LeaguePoints = Label(self.main_canvas, text=str(self.challenger_rankerlist[4].lp) + " LP", bg="black", fg="white")
        self.rank_Label_Fifth_WinRate = Label(self.main_canvas,
                                              text="{0}전\n{1}승\n{2}패\n승률:{3:.1f}%".format(self.challenger_rankerlist[4].total,
                                                                                          self.challenger_rankerlist[4].win,
                                                                                          self.challenger_rankerlist[4].loss,
                                                                                          self.challenger_rankerlist[
                                                                                              4].win * 100 /
                                                                                          self.challenger_rankerlist[4].total), bg="black", fg="white")

        #########################################################################

    def Reset_Canvas(self):
        # 소환사 정보 출력부와 검색 엔트리를 초기화한다.
        pass

    def Button_SendEmail(self):
        # Gmail을 전송한다.
        pass

    ## 이벤트 함수 정의문 ####

    def Event_search_IN(self, event):
        self.label_search.configure(image = self.buttondrawer.img_label_search_over)
    def Event_search_OUT(self, event):
        self.label_search.configure(image = self.buttondrawer.img_label_search)
    def Event_search_CLICK(self, event):
        if self.main_animationflag:
            return
        self.search_animationflag = True
        self.frame = 0.0
        self.Disable_mainlabels()
        self.main_canvas.after(0, self.Animate_toSearch)
        print("\x1b[1;34mSearch Scene blend Start\x1b[0;m")

    def Event_search_searchIN(self, event):
        self.search_button_search.configure(image = self.buttondrawer.img_button_search_over_red)
    def Event_search_searchOUT(self, event):
        self.search_button_search.configure(image=self.buttondrawer.img_button_search)
    def Event_search_searchCLICK(self, event):
        #self.SearchSummonerName(self.search_entry.get())
        self.gif_animationflag = False
    def Event_search_resetIN(self, event):
        self.search_button_reset.configure(image = self.buttondrawer.img_button_reset_over_red)
    def Event_search_resetOUT(self, event):
        self.search_button_reset.configure(image = self.buttondrawer.img_button_reset)

    def Event_rotation_IN(self, event):
        self.label_rotation.configure(image = self.buttondrawer.img_label_rotation_over)
    def Event_rotation_OUT(self, event):
        self.label_rotation.configure(image = self.buttondrawer.img_label_rotation)
    def Event_rotation_CLICK(self, event):
        if self.main_animationflag:
            return
        self.rotation_animationflag = True
        self.frame = 0.0
        self.Disable_mainlabels()
        self.main_canvas.after(0, self.Animate_toRotation)
        print("\x1b[1;34mRotation Scene blend Start\x1b[0;m")

    def Event_challenger_IN(self, event):
        self.label_challenger.configure(image = self.buttondrawer.img_label_challenger_over)
    def Event_challenger_OUT(self, event):
        self.label_challenger.configure(image = self.buttondrawer.img_label_challenger)
    def Event_challenger_CLICK(self, event):
        if self.main_animationflag:
            return
        self.challenger_animationflag = True
        self.frame = 0.0
        self.Disable_mainlabels()
        self.main_canvas.after(0, self.Animate_toChallenger)
        print("\x1b[1;34mChallenger Scene blend Start\x1b[0;m")

    def Event_back_IN(self, event):
        self.label_back.configure(image = self.buttondrawer.img_label_back_over)
    def Event_back_OUT(self, event):
        self.label_back.configure(image=self.buttondrawer.img_label_back)
    def Event_back_CLICK(self, event):
        print("{0}, {1}".format(self.isAnimationing, self.challenger_isAnimationing))
        if self.isAnimationing:
            return
        elif self.challenger_isAnimationing:
            return
        self.main_canvas.delete('search')
        self.main_canvas.delete('challenger')
        self.Disable_searchscene()
        self.Disable_rotationscene()
        self.Disable_challengerscene()

        self.frame = 0.0
        self.gif_animationflag = False
        self.main_animationflag = True
        self.main_animationtype = _WHITE_OUT
        self.main_canvas.after(0, self.Animate_mainscene)
        print("\x1b[1;34mTo main Scene blend Start\x1b[0;m")

    def Event_tab_Click(self, event):
        clicked_tab = self.notebook.tk.call(self.notebook._w, "identify", "tab", event.x, event.y)
        if clicked_tab != 2: # 2번째 인덱스로 더해졌기 때문에
            self.gif_animationflag = False
            self.main_animationflag = False
            self.search_animationflag = False
            return
        if self.main_animationflag:
            return
        if self.search_animationflag:
            return

        self.main_canvas.delete('search')
        self.main_canvas.delete('challenger')
        self.Disable_searchscene()
        self.Disable_rotationscene()
        self.Disable_challengerscene()

        self.frame = 0.0
        self.main_animationflag = True
        self.main_animationtype = _WHITE_OUT
        self.Enable_mainlabels()
        self.main_canvas.after(0, self.Animate_mainscene)
        print("\x1b[1;34mLOL Scene blend Start\x1b[0;m")

    ########################

    ## 애니메이션 함수 정의문 ####

    def Animate_gif(self, in_counter):
        if not self.gif_animationflag:
            return

        self.search_button_search.update()
        self.main_canvas.itemconfig(self.background_gif, image=self.buttondrawer.img_sequence[in_counter])
        self.main_canvas.after(35, lambda: self.Animate_gif((in_counter + 1) % len(self.buttondrawer.img_sequence)))

    def Animate_toSearch(self):
        animSpeed = 2
        self.frame += 0.016 * animSpeed

        if math.floor(self.frame) == 0:
            self.main_background_blended = self.buttondrawer.Get_BlendedImageFromImages(self.buttondrawer.img_background,
                                                                                        self.buttondrawer.img_whitebackground,
                                                                                        self.frame - math.floor(self.frame))
        elif math.floor(self.frame) == 1:
            self.main_background_blended = self.buttondrawer.Get_BlendedImageFromImages(self.buttondrawer.img_whitebackground,
                                                                                        self.buttondrawer.img_background_transparent,
                                                                                        self.frame - math.floor(self.frame))
        else:
            self.main_background_blended = self.buttondrawer.img_background_transparent_raw
            self.search_animationflag = False

        self.main_canvas.delete("background")
        self.main_canvas.create_image(615, 375, image=self.main_background_blended, tags="background")

        if self.search_animationflag:
            self.main_canvas.after(16, self.Animate_toSearch)
        else:
            self.background_gif = self.main_canvas.create_image(1230 / 2, 750 / 2, image=self.buttondrawer.img_sequence[0])
            print("\x1b[1;34mSearch Scene blend Ended\x1b[0;m")
            self.Enable_searchscene()
            self.gif_animationflag = True
            self.Animate_gif(0)

    def Animate_toRotation(self):
        animSpeed = 2
        self.frame += 0.016 * animSpeed

        if math.floor(self.frame) == 0:
            self.main_background_blended = self.buttondrawer.Get_BlendedImageFromImages(
                self.buttondrawer.img_background,
                self.buttondrawer.img_whitebackground,
                self.frame - math.floor(self.frame))
        elif math.floor(self.frame) == 1:
            self.main_background_blended = self.buttondrawer.Get_BlendedImageFromImages(
                self.buttondrawer.img_whitebackground,
                self.buttondrawer.img_background_transparent,
                self.frame - math.floor(self.frame))
        else:
            self.main_background_blended = self.buttondrawer.img_background_transparent_raw
            self.rotation_animationflag = False

        self.main_canvas.delete("background")
        self.main_canvas.create_image(615, 375, image=self.main_background_blended, tags="background")

        if self.rotation_animationflag:
            self.main_canvas.after(16, self.Animate_toRotation)
        else:
            self.background_gif = self.main_canvas.create_image(1230 / 2, 750 / 2,
                                                                image=self.buttondrawer.img_sequence[0])
            print("\x1b[1;34mRotation Scene blend Ended\x1b[0;m")
            self.Enable_rotationscene()
            self.gif_animationflag = True
            self.Animate_gif(0)

    def Animate_toChallenger(self):
        animSpeed = 2
        self.frame += 0.016 * animSpeed

        if math.floor(self.frame) == 0:
            self.main_background_blended = self.buttondrawer.Get_BlendedImageFromImages(
                self.buttondrawer.img_background,
                self.buttondrawer.img_whitebackground,
                self.frame - math.floor(self.frame))
        elif math.floor(self.frame) == 1:
            self.main_background_blended = self.buttondrawer.Get_BlendedImageFromImages(
                self.buttondrawer.img_whitebackground,
                self.buttondrawer.img_background_transparent,
                self.frame - math.floor(self.frame))
        else:
            self.main_background_blended = self.buttondrawer.img_background_transparent_raw
            self.challenger_animationflag = False

        self.main_canvas.delete("background")
        self.main_canvas.create_image(615, 375, image=self.main_background_blended, tags="background")

        if self.challenger_animationflag:
            self.main_canvas.after(16, self.Animate_toChallenger)
        else:
            self.background_gif = self.main_canvas.create_image(1230 / 2, 750 / 2,
                                                                image=self.buttondrawer.img_sequence[0])
            print("\x1b[1;34mChallenger Scene blend Ended\x1b[0;m")
            self.Enable_challengerscene()
            self.gif_animationflag = False
            self.challenger_isAnimationing = True
            self.main_canvas.delete('challenger')
            self.Draw_ChallengerGraph()
            #self.gif_animationflag = True
            #self.Animate_gif(self.counter)


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

    ###########################

    def Enable_mainlabels(self):
        self.label_search.place(x=30, y=200)
        self.label_rotation.place(x=440, y=200)
        self.label_challenger.place(x=850, y=200)

    def Disable_mainlabels(self):
        self.label_search.place_forget()
        self.label_rotation.place_forget()
        self.label_challenger.place_forget()

    # 검색 씬
    def Enable_searchscene(self):
        self.label_back.place(x=50, y=50)

        # 검색 기능들
        self.search_entry.place(x=465, y=100, width = 300)
        self.search_button_search.place(x=780, y=105)
        self.search_button_reset.place(x=820, y=105)
        self.search_label_profileIcon.place(x=350, y=250)
        self.search_label_Emblem.place(x=350, y=420)
        self.search_label_Name.place(x=350+100+10, y=250)
        self.search_label_Level.place(x=350+100+10, y=270)
        self.search_label_WinRate.place(x=350+100+10, y=290)
        self.search_label_Queuetype.place(x=350+140+10, y=420)
        self.search_label_LeagueName.place(x=350+140+10, y=440)
        self.search_label_LeaguePoints.place(x=350+140+10, y=460)

    def Disable_searchscene(self):
        self.label_back.place_forget()

        # 검색 기능들
        self.search_entry.place_forget()
        self.search_button_search.place_forget()
        self.search_button_reset.place_forget()
        self.search_label_profileIcon.place_forget()
        self.search_label_Emblem.place_forget()
        self.search_label_Name.place_forget()
        self.search_label_Level.place_forget()
        self.search_label_WinRate.place_forget()
        self.search_label_Queuetype.place_forget()
        self.search_label_LeagueName.place_forget()
        self.search_label_LeaguePoints.place_forget()
    # 로테이션 씬
    def Enable_rotationscene(self):
        self.label_back.place(x=50, y=50)

        print(len(self.rotation_labellist))
        # 로테이션 라벨
        for idx in range(0, 7):
            self.rotation_labellist[idx].place(x = 24 + idx * 172, y = 275)
        for idx in range(7, 14):
            self.rotation_labellist[idx].place(x = 24 + (idx - 7) * 172, y = 500)
    def Disable_rotationscene(self):
        self.label_back.place_forget()

        # 로테이션 라벨
        for idx in range(0, 14):
            self.rotation_labellist[idx].place_forget()

    # 챌린져 씬
    def Enable_challengerscene(self):
        self.label_back.place(x=50, y=50)

        self.rank_Label_First_profileIcon.place(x=510, y=100)
        self.rank_Label_First_Name.place(x=510 + 220, y=100)
        self.rank_Label_First_Level.place(x=510 + 220, y=100+20)
        self.rank_Label_First_LeaguePoints.place(x=510 + 220, y=100+40)
        self.rank_Label_First_WinRate.place(x=510 + 220, y=100+60)

        self.rank_Label_Second_profileIcon.place(x=162, y=375)
        self.rank_Label_Second_Name.place(x=162+110, y=375)
        self.rank_Label_Second_Level.place(x=162+110, y=375+20)
        self.rank_Label_Second_LeaguePoints.place(x=162+110, y=375+40)
        self.rank_Label_Second_WinRate.place(x=162+110, y=375+60)

        self.rank_Label_Third_profileIcon.place(x=429, y=375)
        self.rank_Label_Third_Name.place(x=429+110, y=375)
        self.rank_Label_Third_Level.place(x=429+110, y=375+20)
        self.rank_Label_Third_LeaguePoints.place(x=429+110,y=375+40)
        self.rank_Label_Third_WinRate.place(x=429+110, y=375+60)

        self.rank_Label_Fourth_profileIcon.place(x=696, y=375)
        self.rank_Label_Fourth_Name.place(x=696+110, y=375)
        self.rank_Label_Fourth_Level.place(x=696+110, y=375+20)
        self.rank_Label_Fourth_LeaguePoints.place(x=696+110, y=375+40)
        self.rank_Label_Fourth_WinRate.place(x=696+110,y=375+60)

        self.rank_Label_Fifth_profileIcon.place(x=963, y=375)
        self.rank_Label_Fifth_Name.place(x=963+110, y=375)
        self.rank_Label_Fifth_Level.place(x=963+110, y=375+20)
        self.rank_Label_Fifth_LeaguePoints.place(x=963+110, y=375+40)
        self.rank_Label_Fifth_WinRate.place(x=963+110, y=375+60)
    def Disable_challengerscene(self):
        self.label_back.place_forget()

        self.rank_Label_First_profileIcon.place_forget()
        self.rank_Label_First_Name.place_forget()
        self.rank_Label_First_Level.place_forget()
        self.rank_Label_First_LeaguePoints.place_forget()
        self.rank_Label_First_WinRate.place_forget()

        self.rank_Label_Second_profileIcon.place_forget()
        self.rank_Label_Second_Name.place_forget()
        self.rank_Label_Second_Level.place_forget()
        self.rank_Label_Second_LeaguePoints.place_forget()
        self.rank_Label_Second_WinRate.place_forget()

        self.rank_Label_Third_profileIcon.place_forget()
        self.rank_Label_Third_Name.place_forget()
        self.rank_Label_Third_Level.place_forget()
        self.rank_Label_Third_LeaguePoints.place_forget()
        self.rank_Label_Third_WinRate.place_forget()

        self.rank_Label_Fourth_profileIcon.place_forget()
        self.rank_Label_Fourth_Name.place_forget()
        self.rank_Label_Fourth_Level.place_forget()
        self.rank_Label_Fourth_LeaguePoints.place_forget()
        self.rank_Label_Fourth_WinRate.place_forget()

        self.rank_Label_Fifth_profileIcon.place_forget()
        self.rank_Label_Fifth_Name.place_forget()
        self.rank_Label_Fifth_Level.place_forget()
        self.rank_Label_Fifth_LeaguePoints.place_forget()
        self.rank_Label_Fifth_WinRate.place_forget()

    def __init__(self, in_mainWindow, in_buttondrawer):
        global parser
        self.frame = 0.0
        self.counter = 0
        self.buttondrawer = in_buttondrawer

        # main frame
        self.main_frame = Frame(in_mainWindow.window)
        self.notebook = in_mainWindow.notebook
        self.notebook.add(self.main_frame, image = self.buttondrawer.img_tab_lol, text ="lol")
        self.notebook.bind("<Button-1>", self.Event_tab_Click)

        self.main_canvas = Canvas(self.main_frame, width = self.mainWidth, height = self.mainHeight, bd = 0, relief="raised")
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

        # sub scene gif animation
        self.gif_animationflag = False

        # back button
        self.label_back = Label(self.main_canvas, width = 50, height = 50, bd = 0, image = self.buttondrawer.img_label_back)
        self.label_back.bind("<Enter>", self.Event_back_IN)
        self.label_back.bind("<Leave>", self.Event_back_OUT)
        self.label_back.bind("<Button-1>", self.Event_back_CLICK)

        # rank 관련 변수 선언 ################
        self.challenger_rankerlist_raw = list()
        self.challenger_rankerlist = list()
        self.challenger_profileiconlist = list()
        self.challenger_animationflag = False
        self.challenger_isAnimationing = False

        self.Get_rankinginfo()
        self.Sort_rankinginfo()
        ####################################

        # rotation 관련 변수 선언 ############
        self.rotation_imagelist = list()
        self.rotation_labellist = [Label(self.main_canvas, width = 150, height = 200, bd = 0) for idx in range(0, 14)]
        self.rotation_animationflag = False

        self.Get_rotation()
        self.Set_rotation_labels()
        self.Set_challenger_profileicon()
        self.Set_challengers()
        ####################################

        # search 관련 변수 선언 ##############
        self.search_isEmpty = True
        self.search_animationflag = False
        TempFont = Font(self.main_canvas, size=15, weight='bold', family='나눔고딕')
        self.search_entry = Entry(self.main_canvas, font=TempFont, relief='solid', borderwidth=5)
        #self.search_button_search = Button(self.main_canvas, image=self.buttondrawer.img_button_search)
        self.search_button_search = Button(self.main_canvas, image = self.buttondrawer.img_button_search, command = lambda: self.SearchSummonerName(str(self.search_entry.get())))
        self.search_button_reset = Button(self.main_canvas, image = self.buttondrawer.img_button_reset)
        self.search_isClicked = False
        self.isAnimationing = False
        # 함수 바인딩
        self.search_button_search.bind("<Enter>", self.Event_search_searchIN)
        self.search_button_search.bind("<Leave>", self.Event_search_searchOUT)
        self.search_button_search.bind("<Button-1>", self.Event_search_searchCLICK)
        self.search_button_reset.bind("<Enter>", self.Event_search_resetIN)
        self.search_button_reset.bind("<Leave>", self.Event_search_resetOUT)

        self.search_label_profileIcon = Label(self.main_canvas, relief="sunken", bg = "black" , bd = 5)
        self.search_label_Emblem = Label(self.main_canvas, relief="sunken", bg="black", bd = 5)
        self.search_label_Name = Label(self.main_canvas, text="소환사 레벨:", bg = "black", fg = "white")
        self.search_label_Level = Label(self.main_canvas, text="소환사 레벨:", bg = "black", fg = "white")
        self.search_label_WinRate = Label(self.main_canvas, text="전 승 패", bg = "black", fg = "white")
        self.search_label_Queuetype = Label(self.main_canvas, text="큐 정보", bg = "black", fg = "white")
        self.search_label_LeagueName = Label(self.main_canvas, text="리그 정보", bg = "black", fg = "white")
        self.search_label_LeaguePoints = Label(self.main_canvas, text="LP", bg = "black", fg = "white")
        ####################################

    def SearchSummonerName(self, summonerName):
        global version_profileicon

        self.isEmpty = False
        self.main_canvas.delete('search')
        self.main_canvas.update()

        jsonData = parser.Get_API_Search_byName(summonerName)
        if jsonData == None:
            self.isEmpty = True
            self.gif_animationflag = True
            self.Animate_gif(self.counter)
            return
        #print(jsonData)
        #print("검색 소환사명:" + jsonData['name'])

        self.data_summoner_searched = SearchedSummoner(jsonData['name'], jsonData['id'], jsonData['accountId'], jsonData['profileIconId'], jsonData['summonerLevel'] )

        # 이름 출력
        self.search_label_Name.config(text=self.data_summoner_searched.name)
        # 레벨 출력
        self.search_label_Level.config(text="소환사 레벨: " + str(self.data_summoner_searched.level))
        # 전적 텍스트 출력
        if self.data_summoner_searched.isActive:
            self.search_label_WinRate.config(text = str(self.data_summoner_searched.total) + "전 " + str(self.data_summoner_searched.win) + "승 " + str(self.data_summoner_searched.loss) + "패 승률:" + "{0:.1f}%".format(self.data_summoner_searched.win * 100 / self.data_summoner_searched.total))
            self.search_label_Queuetype.config(text = self.data_summoner_searched.queue)
            self.search_label_LeagueName.config(text = self.data_summoner_searched.tier + " " + self.data_summoner_searched.rank)
            self.search_label_LeaguePoints.config(text = str(self.data_summoner_searched.lp) + " LP")
        else:
            self.search_label_WinRate.config(text="승률 정보 없음")
            self.search_label_Queuetype.config(text="큐 정보 없음")
            self.search_label_LeagueName.config(text="배치 리그 정보 없음")
            self.search_label_LeaguePoints.config(text="리그 포인트 정보 없음")
        # ..

        # 프로필 아이콘 출력
        self.search_img_profileicon = parser.Get_ProfileIcon(version_profileicon, self.data_summoner_searched.id_Profile, (100, 100))
        self.search_label_profileIcon.config(image = self.search_img_profileicon, relief = "raised", bd = 5)

        # 리그 아이콘 출력
        if self.data_summoner_searched.isActive:
            Emblemfilepath = "./lol_images/Emblem_" + str(self.data_summoner_searched.tier) + ".png"
        else:
            Emblemfilepath = "./lol_images/Emblem_" + "UNRANKED" + ".png"

        self.search_img_Emblem = parser.Get_ImageFromFile(Emblemfilepath, (140, 159))
        self.search_label_Emblem.config(image = self.search_img_Emblem, relief = "raised", bd = 5)

        if self.data_summoner_searched.isActive:
            self.isAnimationing = True
            self.DrawGraph()

        self.gif_animationflag = True
        self.Animate_gif(self.counter)

    def DrawGraph(self):
        self.WinRate = self.data_summoner_searched.win * 360 / self.data_summoner_searched.total
        self.LossRate = 360 - self.WinRate
        self.currWinRate = 0.0
        self.currLossRate = 0.0
        self.textWinRate = 0.0
        TempFont = Font(self.main_canvas, size=50, weight='bold', family='나눔고딕')
        while self.isAnimationing:

            if ((self.currWinRate < self.WinRate) & (self.currLossRate < self.LossRate)):
                time.sleep(0.0025)
                self.currWinRate += float(self.WinRate) * 0.0025
                self.currLossRate += float(self.LossRate) * 0.0025
                self.textWinRate = self.currWinRate
                self.main_canvas.delete('search')
            else:
                self.currWinRate = self.WinRate
                self.currLossRate = self.LossRate
                self.isAnimationing = False
                #self.currWinRate = 0.0
                #self.currLossRate = 0.0

            self.main_canvas.create_arc(700, 400, 1000, 700, start=0, extent=self.currWinRate, fill="RoyalBlue2",
                                        tags='search')
            self.main_canvas.create_arc(700, 400, 1000, 700, start=self.WinRate, extent=self.currLossRate, fill="red3",
                                        tags='search')

            self.main_canvas.create_text(880, 550, font=TempFont,text = str(int((self.textWinRate * 100) / 360)) + "%", fill='white', tags ='search')
            self.main_canvas.update()

    def Draw_ChallengerGraph(self):
        self.challenger_isTopAnimationing = True
        barWidth = 260
        barheight = 70
        self.c_WinRate = [self.challenger_rankerlist[idx].win * barWidth / self.challenger_rankerlist[idx].total for idx in range(1,5)]
        self.c_LossRate = [barWidth - self.c_WinRate[idx] for idx in range(0, 4)]
        self.c_currWinRate = [0.0 for x in range(0, 4)]
        self.c_currLossRate = [0.0 for x in range(0, 4)]
        self.c_textWinRate = [0.0 for x in range(0, 4)]
        self.c_isWinAnimationing =  [False for x in range(0,4)]

        print("{0},{1},{2},{3}".format(self.c_WinRate, self.c_LossRate, self.c_currWinRate, self.c_currLossRate))

        self.first_WinRate = self.challenger_rankerlist[0].win * 360 / self.challenger_rankerlist[0].total
        self.first_LossRate = 360 - self.first_WinRate
        self.first_currWinRate = 0.0
        self.first_currLossRate = 0.0
        self.first_textWinRate = 0.0

        while self.challenger_isAnimationing:
            time.sleep(0.025)
            if ((self.first_currWinRate < self.first_WinRate) & (self.first_currLossRate < self.first_LossRate)):

                self.first_currWinRate += float(self.first_WinRate) * 0.025
                self.first_currLossRate += float(self.first_LossRate) * 0.025
                self.first_textWinRate = self.first_currWinRate
                self.main_canvas.delete('challenger')
            else:
                self.challenger_isTopAnimationing = False
                self.first_currWinRate = self.first_WinRate
                self.first_currLossRate = self.first_LossRate
            if not self.challenger_isTopAnimationing:
                #self.main_canvas.delete('challenger')
                if not((self.c_WinRate[0] < self.c_currWinRate[0]) and(self.c_WinRate[1] < self.c_currWinRate[1]) and(self.c_WinRate[2] < self.c_currWinRate[2]) and(self.c_WinRate[3] < self.c_currWinRate[3])):
                    for idx in range(0,4):
                        if (self.c_WinRate[idx] > self.c_currWinRate[idx]):
                            self.c_currWinRate[idx] += self.c_WinRate[idx] * 0.025
                        elif (self.c_WinRate[idx] < self.c_currWinRate[idx]):
                            self.c_isWinAnimationing[idx] = True

                if not((self.c_LossRate[0] < self.c_currLossRate[0]) and (self.c_LossRate[1] < self.c_currLossRate[1]) and (self.c_LossRate[2] < self.c_currLossRate[2]) and (self.c_LossRate[3] < self.c_currLossRate[3])):
                    for idx in range(0, 4):
                        if (self.c_LossRate[idx] > self.c_currLossRate[idx]):
                            self.c_currLossRate[idx] += self.c_LossRate[idx] * 0.025

                if (self.c_WinRate[0] <= self.c_currWinRate[0]) and (self.c_WinRate[1] <= self.c_currWinRate[1]) and (self.c_WinRate[2] <= self.c_currWinRate[2]) and (self.c_WinRate[3] <= self.c_currWinRate[3]) and (self.c_LossRate[0] <= self.c_currLossRate[0]) and(self.c_LossRate[1] <= self.c_currLossRate[1]) and(self.c_LossRate[2] <= self.c_currLossRate[2]) and (self.c_LossRate[3] <= self.c_currLossRate[3]):
                    self.challenger_isAnimationing = False

            self.main_canvas.create_arc(740, 215, 890, 365, start=0, extent=self.first_currWinRate, fill="RoyalBlue2",
                                        tags='challenger')
            self.main_canvas.create_arc(740, 215, 890, 365, start=self.first_WinRate, extent=self.first_currLossRate, fill="IndianRed1",
                                        tags='challenger')
            for idx in range(0, 4):
                self.main_canvas.create_rectangle(85 + 267 * idx - 2, 510 - 5, 85 + 267 * idx + barWidth + 2, 510 + barheight +5, fill="black", tags="challenger")
                #self.main_canvas.create_rectangle(85 + 267 * idx, 510, 85 + 267 * idx + barWidth, 510 + barheight, fill = "red", tags="challenger")
                self.main_canvas.create_rectangle(85 + 267 * idx, 510, 85 + 267 * idx + self.c_currWinRate[idx], 510 + barheight, fill="DodgerBlue2", tags="challenger")
                self.main_canvas.create_rectangle(85 + 267 * idx + self.c_currWinRate[idx], 511,
                                                  85 + 267 * idx + self.c_currWinRate[idx] + self.c_currLossRate[idx], 580,
                                                  fill="firebrick1", tags="challenger")
            self.main_canvas.update()

        self.gif_animationflag = True
        self.Animate_gif(self.counter)

    def Get_rotation(self):
        # url과 api-key를 이용해서 챔피언 id 리스트를 가져온다.
        # 이를 통해 챔피언 이름 리스트(파일용으로 사용할 용도)를 생성한다.
        self.rotation_FileNameList = list()
        self.rotation_IDList = list()
        self.rotation_NumberOfChampions = 0

        jsonData = parser.Get_API_ChampionRotations()
        self.rotation_IDList = jsonData["freeChampionIds"]

        for ID in self.rotation_IDList:
            self.rotation_FileNameList.append(findChampionName(ID))
        self.rotation_NumberOfChampions = len(self.rotation_FileNameList)
        print(self.rotation_FileNameList)

    def Set_rotation_labels(self):
        n_Champion = self.rotation_NumberOfChampions
        for idx in range(n_Champion):
            self.rotation_imagelist.append(Draw_rotation_images(self.rotation_FileNameList[idx], 150, 200))

        for idx in range(0, 7):
            self.rotation_labellist[idx].configure(image = self.rotation_imagelist[idx])
        for idx in range(7, 14):
            self.rotation_labellist[idx].configure(image = self.rotation_imagelist[idx])

