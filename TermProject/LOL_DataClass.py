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