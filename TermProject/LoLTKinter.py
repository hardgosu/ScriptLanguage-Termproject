from tkinter import * # import tkinter
import tkinter.ttk as ttk

import json # import json module

## 테스트 용도로 만든 py


class MainWindow:
    def __init__(self):
        self.mainWindow = Tk()
        self.mainWindow.resizable(False, False)
        self.mainWindow.geometry("1280x800+100+100")
        self.mainWindow.wm_iconbitmap('DNF.ico')
        self.mainWindow.title("useful")

        self.notebook = ttk.Notebook(self.mainWindow, width=1230, height=750)
        self.notebook.pack()

        self.tabFrame = Frame(self.mainWindow)
        self.notebook.add(self.tabFrame, text = "롤 전적검색")

        self.mainWindow.mainloop()
        pass

object = MainWindow()

