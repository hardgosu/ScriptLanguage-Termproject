from tkinter import *


class Top(Toplevel):
    def __init__(self, parent, title = "How to Cheat and Hide Text"):
        Toplevel.__init__(self,parent)
        parent.geometry("250x250+100+150")
        if title:
            self.title(title)
        parent.withdraw()
        self.parent = parent
        self.result = None
        dialog = Frame(self)
        self.initial_focus = self.dialog(dialog)
        dialog.pack()


    def dialog(self,parent):

        self.parent = parent

        self.L1 = Label(parent,text = "Hello, World!",state = DISABLED, disabledforeground = parent.cget('bg'))
        self.L1.pack()

        self.B1 = Button(parent, text = "Are You Alive???", command = self.hello)
        self.B1.pack()

    def hello(self):
        self.L1['state']="normal"


if __name__ == '__main__':
    root=Tk()
    ds = Top(root)
    root.mainloop()