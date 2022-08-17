from tkinter import *
from tkinter import messagebox


def close_window():
    if messagebox.askokcancel("Выход", "Выййти из приложения?"):
        master.destroy()


W, H = 10, 20
TILE = 45
GAME_RES = W * TILE, H * TILE
RES = 750, 940
FPS = 60

master = Tk()
master.protocol("WM_DELETE_WINDOW", close_window)
master.resizable(False, False)
master.wm_attributes("-topmost", 1)
master.title("Tetris")
canvas = Canvas(master, width=RES[0], height=RES[1], bg="red", highlightthickness=0)
canvas.pack()

img_obj1 = PhotoImage(file="images/background_1.png")
img_obj2 = PhotoImage(file="images/background_2.png")
canvas.create_image(0, 0, anchor=NW, image=img_obj1)
canvas.create_image(20, 20, anchor=NW, image=img_obj2)

mainloop()
