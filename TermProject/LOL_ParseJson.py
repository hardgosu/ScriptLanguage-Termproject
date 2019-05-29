## importing Area ##
import json                 # json module importing
import urllib.request       #
import http.client          #

####################################################################################
## Class Definition ##
class Parser:
    # URL 주소를 통해 JSON을 파싱하거나 URL과 LOL-API를 통해 가져온 JSON 객체를 파싱하여 리턴하는 역할을 수행한다.

    def __init__(self, in_server = "", in_apiKey= ""):
        self.isAlive = True

        if in_server == "" | in_apiKey == "":
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
        print("{0}::Response status-{1}".format(in_FuncName, in_number))

    def Check_Validation(self, in_errorCode = ""):
        # 파서가 활성화 되었는가? - 파서가 수행하는 메서드들의 첫 부분에 들어간다.
        if self.isAlive:
            return True
        else:
            print("Error has Occured : [\"The Parser is NOT active\"]\n[RETURNED AT::{0}]".format(in_errorCode))
            return False

    def Decode_URLtoJson(self, in_url):
        # URL에 요청해서 받은 JSON을 파싱하여 리턴한다.
        if not self.Check_Validation():
            return

        local_url = in_url
        return json.loads(urllib.request.urlopen(local_url).read().decod('utf-8'))

    def Encode_Text(self, in_text):
        # URL에 사용할 일반 텍스트를 인코딩하여 리턴한다.
        encText = urllib.parse.quote(in_text)
        return encText

    def Get_API_Search_byName(self, in_SummonerName):
        # 스트링으로 받은 in_SummonerName을 Encoding 하여 관련 정보를 리턴한다.

        if not self.Check_Validation("Search_byName"):
            return

        if in_SummonerName == "":
            self.Print_Errors("Empty input")
            return

        encText = self.Encode_Text(in_SummonerName)

        self.conn.request("GET",
                     "/lol/summoner/v4/summoners/by-name/" + encText + "?api_key=" + self.apiKey)
        request = self.conn.getresponse()
        print("First Searching Response Code:" + str(request.status))


        pass

    def Get_API_ChampionRotations(self):
        # 현재 서버의 챔피언 로테이션 ID 값을 리스트로 반환한다.

        if not self.Check_Validation("ChampionRotations"):
            return



        pass

    def GEt_API_(self):
        pass


