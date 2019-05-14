from tkinter import *
import random

# 코딩할 때 알아보기 쉽도록 인덱스들의 숫자 의미를 표현하는 변수 선언. 무시해도 좋다.
o = 0
x = 1
none = 3

class Cell:
    def __init__(self):
        self.isClicked = False
        self.value = 2
    def changeValue(self, inputData):
        if not self.isClicked:
            self.isClicked = True
            self.value = inputData
            return True
        return False
    pass

class Program:
    def win(self, value):
        if value:
            self.label.configure(text = "Player X Win!")
        else:
            self.label.configure(text = "Player O Win!")

    def draw(self):
        self.label.configure(text="Draw!")

    def judgementGame(self):
        # 승패를 판정한다.
        # 가로
        if (self.cellDataList[0][0].value == 1) & (self.cellDataList[0][1].value == 1) & (self.cellDataList[0][2].value == 1):
            self.win(1)
            return False
        elif (self.cellDataList[1][0].value == 1) & (self.cellDataList[1][1].value == 1) & (self.cellDataList[1][2].value == 1):
            self.win(1)
            return False
        elif (self.cellDataList[2][0].value == 1) & (self.cellDataList[2][1].value == 1) & (self.cellDataList[2][2].value == 1):
            self.win(1)
            return False
        elif (self.cellDataList[0][0].value == 0) & (self.cellDataList[0][1].value == 0) & (self.cellDataList[0][2].value == 0):
            self.win(0)
            return False
        elif (self.cellDataList[1][0].value == 0) & (self.cellDataList[1][1].value == 0) & (self.cellDataList[1][2].value == 0):
            self.win(0)
            return False
        elif (self.cellDataList[2][0].value == 0) & (self.cellDataList[2][1].value == 0) & (self.cellDataList[2][2].value == 0):
            self.win(0)
            return False
        # 세로
        if (self.cellDataList[0][0].value == 1) & (self.cellDataList[1][0].value == 1) & (self.cellDataList[2][0].value == 1):
            self.win(1)
            return False
        elif (self.cellDataList[0][1].value == 1) & (self.cellDataList[1][1].value == 1) & (self.cellDataList[2][1].value == 1):
            self.win(1)
            return False
        elif (self.cellDataList[0][2].value == 1) & (self.cellDataList[1][2].value == 1) & (self.cellDataList[2][2].value == 1):
            self.win(1)
            return False
        elif (self.cellDataList[0][0].value == 0) & (self.cellDataList[1][0].value == 0) & (self.cellDataList[2][0].value == 0):
            self.win(0)
            return False
        elif (self.cellDataList[0][1].value == 0) & (self.cellDataList[1][1].value == 0) & (self.cellDataList[2][1].value == 0):
            self.win(0)
            return False
        elif (self.cellDataList[0][2].value == 0) & (self.cellDataList[1][2].value == 0) & (self.cellDataList[2][2].value == 0):
            self.win(0)
            return False
        # 사선
        if (self.cellDataList[0][0].value == 1) & (self.cellDataList[1][1].value == 1) & (self.cellDataList[2][2].value == 1):
            self.win(1)
            return False
        elif (self.cellDataList[0][0].value == 0) & (self.cellDataList[1][1].value == 0) & (self.cellDataList[2][2].value == 0):
            self.win(0)
            return False
        elif (self.cellDataList[0][2].value == 1) & (self.cellDataList[1][1].value == 1) & (self.cellDataList[2][0].value == 1):
            self.win(1)
            return False
        elif (self.cellDataList[0][2].value == 0) & (self.cellDataList[1][1].value == 0) & (self.cellDataList[2][0].value == 0):
            self.win(0)
            return False

        # 모두가 가득 찼을 때

        isAllClicked = True

        for row in range(3):
            for col in range(3):
                if not self.cellDataList[row][col].isClicked:
                    isAllClicked = False
        if isAllClicked:
            self.draw()

        pass

    def pressed(self, row, col):
        # 버튼 중복처리를 판정한다.

        if self.playerTurn: # X 차례
            if not self.cellDataList[row][col].changeValue(1):
                return None
            self.buttonList[row * 3 + col].configure(image = self.imageList[1])
            self.label.configure(text = "Player O's turn\n<Press the Button>")
        else: # O 차례
            if not self.cellDataList[row][col].changeValue(0):
                return None
            self.buttonList[row * 3 + col].configure(image = self.imageList[0])
            self.label.configure(text = "Player X's turn\n<Press the Button>")

        self.playerTurn = not self.playerTurn
        self.judgementGame()
        pass

    def importImage(self):
        self.imageList.append(PhotoImage(file="o.gif")) # 0 index
        self.imageList.append(PhotoImage(file="x.gif")) # 1 index
        self.imageList.append(PhotoImage(file="blank.gif")) # 2 index

        pass
    def __init__(self):
        # 필요한 변수 선언
        self.playerTurn = True # X가 먼저 놓는다.
        self.imageList = []
        self.buttonList = []
        self.cellDataList = [[Cell() for col in range(3)] for row in range(3)]
        self.runningFlag = True

        self.window = Tk()
        # 윈도우 사용자 정의
        self.window.title("틱택토")
        self.window.geometry("150x170+100+100")
        self.window.resizable(False, False)

        self.importImage()

        mainframe = Frame(self.window)
        mainframe.pack()

        for r in range(3):
            for c in range(3):
                self.buttonList.append(Button(mainframe, overrelief = "groove", image = self.imageList[2], command = lambda Row = r, Col = c : self.pressed(Row, Col)))
                self.buttonList[-1].grid(row = r, column = c)

        textframe = Frame(self.window)
        textframe.pack()
        self.showText = "게임 진행 중"
        self.label = Label(textframe, text=self.showText)
        self.label.pack()

        self.window.mainloop()
        pass
    pass

Program()