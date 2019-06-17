import LOL_Parse
from tkinter import *
import webbrowser
import Animator

window = Tk()
window.geometry("1230x750+0+0")
canvas = Canvas(window, width = 1230, height = 750, bg = "white")
canvas.place(x = 0, y = 0)

a = Animator.ButtonDrawer(window)

def openSonaLink():
    webbrowser.open("http://gameinfo.leagueoflegends.co.kr/ko/game-info/champions/sona/")
    pass

def nothing():
    pass

def speak(event):
    print("버튼 in")
    print("{0}".format(event))
    defaultbutton.configure(image=buttonoff, bd = 0, overrelief = "solid")
def speakExit(event):
    print("버튼 out")
    print("{0}".format(event))
    defaultbutton.configure(image = buttonon)

def s_IN(event):
    label.configure(image = s2)
def s_OUT(event):
    label.configure(image = s1)
def Click(event):
    webbrowser.open("http://gameinfo.leagueoflegends.co.kr/ko/game-info/champions/sona/")

def r_IN(event):
    label2.configure(image = r2)
def r_OUT(event):
    label2.configure(image = r1)

def c_IN(event):
    label3.configure(image = c2)
def c_OUT(event):
    label3.configure(image = c1)

server = "kr.api.riotgames.com"
apiKey = "RGAPI-354e7489-f932-4a39-90ab-24069b93c837"
# 파서 객체 생성, apikey와 server는 정해져 있다.
parser = LOL_Parse.Parser(server, apiKey)

background = a.Get_ImageFromFile_COMPLETE("./lol_images/background/abc.png", (1230, 750))
yellow = a.Get_ImageFromFile_COMPLETE("./lol_images/background/yellow.png", (1230, 750))
buttonon = parser.Get_ImageFromFile("./lol_images/button_search.png", (30, 20))
buttonoff = parser.Get_ImageFromFile("./lol_images/button_search_over.png", (30, 20))

s1 = parser.Get_ImageFromFile("./sceneimage/lol_search.png", (350, 350))
s2 = parser.Get_ImageFromFile("./sceneimage/lol_search_over.png", (350, 350))
r1 = parser.Get_ImageFromFile("./sceneimage/lol_rotation.png", (350, 350))
r2 = parser.Get_ImageFromFile("./sceneimage/lol_rotation_over.png", (350, 350))
c1 = parser.Get_ImageFromFile("./sceneimage/lol_challenger.png", (350, 350))
c2 = parser.Get_ImageFromFile("./sceneimage/lol_challenger_over.png", (350, 350))


label = Label(canvas, width = 350, height = 350, bd = 0, image = s1, fill = None)
#label.place(x = 30, y = 200)

label2 = Label(canvas, width = 350, height = 350, bd = 0, image = r1, fill = None)
#label2.place(x = 440, y = 200)

label3 = Label(canvas, width = 350, height = 350, bd = 0, image = c1, fill = None)
#label3.place(x = 850, y = 200)

#buttontest = parser.Get_ImageFromFile("./lol_images/test3.png", ())
canvas.create_image(615, 375, image = background)

button = Button(window, command = openSonaLink, text = "버튼", image = buttonon, bd = 0, padx = 0, pady = 0, overrelief = "flat")
button.place(x= 100, y= 100)

buttonSizetest = Button(window, command = nothing, text = "검색", bd = 0, padx = 0, pady = 0, overrelief = "flat")
buttonSizetest.place(x=500, y= 100)

defaultbutton = Button(window, command = nothing, text = "검색", bd = 0, padx = 0, pady = 0, overrelief = "flat")
defaultbutton.place(x= 500, y= 120)

defaultbutton.bind("<Enter>", speak)
defaultbutton.bind("<Leave>", speakExit)

label.bind("<Enter>", s_IN)
label.bind("<Leave>", s_OUT)
label.bind("<Button-1>", Click)

label2.bind("<Enter>", r_IN)
label2.bind("<Leave>", r_OUT)

label3.bind("<Enter>", c_IN)
label3.bind("<Leave>", c_OUT)

canvas.create_image(615, 375, image = yellow)

window.mainloop()