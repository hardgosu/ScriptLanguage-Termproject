from tkinter import *
import math
import LOL_Parse

_WINDOW_WIDTH = 1000
_WINDOW_HEIGHT = 500

server = "kr.api.riotgames.com"
apiKey = "RGAPI-354e7489-f932-4a39-90ab-24069b93c837"
parser = LOL_Parse.Parser(server, apiKey)

# 인트로 씬을 위한 애니메이터 클래스
# 씬 전개 순서는 학교 로고 - 개발자 학생 로고 - 어플리케이션 이름 순서
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

        self.canvas = Canvas(self.window, bg = "white", width = _WINDOW_WIDTH, height = _WINDOW_HEIGHT, bd = 0)
        self.canvas.place(x = 0, y = 0)
        if self.animationFlag:
            self.canvas.after(0, self.Animate)
        else:
            return

    def Animate(self):
        animSpeed = 3
        self.frame += 0.016 * animSpeed

        if math.floor(self.frame) == 0:     # 1초
            self.img_blended = parser.Get_BlendedImageFromFile("./sceneimage/logoblack.png",
                                                                     "./sceneimage/logo.png",
                                                                     self.frame - math.floor(self.frame), (1000, 500))
        elif math.floor(self.frame) == 1:   # 2초
            self.img_blended = parser.Get_BlendedImageFromFile("./sceneimage/logo.png",
                                                                     "./sceneimage/minsulogo.png",
                                                                     self.frame - math.floor(self.frame), (1000, 500))
        elif math.floor(self.frame) == 2:   # 3초
            self.img_blended = parser.Get_BlendedImageFromFile("./sceneimage/minsulogo.png",
                                                                     "./sceneimage/applogo.png",
                                                                     self.frame - math.floor(self.frame), (1000, 500))
        elif math.floor(self.frame) == 3:   # 4초
            img_blended = parser.Get_ImageFromFile("./sceneimage/applogo.png", (1000, 500))
        else:
            self.animationFlag = False
            print("\x1b[1;32mIntroScene Ended\x1b[0;m")
            self.window.destroy()
            return

        self.canvas.delete("introscene")

        self.canvas.create_image(500, 250, image = self.img_blended, tags = "introscene")

        self.canvas.after(16, self.Animate)
