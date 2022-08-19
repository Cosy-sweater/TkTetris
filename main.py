from tkinter import *
from tkinter import messagebox
import pyglet
import json
import random
from random import choice
from copy import deepcopy
import time


def close_window():
    global app_running
    if messagebox.askokcancel("", "Выйти из приложения?"):
        master.destroy()
        app_running = False
        app_info["record"] = record
        set_record()


def set_record():
    app_info["record"] = max(record, score)
    with open('app_info.json', 'w') as f:
        json.dump(app_info, f)


def get_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


def game_over():
    global grid  # , app_running
    # app_running = False
    for i in grid:
        master.after(1, game_sc.itemconfigure(i, fill=get_color()))


with open('app_info.json') as f:
    app_info = json.load(f)
W, H = 10, 20
TILE = 45
GAME_RES = W * TILE, H * TILE
RES = 750, 940
FPS = 60
score = 0
record = app_info["record"]
app_running = True

pyglet.font.add_file("font/font.ttf")
master = Tk()
master.protocol("WM_DELETE_WINDOW", close_window)
master.resizable(False, False)
master.wm_attributes("-topmost", 1)
master.title("Tetris" + " " + app_info["version"])
sc = Canvas(master, width=RES[0], height=RES[1], bg="red", highlightthickness=0)
sc.pack()
game_sc = Canvas(master, width=GAME_RES[0] + 1, height=GAME_RES[1] + 1, bg="red", highlightthickness=0)
game_sc.place(x=20, y=20)

img_obj1 = PhotoImage(file="images/background_1.png")
img_obj2 = PhotoImage(file="images/background_2.png")
sc.create_image(0, 0, anchor=NW, image=img_obj1)
game_sc.create_image(0, 0, anchor=NW, image=img_obj2)

grid = [game_sc.create_rectangle(x * TILE, y * TILE, x * TILE + TILE, y * TILE + TILE) for x in range(W) for y in
        range(H)]

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]
figures = [[[x + W // 2, y + 1, 1, 1] for x, y in fig_pos] for fig_pos in figures_pos]
field = [[0 for i in range(W)] for j in range(H)]

anim_count, anim_speed, anim_limit = 0, 60, 2000
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

sc.create_text(505, 30, text="TETRIS", fill="#1a9f2c", font=("a_BighausTitul", 55), anchor=NW)
sc.create_text(530, 650, text="Record:", fill="#f4e635", font=("a_BighausTitul", 35), anchor=NW)
sc.create_text(525, 780, text="Score:", fill="#23d13b", font=("a_BighausTitul", 35), anchor=NW)
sc.create_text(530, 710, text=str(record), fill="#f4e635", font=("a_BighausTitul", 32), anchor=NW)
sc.create_text(525, 840, text=str(score), fill="#23d13b", font=("a_BighausTitul", 32), anchor=NW)

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()


# for i in range(4):
#     figure_rect_x = figure[i][0] * TILE
#     figure_rect_y = figure[i][1] * TILE
#     game_sc.create_rectangle(figure_rect_x, figure_rect_y, figure_rect_x + TILE, figure_rect_y + TILE,
#                              fill=color)
#
# for i in range(4):
#     figure_rect_x = next_figure[i][0] * TILE + 380
#     figure_rect_y = next_figure[i][1] * TILE + 185
#     sc.create_rectangle(figure_rect_x, figure_rect_y, figure_rect_x + TILE, figure_rect_y + TILE,
#                         fill=next_color)


def checkborders():
    if figure[i][0] < 0 or figure[i][0] > W - 1:
        return False
    elif figure[i][1] > H - 1 or field[figure[i][1]][figure[i][0]]:
        return False
    return True


def move_obj(event):
    global anim_limit, dx, rotate
    if event.keysym == "w":
        rotate = True
    if event.keysym == "a":
        dx = -1
        time.sleep(0.001)
    if event.keysym == "s":
        anim_limit = 100
    if event.keysym == "d":
        dx = 1
        time.sleep(0.001)


game_sc.bind_all("<KeyPress-w>", move_obj)
game_sc.bind_all("<KeyPress-a>", move_obj)
game_sc.bind_all("<KeyPress-s>", move_obj)
game_sc.bind_all("<KeyPress-d>", move_obj)

dx, rotate = 0, False

while app_running:
    if app_running:
        # move x
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i][0] += dx
            if not checkborders():
                figure = deepcopy(figure_old)
        # move y
        anim_count += anim_speed
        if anim_count > anim_limit:
            anim_count = 0
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i][1] += 1
                if not checkborders():
                    for j in range(4):
                        field[figure_old[j][1]][figure_old[j][0]] = color
                    figure, color = next_figure, next_color
                    next_figure, next_color = deepcopy(choice(figures)), get_color()
                    anim_limit = 2000
                    break
        # rotate
        center = figure[0]
        figure_old = deepcopy(figure)
        if rotate:
            for i in range(4):
                x = figure[i][1] - center[1]
                y = figure[i][0] - center[0]
                figure[i][0] = center[0] - x
                figure[i][1] = center[1] + y
                if not checkborders():
                    figure = deepcopy(figure_old)
                    break
        # check lines
        line, lines = H - 1, 0
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < W:
                line -= 1
            else:
                anim_speed += 3
                lines += 1
        # compute score
        score += scores[lines]

        fig = []
        # draw figure
        for i in range(4):
            figure_rect_x = figure[i][0] * TILE
            figure_rect_y = figure[i][1] * TILE
            fig.append(
                game_sc.create_rectangle(figure_rect_x, figure_rect_y, figure_rect_x + TILE, figure_rect_y + TILE,
                                         fill=color))

        dx, rotate = 0, False
        master.update_idletasks()
        master.update()
        for id_fig in fig:
            game_sc.delete(id_fig)
    time.sleep(0.01)
# mainloop()
