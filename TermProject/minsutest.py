import tkinter
root = tkinter.Tk()
c = tkinter.Canvas(root,background='white'); c.pack(fill='both')
c.create_line(10,10,100,100,fill='red')
c.create_rectangle(20,20,90,90, fill = None, outline='black')
root.mainloop()