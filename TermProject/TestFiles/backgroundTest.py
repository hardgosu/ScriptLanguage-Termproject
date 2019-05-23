from tkinter import*



window = Tk()


photoImage = PhotoImage(file = "background2.png")
label = Label(window,image = photoImage)

label.pack()


window.mainloop()