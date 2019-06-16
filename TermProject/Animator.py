from tkinter import *
import math                     # modules for floor()
from PIL import ImageTk, Image  # modules for Pillow Image

_WINDOW_WIDTH = 1000
_WINDOW_HEIGHT = 500
_SCENE_SIZE = (_WINDOW_WIDTH, _WINDOW_HEIGHT)

# 인트로 씬을 위한 애니메이터 클래스
# 씬 전개 순서는 학교 로고 - 개발자 학생 로고 - 어플리케이션 이름 순서
class IntroSceneAnimator:
    global _WINDOW_HEIGHT, _WINDOW_WIDTH, _SCENE_SIZE

    def __init__(self):
        global parser

        # 윈도우 설정
        self.animationFlag = True
        self.frame = 0.0
        self.window = Tk()
        self.window.resizable(False, False)

        self.Load_data()

        # 중앙 배치를 위한 오프셋 계산
        _WINDOW_OFFSET_X = int(self.window.winfo_screenwidth() / 2 - _WINDOW_WIDTH / 2)
        _WINDOW_OFFSET_Y = int(self.window.winfo_screenheight() / 2 - _WINDOW_HEIGHT / 2)

        # 스크린 중앙 배치
        setGeometry = "{0}x{1}+{2}+{3}".format(_WINDOW_WIDTH, _WINDOW_HEIGHT, _WINDOW_OFFSET_X, _WINDOW_OFFSET_Y)
        self.window.geometry(setGeometry)

        # 애니메이션 동안 블렌딩을 위한 캔버스와 이미지 로딩
        self.canvas = Canvas(self.window, bg = "white", width = _WINDOW_WIDTH, height = _WINDOW_HEIGHT, bd = 0)
        self.canvas.place(x = 0, y = 0)
        if self.animationFlag:
            self.canvas.after(0, self.Animate)
        else:
            return

    def Animate(self):
        # 애니메이션 재생 속도 조절
        animSpeed = 1
        self.frame += 0.016 * animSpeed

        if math.floor(self.frame) == 0:     # 1초
            self.img_blended = self.Get_BlendedImageFromImages(self.img_logoblack, self.img_kpulogo, self.frame - math.floor(self.frame))
        elif math.floor(self.frame) == 1:   # 2초
            self.img_blended = self.Get_BlendedImageFromImages(self.img_kpulogo, self.img_minsulogo, self.frame - math.floor(self.frame))
        elif math.floor(self.frame) == 2:   # 3초
            self.img_blended = self.Get_BlendedImageFromImages(self.img_minsulogo, self.img_applogo, self.frame - math.floor(self.frame))
        elif math.floor(self.frame) == 3:   # 4초
            self.img_blended = self.img_applogo_raw
            pass
        else:
            self.animationFlag = False
            print("\x1b[1;34mIntroScene Ended\x1b[0;m")
            self.window.destroy()
            return

        self.canvas.delete("introscene")

        self.canvas.create_image(500, 250, image = self.img_blended, tags = "introscene")

        self.canvas.after(16, self.Animate)


    ## 내부 동작을 위한 함수 ####################################################

    def Get_ImageFromFile(self, in_filePath = "", in_ImgSize = tuple()):
        # 파일 경로에 저장되어 있는 이미지를 읽어와 리사이징하고 RGBA 형식으로 변환해 리턴한다.
        if in_filePath == "":
            self.Print_Errors("Empty FilePath")
            return

        if in_ImgSize == ():
            self.Print_Errors("Empty size")
            return

        image = Image.open(in_filePath)
        image_resized = image.resize(in_ImgSize)
        image_converted = image_resized.convert("RGBA")
        if image_converted:
            return image_converted
        else:
            self.Print_Errors("Image Loading Failure")
            return

    def Get_BlendedImageFromImages(self, in_img1, in_img2, in_alpha = 0.0) :
        # 입력받은 이미지를 블렌딩한다.
        image_blended = Image.blend(in_img1, in_img2, in_alpha)
        image_result = ImageTk.PhotoImage(image_blended)

        if image_result:
            return image_result
        else:
            self.Print_Errors("Image Blending Failure")
            return

    def Get_ImageFromFile_COMPLETE(self, in_filePath = "", in_ImgSize = tuple()):
        # 파일 경로에 저장되어 있는 이미지를 읽어와 리사이징하고 RGBA 형식으로 변환해 완전한 PhotoImage 개체로 리턴한다.
        if in_filePath == "":
            self.Print_Errors("Empty FilePath")
            return

        if in_ImgSize == ():
            self.Print_Errors("Empty size")
            return

        image = Image.open(in_filePath)
        image_resized = image.resize(in_ImgSize)
        image_converted = image_resized.convert("RGBA")
        image_result = ImageTk.PhotoImage(image_converted)

        if image_result:
            return image_result
        else:
            self.Print_Errors("Image Loading Failure")
            return

    def Print_Errors(self, in_errorText = ""):
        # 에러 입력을 출력한다.
        print("\x1b[1;91mProcessing Error\x1b[0;m: [{0}]".format(in_errorText))

    def Load_data(self):
        # 이미지 데이터들을 로딩한다.

        # image loading & resizing
        self.img_logoblack = self.Get_ImageFromFile("./sceneimage/logoblack.png", _SCENE_SIZE)
        self.img_kpulogo = self.Get_ImageFromFile("./sceneimage/logo.png", _SCENE_SIZE)
        self.img_minsulogo = self.Get_ImageFromFile("./sceneimage/minsulogo.png", _SCENE_SIZE)
        self.img_applogo = self.Get_ImageFromFile("./sceneimage/applogo.png", _SCENE_SIZE)

        # 바로 원본으로 사용할 이미지 개체
        self.img_logoblack_raw = self.Get_ImageFromFile_COMPLETE("./sceneimage/logoblack.png", _SCENE_SIZE)
        self.img_kpulogo_raw = self.Get_ImageFromFile_COMPLETE("./sceneimage/logo.png", _SCENE_SIZE)
        self.img_minsulogo_raw = self.Get_ImageFromFile_COMPLETE("./sceneimage/minsulogo.png", _SCENE_SIZE)
        self.img_applogo_raw = self.Get_ImageFromFile_COMPLETE("./sceneimage/applogo.png", _SCENE_SIZE)

        print("\x1b[1;32mIntroScene Image Loading COMPLETE\x1b[0;m")