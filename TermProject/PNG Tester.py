import LOL_Parse
from tkinter import *
import webbrowser
import Animator

window = Tk()
window.geometry("1230x750+0+0")
canvas = Canvas(window, width = 1230, height = 750, bg = "white")
canvas.place(x = 0, y = 0)
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

server = "kr.api.riotgames.com"
apiKey = "RGAPI-354e7489-f932-4a39-90ab-24069b93c837"
# 파서 객체 생성, apikey와 server는 정해져 있다.
parser = LOL_Parse.Parser(server, apiKey)

background = parser.Get_ImageFromFile("./lol_images/background/background.png", (1230, 750))
buttonon = parser.Get_ImageFromFile("./lol_images/button_search.png", (30, 20))
buttonoff = parser.Get_ImageFromFile("./lol_images/button_search_over.png", (30, 20))
#buttontest = parser.Get_ImageFromFile("./lol_images/test3.png", ())
canvas.create_image(615, 375, image = background)

button = Button(window, command = openSonaLink, text = "버튼", image = buttonon, bd = 0, padx = 0, pady = 0, overrelief = "flat")
button.place(x= 100, y= 100)

buttonSizetest = Button(window, command = nothing, text = "검색", bd = 0, padx = 0, pady = 0, overrelief = "flat")
buttonSizetest.place(x=500, y= 100)

defaultbutton = Button(window, command = nothing, text = "검색", bd = 0, padx = 0, pady = 0, overrelief = "flat")
defaultbutton.place(x= 500, y= 120)

defaultbutton.bind("<Enter>", speak)
defaultbutton.bind("<Leave>", speakExit, )

window.mainloop()