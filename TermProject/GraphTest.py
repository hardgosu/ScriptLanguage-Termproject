from tkinter import *
import time

## data
winRate = 0.7
loseRate = 1 - winRate

## Tkinter Windows
window = Tk()
window.resizable(False, False)
window.geometry("1000x500+500+0")

rightcanvas = Canvas(window, relief = "solid", width = 500, height = 500, bg = "black")
rightcanvas.place(x = 500, y = 0)
leftcanvas = Canvas(window, relief = "raised", width = 500, height = 500, bg = "white")
leftcanvas.place(x = 0, y = 0)

isDone = False

barHeight = 500 - 20 # Max Height
currRed = barHeight +10 - barHeight * winRate
currBlue = barHeight + 10

rightcanvas.create_rectangle(0,0, 100, barHeight, fill = "blue", tags = 'test')

while not(isDone):
    if currRed > barHeight + 10 - barHeight * loseRate - barHeight * winRate:
        time.sleep(0.025)
        if currBlue > barHeight - barHeight * winRate:
            currBlue -= barHeight * winRate * 0.025
        else:
            currRed -= barHeight * loseRate * 0.025

    else:
        isDone = True

    print("{0}, {1}".format(currBlue, currRed))
    rightcanvas.delete('test')
    rightcanvas.create_rectangle(10, barHeight + 10 - barHeight * winRate, 100, currRed, fill = "red2", tags = 'test')
    rightcanvas.create_rectangle(10, barHeight + 10, 100, currBlue, fill = "blue3", tags = 'test' )
    rightcanvas.update()


## loop
window.mainloop()

