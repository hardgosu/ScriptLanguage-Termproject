# 사목게임
# 구글에 사목게임 검색,동영상 참고
# 편의상 O,X 이미지로 해도됌.

# 보드판을 6행 7열로 바꿔보자

# 텍스트와 이미지를 동시에 주면 텍스트가 덮어쓴다
# 버튼에 비어있는 텍스트를 준다
# 비어있는 row가 있는지 찾아서 색을 칠하자

from tkinter import *
import random
import tkinter.messagebox as tm

def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))
class TickTacToe:
    def Again(self):
        #configure를 써보자
        #일케하니까 쉽네
        #기존객체 삭제할거없이
        for i in self.buttonList:

            i.configure(image = self.imageList[2],text = ' ')


            #아래처럼 키 : 값 쌍으로 대입해도 된다.
            #i["image"] = self.imageList[1]
        pass
    def pressed(self,Row,Col):
        #어느 버튼을 클릭했던지 그 열의 끝에서부터 체크한다.
        #5부터찾아봐
        for r in range(5,-1,-1): # 5,4,3,2,1,0
            if self.buttonList[r*7 + Col]["text"] == ' ':
                if self.playerTurn:  # O 차례
                    self.buttonList[r * 7 + Col].configure(image=self.imageList[0], text = 'O')

                else:
                    self.buttonList[r * 7 + Col].configure(image=self.imageList[1], text = 'X')
                self.playerTurn = not self.playerTurn
                break
        self.CheckOfVictory()
        pass

    def CheckOfVictory(self):
        #비김
        for i in range(len(self.buttonList)):
            if (self.buttonList[i]["text"]) == ' ':
                break
            if i == len(self.buttonList) - 1:
                tm.showinfo("비김","비긴거임")
                exit(0)

        # 가로 검사
        for i in range(self.height,-1,-1):
            stack = 0
            label = ""
            for j in range(self.width):
                if (self.buttonList[(i - 1) * self.width + j]["text"]) != ' ':
                    if label == "":
                        label = self.buttonList[(i - 1) * self.width + j]["text"]
                        stack += 1
                        continue
                    if label == self.buttonList[(i - 1) * self.width + j]["text"]:
                        #label = self.buttonList[(i - 1) * self.width + j].label
                        stack += 1
                    else:
                        label = self.buttonList[(i - 1) * self.width + j]["text"]
                        stack = 1
                else:
                    stack = 0

                    label = ""
                if stack == 4:
                    print(label + "가로검사")
                    tm.showinfo("승리","플레이어 " + label +  "이 승리했다!")

        #세로 검사
        for i in range(self.width,-1,-1):
            stack = 0
            label = ""
            for j in range(self.height):
                if (self.buttonList[(i - 1) + (self.width) * j]["text"]) != ' ':
                    if label == "":
                        label = self.buttonList[(i - 1) + (self.width) * j]["text"]
                        stack += 1
                        continue
                    if  label == self.buttonList[(i - 1) + (self.width) * j]["text"]:
                        #label = self.buttonList[(i - 1) * self.width + j].label
                        stack += 1
                    else:
                        label = self.buttonList[(i - 1) + (self.width) * j]["text"]
                        stack = 1
                else:
                    stack = 0
                    label = ""
                if stack == 4:
                    print(label + "세로검사")
                    tm.showinfo("승리","플레이어 " + label +  "이 승리했다!")

        #대각선 검사1
        for i in range(self.width):
            stack = 0
            label = ""
            for j in range(clamp(0,i + 1,self.height - 1)):
                if (self.buttonList[i + j * (self.width - 1)]["text"]) != ' ':
                    if label == "":
                        stack +=1
                        label = self.buttonList[i + j * (self.width - 1)]["text"]
                        continue

                    if label == self.buttonList[i + j * (self.width - 1)]["text"]:
                        #label = self.buttonList[j + j * (self.width - 1)].label
                        stack += 1
                    else:
                        label = self.buttonList[i + j * (self.width - 1)]["text"]
                        stack = 1
                else:
                    stack = 0
                    label = ""
                if stack == 4:
                    print(label + "대각선검사1")
                    tm.showinfo("승리","플레이어 " + label +  "이 승리했다!")

        for i in range(self.height - 1):
            stack = 0
            label = ""
            for j in range(self.height - i - 1):
                #print((i + 1)* self.width  +  (j + 1)*(self.width - 1))
                if (self.buttonList[ (i + 1)* self.width  +  (j + 1)*(self.width - 1) ]["text"]) != ' ':
                    if label == "":
                        stack +=1
                        label = self.buttonList[ (i + 1)* self.width  +  (j + 1)*(self.width - 1) ]["text"]
                        continue

                    if label == self.buttonList[ (i + 1)* self.width  +  (j + 1)*(self.width - 1) ]["text"]:
                        stack +=1
                    else:
                        label = self.buttonList[ (i + 1)* self.width  +  (j + 1)*(self.width - 1) ]["text"]
                        stack = 1
                else:
                    stack = 0
                    label = ""
                if stack == 4:
                    print(label + "대각선검사1-1")
                    tm.showinfo("승리","플레이어 " + label +  "이 승리했다!")




        #대각선 검사2
        for i in range(self.width):
            stack = 0
            label = ""
            for j in range(clamp(0,i + 1,self.height - 1)):
                #print(self.width * (self.height - 1) + i - j * (self.width + 1))
                if (self.buttonList[self.width * (self.height - 1) + i - j * (self.width + 1)]["text"]) != ' ':
                    if label == "":
                        stack +=1
                        label = self.buttonList[self.width * (self.height - 1) + i - j * (self.width + 1)]["text"]
                        continue

                    if label == self.buttonList[self.width * (self.height - 1) + i - j * (self.width + 1)]["text"]:
                        #label = self.buttonList[j + j * (self.width - 1)].label
                        stack += 1
                    else:
                        label = self.buttonList[self.width * (self.height - 1) + i - j * (self.width + 1)]["text"]
                        stack = 1
                else:
                    stack = 0
                    label = ""
                if stack == 4:
                    print(label + "대각선검사2")
                    tm.showinfo("승리","플레이어 " + label +  "이 승리했다!")

        for i in range(self.height - 1):
            stack = 0
            label = ""
            for j in range(self.height - i - 1):
                #print((self.width * (self.height - (1 + i)) - 1)  -  (j)*(self.width + 1) )
                if (self.buttonList[ (self.width * (self.height - (1 + i)) - 1)  -  (j)*(self.width + 1) ]["text"]) != ' ':
                    if label == "":
                        stack += 1
                        label = self.buttonList[(self.width * (self.height - (1 + i)) - 1) - (j) * (self.width + 1)]["text"]
                        continue

                    if label == self.buttonList[ (self.width * (self.height - (1 + i)) - 1)  -  (j)*(self.width + 1) ]["text"]:
                        stack +=1
                    else:
                        label = self.buttonList[ (self.width * (self.height - (1 + i)) - 1)  -  (j)*(self.width + 1) ]["text"]
                        stack = 1
                else:
                    stack = 0
                    label = ""
                if stack == 4:
                    print(label + "대각선검사2-1")
                    tm.showinfo("승리","플레이어 " + label +  "이 승리했다!")


        pass



    def __init__(self):
        window = Tk()
        self.imageList = []
        self.imageList.append(PhotoImage(file = "o.gif"))
        self.imageList.append(PhotoImage(file = "x.gif"))
        self.imageList.append(PhotoImage(file = "empty.gif"))
        self.buttonList = []

        self.width = 7
        self.height = 6


        frame1 = Frame(window)
        frame1.pack()

        self.playerTurn = True


        for r in range(6): #r은 0,1,2
            for c in range(7): #c는 0,1,2
                #인자있는 함수를 연결하려면 람다를 활용...
                #꼭 기억하세요
                self.buttonList.append(Button(frame1, text = ' ',image = self.imageList[2],command = lambda Row = r,Col = c : self.pressed(Row,Col)))
                self.buttonList[-1].grid(row = r, column = c)
        frame2 = Frame(window)
        frame2.pack()
        self.showText = "안녕"
        self.reFreshButton = Button(frame2,text = self.showText,command = self.Again)
        self.reFreshButton.pack()

        window.mainloop()


TickTacToe()