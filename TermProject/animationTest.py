# Working on window interface of soundAsleep

# Tkinter will handle the GUI
from tkinter import *

root = Tk()
root.title("soundAsleep beta")

frame = []

# Importing the images. They are named w1.gif, w2.gif...w7.gif
for i in range(1, 7):
    fname = "새 폴더/w (" + str(i) + ").png"
    frame += [PhotoImage(file=fname)]

wrap = Canvas(root, width=200, height=120)
wrap.pack()


def do_animation(currentframe):
    def do_image():
        wrap.create_image(100, 70, image=frame[currentframe],
                          tag='ani')

    # Delete the current picture if one exists
    wrap.delete('ani')
    try:
        do_image()
    except IndexError:


        # End of image list reached, start over at the first image

        currentframe = 0
        do_image()
    wrap.update_idletasks()  # Force redraw
    currentframe = currentframe + 1
    # Call myself again to keep the animation running in a loop
    root.after(50, do_animation, currentframe)

# Start the animation loop just after the Tkinter loop begins
root.after(10, do_animation, 0)

root.mainloop()
