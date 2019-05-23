import tkinter as tk

def show_label():
    label1.lift()

def hide_label():
    label1.lower()

root = tk.Tk()
frame1 = tk.Frame(root)
frame1.pack()

label1 = tk.Label(root, text="Hello, world")
label1.pack(in_=frame1)

button1 = tk.Button(root, text="Click to hide label",command=hide_label)
button2 = tk.Button(root, text="Click to show label", command=show_label)
button1.pack(in_=frame1)
button2.pack(in_=frame1)

entry = tk.Entry(root,relief = 'ridge',borderwidth = 12)
entry.pack()

root.mainloop()