from tkinter import * # import tkinter
import tkinter.ttk as ttk
import urllib.request
from io import BytesIO
from PIL import Image, ImageTk
import json # import json module
import http.client

## 테스트 용도로 만든 py

# 현재 롤 클라이언트 버전을 확인하기 위해 데이터 드래곤 url의 한국서버 json 파일을 받아온다.
currentVersionPath = "https://ddragon.leagueoflegends.com/realms/kr.json"
text_data = urllib.request.urlopen(currentVersionPath).read().decode('utf-8')
data = json.loads(text_data)
version_champion = data["n"]["champion"]
version_profileicon = data["n"]["profileicon"]
version_language = data["l"]


class MainWindow:
    global newimg
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

        #Button(self.profileFrame, text="버튼프레임").pack()
        #Button(self.RankingFrame, text="랭킹프레임").pack()


        ##with urllib.request.urlopen("http://ddragon.leagueoflegends.com/cdn/img/champion/loading/Aatrox_0.jpg") as u:
        ##    rawData = u.read()
        ##im = Image.open(BytesIO(rawData))
        ##resize_im = im.resize((100,200))
        ##image = ImageTk.PhotoImage(resize_im)


        ##label = Label(self.tabFrame, image = image)
        ##label.pack()

        self.GetData("므글쁘글")


        self.mainWindow.mainloop()
        pass

    def GetData(self, summonerName):
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
        print(request.status)
        if int(request.status) == 200: # 정상 응답코드는 200
            response_body = request.read().decode('utf-8')
        jsonData = json.loads(response_body)
        print(jsonData['name'])



object = MainWindow()

