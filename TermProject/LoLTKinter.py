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

        self.tabFrame = Frame(self.mainWindow)
        self.notebook.add(self.tabFrame, text = "롤 전적검색")

        with urllib.request.urlopen("http://ddragon.leagueoflegends.com/cdn/img/champion/loading/Aatrox_1.jpg") as u:
            rawData = u.read()
        im = Image.open(BytesIO(rawData))
        image = ImageTk.PhotoImage(im)
        label = Label(self.tabFrame, image = image, height = 400, width = 200 )
        label.pack()


        self.mainWindow.mainloop()
        pass

object = MainWindow()

