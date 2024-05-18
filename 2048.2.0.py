import turtle
import random
import tkinter as tk
import sys
import pygame
from tkinter import messagebox

t = turtle.Screen()
t.title("2048 by chiang_j_x")
t.bgcolor("darkslateblue")
t.setup(width=500, height=490)
t.tracer(0)

score = 0

grid = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [2, 0, 2, 0]
]

grid_merged = [
    [False, False, False, False],
    [False, False, False, False],
    [False, False, False, False],
    [False, False, False, False]
]

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.turtlesize(stretch_wid=2, stretch_len=2, outline=2)
pen.goto(0, 260)

def draw_grid():
    pen.clear()
    colors = {
        0: "white",
        2: "yellow",
        4: "orange",
        8: "pink",
        16: "salmon",
        32: "light green",
        64: "yellowgreen",
        128: "orchid",
        256: "purple",
        512: "gold",
        1024: "silver",
        2048: "black"
    }
    grid_y = 0
    y = 120
    for row in grid:
        grid_x = 0
        x = -120
        y=y-45
        for column in row:
            x=x+45
            pen.goto(x, y)
            value = grid[grid_y][grid_x]
            color = colors[value]
            pen.color(color)
            pen.stamp()
            pen.color("midnightblue")
            if column == 0:
                number = ""
            else:
                number = str(column)
            pen.sety(pen.ycor() - 10)
            pen.write(number, align="center", font=("Courier", 14, "bold"))
            pen.sety(pen.ycor() + 10)
            grid_x=grid_x+1
        grid_y=grid_y+1

def add_random():
    while True:
        x = random.randint(0, 3)
        y = random.randint(0, 3)
        if grid[y][x] == 0:
            grid[y][x] = random.choice([2,4])#在這裡更改隨機加入的數字
            break

def move_and_merge(row):
    non_zero = [i for i in row if i != 0]
    merged = []
    new_row = []
    skip = False
    for i in range(len(non_zero)):
        if skip:
            skip = False
            continue
        if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
            merged_value = non_zero[i] * 2
            new_row.append(merged_value)
            global score
            score += merged_value
            skip = True
        else:
            new_row.append(non_zero[i])
    return new_row + [0] * (4 - len(new_row))

def up():
    global score, grid
    for x in range(4):
        for y in range(1, 4):
            if grid[y][x] != 0:
                for y2 in range(y, 0, -1):
                    if grid[y2 - 1][x] == 0:
                        grid[y2 - 1][x] = grid[y2][x]
                        grid[y2][x] = 0
                    elif grid[y2 - 1][x] == grid[y2][x]:
                        grid[y2 - 1][x] *= 2
                        score += grid[y2 - 1][x]
                        grid[y2][x] = 0
                        break
            if grid[y-1][x] == grid[y][x] and not grid_merged[y-1][x]:
                grid[y-1][x] = grid[y][x] * 2
                grid_merged[y-1][x] = True
                grid[y][x] = 0
                y = 0
                continue
    reset_grid_merged()
    print("up")
    add_random()
    draw_grid()
    check_game_over_and_win()

def down():
    global grid
    for _ in range(4):
        for y in range(2, -1, -1):
            for x in range(0, 4):
                if grid[y+1][x] == 0:
                    grid[y+1][x] = grid[y][x]
                    grid[y][x] = 0
                    x -= 1
                    continue
                if grid[y+1][x] == grid[y][x] and not grid_merged[y+1][x]:
                    grid[y+1][x] = grid[y][x] * 2
                    grid_merged[y+1][x] = True
                    grid[y][x] = 0
                    x -= 1
                    continue
    reset_grid_merged()
    print("down")
    add_random()
    draw_grid()
    check_game_over_and_win()

def left():
    global grid
    for y in range(4):
        for x in range(1, 4):
            if grid[y][x] != 0:
                for x2 in range(x, 0, -1):
                    if grid[y][x2 - 1] == 0:
                        grid[y][x2 - 1] = grid[y][x2]
                        grid[y][x2] = 0
                    elif grid[y][x2 - 1] == grid[y][x2] and not grid_merged[y][x2 - 1]:
                        grid[y][x2 - 1] *= 2
                        grid_merged[y][x2 - 1] = True
                        grid[y][x2] = 0
                        break
    reset_grid_merged()
    print("left")
    add_random()
    draw_grid()
    check_game_over_and_win()

def right():
    global grid
    for y in range(4):
        for x in range(2, -1, -1):
            if grid[y][x] != 0:
                for x2 in range(x, 3):
                    if grid[y][x2 + 1] == 0:
                        grid[y][x2 + 1] = grid[y][x2]
                        grid[y][x2] = 0
                    elif grid[y][x2 + 1] == grid[y][x2] and not grid_merged[y][x2 + 1]:
                        grid[y][x2 + 1] *= 2
                        grid_merged[y][x2 + 1] = True
                        grid[y][x2] = 0
                        break
    reset_grid_merged()
    print("right")
    add_random()
    draw_grid()
    check_game_over_and_win()

def reset_grid_merged():
    global grid_merged
    grid_merged = [
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False]
    ]

def check_game_over_and_win_vertical():
    global grid
    print("check_game_over_and_win_vertical")
    if any(2048 in row for row in grid):
        game_win()
    else:
        for col in zip(*grid):
            for i in range(len(col) - 1):
                if col[i] == col[i + 1] or col[i] ==0 or col[i+1] == 0:
                    return 
        game_over()  
def check_game_over_and_win_horizontal():
    global grid
    print("check_game_over_and_win_horizontal")
    if any(2048 in row for row in grid):
        game_win()
    else:
        for row in grid:
            for i in range(len(row) - 1):
                if row[i] == row[i + 1] or row[i] == 0 or row[i+1] == 0:
                    return 
        game_over() 


def check_game_over_and_win():
    check_game_over_and_win_horizontal()
    check_game_over_and_win_vertical()

def game_over():
    print("Game over!")
    pygame.mixer_music.pause()
    try:
        t.update()
    except turtle.Terminator:#例外處理
        return
    ans = messagebox.askyesno("遊戲結束", "遊戲結束！是否要重新開始？")
    if ans:
        reset_game()
        return True
    else:
        t.bye()
        return False

def game_win():
    print("Game win!")
    pygame.mixer_music.pause()
    try:
        t.update()
    except turtle.Terminator:
        return
    ans = messagebox.askyesno("遊戲結束", "恭喜成功達標！遊戲結束！是否要重新開始？")
    if ans:
        reset_game()
        return True
    else:
        t.bye()
        return False

def reset_game():
    print("重置")
    pygame.mixer_music.play(-1)
    global grid, grid_merged, score
    grid = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [2, 0, 2, 0]
]
    grid_merged = [
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False]
    ]
    score = 0
    draw_grid()

t.listen()
t.onkeypress(left, "Left")
t.onkeypress(right, "Right")
t.onkeypress(up, "Up")
t.onkeypress(down, "Down")

draw_grid()
t.update()
pygame.mixer.init()
pygame.mixer_music.load(r"C:\Users\88692\Downloads\2048-song.wav")
pygame.mixer_music.play(-1)
t.mainloop()

#
