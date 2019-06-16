from tkinter import *
import math
import LOL_Parse

_WINDOW_WIDTH = 1000
_WINDOW_HEIGHT = 500

server = "kr.api.riotgames.com"
apiKey = "RGAPI-354e7489-f932-4a39-90ab-24069b93c837"
parser = LOL_Parse.Parser(server, apiKey)

# 인트로 씬을 위한 애니메이터 클래스
# 씬 전개 순서는 학교 로고 - 학생 로고 - 어플리케이션 이름 순서
class IntroSceneAnimator:
    global _WINDOW_HEIGHT, _WINDOW_WIDTH

    def __init__(self):
        global parser

        # 윈도우 설정
        self.animationFlag = True
        self.frame = 0.0
        self.window = Tk()
        self.window.resizable(False, False)

        # 중앙 배치를 위한 오프셋 계산
        _WINDOW_OFFSET_X = int(self.window.winfo_screenwidth() / 2 - _WINDOW_WIDTH / 2)
        _WINDOW_OFFSET_Y = int(self.window.winfo_screenheight() / 2 - _WINDOW_HEIGHT / 2)
        # 스크린 중앙 배치
        setGeometry = "{0}x{1}+{2}+{3}".format(_WINDOW_WIDTH, _WINDOW_HEIGHT, _WINDOW_OFFSET_X, _WINDOW_OFFSET_Y)
        self.window.geometry(setGeometry)

        # 블렌딩을 위한 캔버스와 이미지 로딩
        self.img_background = parser.Get_ImageFromFile("./sceneimage/kpulogo.png", (1000, 500))
        self.img_logo = parser.Get_ImageFromFile("./sceneimage/logo.png", (1000, 500))
        self.img_blackbackground = parser.Get_ImageFromFile("./sceneimage/logoblack.png", (1000, 500))

        self.canvas = Canvas(self.window, bg = "white", width = _WINDOW_WIDTH, height = _WINDOW_HEIGHT, bd = 0)
        self.canvas.create_image(500, 250, image = self.img_logo, tags = "introscene")
        self.canvas.place(x = 0, y = 0)
        if self.animationFlag:
            self.canvas.after(0, self.Animate)
        else:
            return

    def Animate(self):
        if int(self.frame) > 5.0:
            self.animationFlag = False
            print("IntroScene Ended")
            self.window.destroy()
            return

        animSpeed = 5
        self.frame += 0.016 * animSpeed
        self.img_blended = parser.Get_BlendedImageFromFile("./sceneimage/logo.png", "./sceneimage/logoblack.png", (1 - self.frame/5.0), (1000,500))

        #self.count = int(self.frame)
        #setBackground = "gray" + str(self.count)

        self.canvas.delete("introscene")
        self.canvas.create_image(500, 250, image = self.img_blended, tags = "introscene")
        #self.canvas.update()

        self.canvas.after(16, self.Animate)
