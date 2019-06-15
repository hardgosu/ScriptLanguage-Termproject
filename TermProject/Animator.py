from tkinter import *
import LOL_Parse

_WINDOW_WIDTH = 1280
_WINDOW_HEIGHT = 800



class IntroSceneAnimator:
    global _WINDOW_HEIGHT, _WINDOW_WIDTH

    def __init__(self):
        # 윈도우 설정
        self.window = Tk()
        self.window.resizable(False, False)
        # 중앙 배치를 위한 오프셋 계산
        _WINDOW_OFFSET_X = int(self.window.winfo_screenwidth() / 2 - _WINDOW_WIDTH / 2)
        _WINDOW_OFFSET_Y = int(self.window.winfo_screenheight() / 2 - _WINDOW_HEIGHT / 2)
        # 스크린 중앙 배치
        setGeometry = "{0}x{1}+{2}+{3}".format(_WINDOW_WIDTH, _WINDOW_HEIGHT, _WINDOW_OFFSET_X, _WINDOW_OFFSET_Y)
        self.window.geometry(setGeometry)
        pass