from tkinter import *
from tkinter import messagebox
import pyglet
import json
import random


def close_window():
    if messagebox.askokcancel("", "Выйти из приложения?"):
        master.destroy()
        app_info["record"] = record
        with open('app_info.json', 'w') as f:
            json.dump(app_info, f)


def get_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


def game_over():
    global grid
    for i in grid:
        master.after(1, canvas.itemconfigure(i, fill=get_color()))


with open('app_info.json') as f:
    app_info = json.load(f)

W, H = 10, 20
TILE = 45
GAME_RES = W * TILE, H * TILE
RES = 750, 940
FPS = 60
score = 0
record = app_info["record"]

pyglet.font.add_file("font/font.ttf")
master = Tk()
master.protocol("WM_DELETE_WINDOW", close_window)
master.resizable(False, False)
master.wm_attributes("-topmost", 1)
master.title("Tetris" + " " + app_info["version"])
canvas = Canvas(master, width=RES[0], height=RES[1], bg="red", highlightthickness=0)
canvas.pack()

img_obj1 = PhotoImage(file="images/background_1.png")
img_obj2 = PhotoImage(file="images/background_2.png")
canvas.create_image(0, 0, anchor=NW, image=img_obj1)
canvas.create_image(20, 20, anchor=NW, image=img_obj2)

grid = [canvas.create_rectangle(x * TILE, y * TILE, x * TILE + TILE, y * TILE + TILE) for x in range(W) for y in
        range(H)]
for i in grid:
    canvas.move(i, 20, 20)

canvas.create_text(505, 30, text="TETRIS", fill="#1a9f2c", font=("a_BighausTitul", 55), anchor=NW)
canvas.create_text(530, 650, text="Record:", fill="#f4e635", font=("a_BighausTitul", 35), anchor=NW)
canvas.create_text(525, 780, text="Score:", fill="#23d13b", font=("a_BighausTitul", 35), anchor=NW)

canvas.create_text(530, 710, text=str(record), fill="#f4e635", font=("a_BighausTitul", 32), anchor=NW)
canvas.create_text(525, 840, text=str(score), fill="#23d13b", font=("a_BighausTitul", 32), anchor=NW)

mainloop()