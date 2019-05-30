## importing Area ##
import json                     # module for json parsing
import urllib.request           # module about url
import http.client              # module for http connection
from PIL import ImageTk, Image  # modules for Pillow Image
from io import BytesIO          # module for Byte Input


####################################################################################
## Class Definition ##
class Parser:
    # URL 주소를 통해 JSON을 파싱하거나 URL과 LOL-API를 통해 가져온 JSON 객체를 파싱하여 리턴하는 역할을 수행한다.

    def __init__(self, in_server = "", in_apiKey= ""):
        self.isAlive = True

        if in_server == "" or in_apiKey == "":
            # 예외처리 - server 와 apikey 입력이 이루어지지 않았다.
            print("Error has Occured : [\"Vacant server or apiKey\"]")
            self.isAlive = False
        else:
            # 정상 입력이라면 서버, apikey, 서버연결을 객체 변수로 저장한다.
            self.server = in_server
            self.apiKey = in_apiKey
            self.conn = http.client.HTTPSConnection(self.server)

    def Print_Errors(self, in_errorText = ""):
        # 에러 입력을 출력한다.
        print("Processing Error : [{0}]".format(in_errorText))

    def Print_ResponseCode(self, in_FuncName, in_number):
        # API가 보내온 응답 코드를 출력한다.
        # 200이 일반적인 정상응답이다.
        print("■[{0}] Response Code:{1}".format(in_FuncName, in_number))

    def Check_Validation(self, in_errorCode = ""):
        # 파서가 활성화 되었는가? - 파서가 수행하는 일반 메서드들의 첫 부분에 들어간다.
        if self.isAlive:
            return True
        else:
            print("Error has Occured : [\"The Parser is NOT active\"]\n[RETURNED AT::{0}]".format(in_errorCode))
            return False

    def Decode_URLtoJson(self, in_url):
        # URL에 요청해서 받은 Json을 파싱하여 리턴한다.

        local_url = in_url
        return json.loads(urllib.request.urlopen(local_url).read().decode('utf-8'))

    def Decode_ResponseToJson(self, in_response):
        # API 응답을 디코딩 후 Json으로 파싱하여 리턴한다.
        return json.loads(in_response.read().decode('utf-8'))

    def Decode_ImagefromURL(self, in_url, in_imgSize = tuple()):
        # URL로부터 얻은 이미지를 반환한다.
        with urllib.request.urlopen(in_url) as url:
            rawData = url.read()
        imgData = Image.open(BytesIO(rawData))
        imgData_resize = imgData.resize(in_imgSize)
        image = ImageTk.PhotoImage(imgData_resize)
        return image

    def Encode_Text(self, in_text):
        # URL에 사용할 일반 텍스트를 인코딩하여 리턴한다.
        encText = urllib.parse.quote(in_text)
        return encText

    def Get_API_Search_byName(self, in_summonerName):
        # 스트링으로 받은 in_SummonerName을 Encoding 하여 관련 정보를 리턴한다.

        if not self.Check_Validation("summoners/by-name/"):
            return

        if in_summonerName == "":
            self.Print_Errors("Empty input")
            return

        encText = self.Encode_Text(in_summonerName)

        self.conn.request("GET", "/lol/summoner/v4/summoners/by-name/" + encText + "?api_key=" + self.apiKey)
        request = self.conn.getresponse()
        self.Print_ResponseCode("Summoner/by-name", request.status)
        if int(request.status) == 200:
            return self.Decode_ResponseToJson(request)
        else:
            self.Print_Errors("Bad Response")
            return

    def Get_ProfileIcon(self, in_version_profileIcon = str(), in_id_profileIcon = -1, in_imgSize = tuple()):
        # 입력받은 id 값에 매칭되는 프로필 아이콘을 URL로부터 가져와 이미지를 리턴한다.
        if in_version_profileIcon == "":
            self.Print_Errors("Version Error")
            return

        if in_imgSize == ():
            self.Print_Errors("Empty size")
            return

        if in_id_profileIcon == -1:
            self.Print_Errors("Invalid profileID")
            return

        url = "http://ddragon.leagueoflegends.com/cdn/" + in_version_profileIcon + "/img/profileicon/" + str(in_id_profileIcon) + ".png"
        image = self.Decode_ImagefromURL(url, in_imgSize)
        if image:
            return image
        else:
            self.Print_Errors("Profile Image Loading Failure")
            return

    def Get_ImageFromFile(self, in_filePath = "", in_ImgSize = tuple()):
        # 파일 경로에 저장되어 있는 이미지를 읽어와 리턴한다.
        if in_filePath == "":
            self.Print_Errors("Empty FilePath")
            return

        if in_ImgSize == ():
            self.Print_Errors("Empty size")
            return

        imgData = Image.open(in_filePath)
        imgData_resize = imgData.resize(in_ImgSize)
        image = ImageTk.PhotoImage(imgData_resize)
        if image:
            return image
        else:
            self.Print_Errors("Image Loading Failure")
            return

    def Get_API_ChampionRotations(self):
        # 현재 서버의 챔피언 로테이션 ID 값을 리스트로 반환한다.

        if not self.Check_Validation("ChampionRotations"):
            return

        self.conn.request("GET", "/lol/platform/v3/champion-rotations?api_key=" + self.apiKey)
        request = self.conn.getresponse()
        self.Print_ResponseCode("champion-rotations", request.status)
        if int(request.status) == 200:
            return self.Decode_ResponseToJson(request)
        else:
            self.Print_Errors("Bad Response")
            return

    def Get_API_Challengerleagues(self):
        # 챌린저 랭커들의 정보를 가져온다.

        if not self.Check_Validation("challengerleagues"):
            return

        self.conn.request("GET", "/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + self.apiKey)
        request = self.conn.getresponse()
        self.Print_ResponseCode("challengerleagues", request.status)
        if int(request.status) == 200:
            return self.Decode_ResponseToJson(request)
        else:
            self.Print_Errors("Bad Response")
            return

    def Get_API_League_ofSummoner(self, in_id_Encryted):
        # 입력값을 통해 소환사의 리그 정보를 리턴한다.
        # main에서는 검색된 소환사의 Encryted id를 입력받는다.

        if not self.Check_Validation("league/v4/entries/by-summoner/"):
            return

        self.conn.request("GET", "/lol/league/v4/entries/by-summoner/" + in_id_Encryted + "?api_key=" + self.apiKey)
        request = self.conn.getresponse()
        self.Print_ResponseCode("league/v4/entries/by-summoner/", request.status)
        if int(request.status) == 200:
            response = request.read().decode('utf-8')
            #data = list()
            if response == "[]": # 데이터 포맷 때문, 비어있는 데이터라면
                #data.append(False)
                #print(data)
                return (False, None)
            else: # 유효한 리그 데이터가 존재한다면
                jsonData = json.loads(response)[0]
                #data.append(True)
                #data.append(jsonData)
                #print(data)
                return (True, jsonData)
        else:
            self.Print_Errors("Bad Response")
            return




