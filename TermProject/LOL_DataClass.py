## importing Area ##
import json                 # json module importing
import urllib.request       #
import http.client          #
from PIL import Image, ImageTk

# 작성 중


class TopRanker:
    # 챌린저 리그 소환사 객체를 위한 정보 클래스
    def __init__(self, _Name, _LeaguePoints, _Wins, _Losses, _EncrytedID):
        self.name = _Name
        self.lp = int(_LeaguePoints)
        self.win = int(_Wins)
        self.loss = int(_Losses)
        self.id_Encryted = _EncrytedID
        self.total = self.win + self.loss

    def Set_ProfileIcon(self, idx):
        if idx == 0:
            # 최상위 랭커라면
            self.iconSize = (150, 150)
        else:
            self.iconSize = (60, 60)

        jsonData = self.parser.Get_API_Search_byName(self.name)

        self.id_Profile = jsonData['profileIconId']
        self.level = jsonData['summonerLevel']
        # 프로필 아이콘 이미지를 리턴합니다.
        image = self.parser.Get_ProfileIcon(version_profileicon, self.id_Profile, self.iconSize)
        return image

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

