import tkinter
from PIL import Image, ImageTk, ImageSequence

class App:
    def __init__(self, in_parent):
        self.parent = in_parent
        self.canvas = tkinter.Canvas(in_parent, width = 1230, height = 750)
        self.canvas.pack()
        self.background = ImageTk.PhotoImage(Image.open("./lol_images/background/background_transparent.png").convert("RGBA"))


        self.sequence = [ImageTk.PhotoImage(img.resize((1230, 750)))
                         for img in ImageSequence.Iterator(
                Image.open("./lol_images/background/background_lol.gif"))]
        self.image = self.canvas.create_image(1230/2, 750/2, image = self.sequence[0])
        self.canvas.create_image(1230 / 2, 750 / 2, image=self.background)

        self.animate(0)
    def animate(self, counter):
        self.canvas.itemconfig(self.image, image = self.sequence[counter])
        self.parent.after(35, lambda : self.animate((counter+1) % len(self.sequence)))

root = tkinter.Tk()
app = App(root)
root.mainloop()