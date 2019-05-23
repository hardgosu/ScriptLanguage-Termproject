# imports
import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import Menu
from tkinter import ttk


# Click OK button
def clickOK():
    text = "Your gender is " + gender.get()
    text = text + "\nYou are " + str(age.get()) + " years old.\n"
    scrt.insert(tk.INSERT, text)  # insert text in a scrolledtext
    scrt.see(tk.END)


# Click radio buttons
def clickRadio():
    scrt.insert(tk.INSERT, value3.get())
    scrt.see(tk.END)


# Click a exit menu
def clickExit():
    win.quit()
    win.destroy()
    exit()


if __name__ == '__main__':
    win = tk.Tk()  # Create instance
    win.title("tkinter sample")  # Add a title

    labelGender = ttk.Label(win, text="Gender:")  # Create a label
    labelGender.grid(column=0, row=0)  # Label's grid

    labelAge = ttk.Label(win, text="Age:")  # Create a label
    labelAge.grid(column=1, row=0)  # Label's grid

    gender = tk.StringVar()  # String variable
    genderCombo = ttk.Combobox(win, width=6, textvariable=gender)  # Create a combobox
    genderCombo['values'] = ("Female", "Male")  # Combobox's items
    genderCombo.grid(column=0, row=1)
    genderCombo.current(0)

    age = tk.IntVar()  # Integer variable
    ageEntered = ttk.Entry(win, width=3, textvariable=age)  # Create a textbox
    ageEntered.grid(column=1, row=1)

    action = ttk.Button(win, text="OK", command=clickOK)  # Create a button
    action.grid(column=2, row=1)

    scrt = tkst.ScrolledText(win, width=33, height=3, wrap=tk.WORD)  # Create a scrolledtext
    scrt.grid(column=0, row=2, columnspan=3)
    scrt.focus_set()  # Default focus

    value1 = tk.IntVar()
    check1 = tk.Checkbutton(win, text="Disabled", variable=value1, state='disabled')  # Create a check button
    check1.select()
    check1.grid(column=0, row=3)

    value2 = tk.IntVar()
    check2 = tk.Checkbutton(win, text="UnChecked", variable=value2)  # Create a check button
    check2.grid(column=1, row=3)

    value3 = tk.StringVar()
    rad1 = tk.Radiobutton(win, text="Radio1", variable=value3, value="Clicked a Radio1.\n",
                          command=clickRadio)  # Create a radio button
    rad1.select()
    rad1.grid(column=2, row=3)
    rad2 = tk.Radiobutton(win, text="Radio2", variable=value3, value="Clicked a Radio2.\n",
                          command=clickRadio)  # Create a radio button
    rad2.grid(column=2, row=4)

    menuBar = Menu(win)  # Create a menu
    win.config(menu=menuBar)

    fileMenu = Menu(menuBar, tearoff=0)  # Create the File Menu
    fileMenu.add_command(label="New")  # Add the "New" menu
    fileMenu.add_separator()  # Add a separator
    fileMenu.add_command(label="Exit", command=clickExit)  # Add the "Exit" menu and bind a function
    menuBar.add_cascade(label="File", menu=fileMenu)

    win.resizable(0, 0)  # Disable resizing the GUI
    win.mainloop()  # Start GUI
