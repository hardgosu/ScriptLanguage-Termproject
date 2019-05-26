from tkinter import * # import tkinter
import tkinter.ttk as ttk
import urllib.request
from io import BytesIO
from PIL import Image, ImageTk
import json # import json module

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



        self.mainWindow.mainloop()
        pass

object = MainWindow()

