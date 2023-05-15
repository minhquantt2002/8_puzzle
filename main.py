import turtle
import tkinter as tk
import random
import time
import datetime

from bfs_solve import bfs
from a_star_solve import a_star
from dfs_solve import dfs

NUM_ROWS = 3
NUM_COLS = 3
TABLE_WIDTH = 90
TABLE_HEIGHT = 90
FONT_SIZE = 14
FONT = ('Helvetica', FONT_SIZE, 'normal')
RANDOM_STEP = 1000

start = [1, 2, 3, 4, 5, 6, 7, 8, 9]
temp1 = [8, 1, 6, 7, 2, 3, 9, 5, 4]
temp2 = [6, 5, 7, 2, 3, 1, 8, 4, 9]
goal = [1, 2, 3, 4, 5, 6, 7, 8, 9]

images = []
for i in range(NUM_ROWS * NUM_COLS - 1):
    file = f"number-images/{i+1}.gif"
    images.append(file)

images.append("number-images/empty.gif")
images.append("number-images/scramble.gif")


def register_images():
    global screen
    for i in images:
        screen.addshape(i)


def index_2d(my_list, v):
    """Trả về vị trí của một cell khi click trong bảng"""
    for i, x in enumerate(my_list):
        if v in x:
            return (i, x.index(v))


def is_adjacent(el1, el2):
    """Kiểm tra 2 cell có liền kề không"""
    if abs(el2[1] - el1[1]) == 1 and abs(el2[0] - el1[0]) == 0:
        return True
    if abs(el2[0] - el1[0]) == 1 and abs(el2[1] - el1[1]) == 0:
        return True
    return False


def find_cell_empty():
    """Tìm ô rỗng"""
    global board
    for row in board:
        for candidate in row:
            if candidate.shape() == "number-images/empty.gif":
                empty_square = candidate

    return index_2d(board, empty_square)


def swap_cell(cell):
    """Hoán đổi vị trí của cell được click với ô trống"""
    global screen
    current_i, current_j = index_2d(board, cell)
    empty_i, empty_j = find_cell_empty()
    empty_square = board[empty_i][empty_j]
    if is_adjacent([current_i, current_j], [empty_i, empty_j]):
        temp = board[empty_i][empty_j]
        board[empty_i][empty_j] = cell
        board[current_i][current_j] = temp

        x = start[empty_i * 3 + empty_j]
        start[empty_i * 3 + empty_j] = start[current_i * 3 + current_j]
        start[current_i * 3 + current_j] = x
        draw_board()


def random_puzzle():
    """Random puzzle và đảm bảo có hướng giải"""
    global board, screen

    for i in range(RANDOM_STEP):
        for row in board:
            for candidate in row:
                if candidate.shape() == "number-images/empty.gif":
                    empty_square = candidate

        empty_i, empty_j = find_cell_empty()
        directions = ["up", "down", "left", "right"]

        if empty_i == 0:
            directions.remove("up")
        if empty_i >= NUM_ROWS - 1:
            directions.remove("down")
        if empty_j == 0:
            directions.remove("left")
        if empty_j >= NUM_COLS - 1:
            directions.remove("right")

        direction = random.choice(directions)

        if direction == "up":
            swap_cell(board[empty_i - 1][empty_j])
        if direction == "down":
            swap_cell(board[empty_i + 1][empty_j])
        if direction == "left":
            swap_cell(board[empty_i][empty_j - 1])
        if direction == "right":
            swap_cell(board[empty_i][empty_j + 1])


def draw_board():
    global screen, board
    screen.tracer(0)
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            cell = board[i][j]
            cell.showturtle()
            cell.goto(-138 + j * (TABLE_WIDTH + 2),
                      138 - i * (TABLE_HEIGHT + 2))
    screen.tracer(1)


def temp_one():
    global screen, start, temp1
    start = temp1.copy()
    l = 0
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            board[i][j] = cell = turtle.Turtle(images[temp1[l] - 1])
            cell.penup()
            draw_board()
            l += 1


def temp_two():
    global screen, start, temp1
    start = temp2.copy()
    l = 0
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            board[i][j] = cell = turtle.Turtle(images[temp2[l] - 1])
            cell.penup()
            draw_board()
            l += 1


def create_table():
    """Tạo bảng 9 ô"""
    board = [["#" for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    l = 0
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            cell_num = NUM_COLS * i + j
            cell = turtle.Turtle(images[start[l] - 1])
            cell.penup()
            l += 1
            board[i][j] = cell

            def click_callback(x, y, cell=cell):
                return swap_cell(cell)
            cell.onclick(click_callback)
    return board


def create_button(text, callback, x, y):
    """Tạo button"""
    global screen
    canvas = screen.getcanvas()
    button = tk.Button(canvas.master, text=text, background="cadetblue", foreground="white", height=1,
                       command=callback)
    canvas.create_window(x, y, window=button)


def create_label(text, x, y):
    global screen
    canvas = screen.getcanvas()
    label = tk.Label(canvas.master, text=text, background='aliceblue', font=FONT)
    canvas.create_window(x, y, window=label)


def swap_solve(x1, y1, x2, y2):
    temp = board[x1][y1]
    board[x1][y1] = board[x2][y2]
    board[x2][y2] = temp


def solve_bfs():
    """Giải đường đi theo BFS"""
    global screen, label_time, label_step
    print(start)
    time_start = datetime.datetime.now()
    path, l  = bfs(start, goal)
    time_end = datetime.datetime.now()
    label_state.config(text=str(l))
    label_time.config(text=str(round((time_end - time_start).total_seconds() * 1000)) + " ms")
    label_step.config(text=str(len(path)))
    print("Đường đi theo BFS: ", path)
    for i in path:
        time.sleep(0.5)
        empty_i, empty_j = find_cell_empty()
        if (i == 'up'):
            swap_solve(empty_i - 1, empty_j, empty_i, empty_j)
        if (i == 'down'):
            swap_solve(empty_i + 1, empty_j, empty_i, empty_j)
        if (i == 'right'):
            swap_solve(empty_i, empty_j + 1, empty_i, empty_j)
        if (i == 'left'):
            swap_solve(empty_i, empty_j - 1, empty_i, empty_j)
        draw_board()

    for i in range(9):
        start[i] = i + 1


def solve_a_star():
    """Giải dduwofngg đi theo A*"""
    global screen, label_time, label_step, label_state
    print(start)
    time_start = datetime.datetime.now()
    path, l = a_star(tuple(start))
    time_end = datetime.datetime.now()
    label_state.config(text=str(l))
    label_time.config(text=str(round((time_end - time_start).total_seconds() * 1000)) + " ms")
    label_step.config(text=str(len(path)))
    print("Đường đi theo A*: ", path)
    for i in path:
        time.sleep(0.5)
        empty_i, empty_j = find_cell_empty()
        if (i == 'up'):
            swap_solve(empty_i - 1, empty_j, empty_i, empty_j)
        if (i == 'down'):
            swap_solve(empty_i + 1, empty_j, empty_i, empty_j)
        if (i == 'right'):
            swap_solve(empty_i, empty_j + 1, empty_i, empty_j)
        if (i == 'left'):
            swap_solve(empty_i, empty_j - 1, empty_i, empty_j)
        draw_board()

    for i in range(9):
        start[i] = i + 1

def solve_dfs():
    """Giải đường đi theo dfs"""
    global screen, label_time, label_step
    print(start)
    time_start = datetime.datetime.now()
    path, l = dfs(start, goal)
    time_end = datetime.datetime.now()
    label_state.config(text=str(l))
    label_time.config(text=str(round((time_end - time_start).total_seconds() * 1000)) + " ms")
    label_step.config(text=str(len(path)))
    print("Đường đi theo dfs: ", path)
    for i in path:
        # time.sleep(0.0001)
        empty_i, empty_j = find_cell_empty()
        if (i == 'up'):
            swap_solve(empty_i - 1, empty_j, empty_i, empty_j)
        if (i == 'down'):
            swap_solve(empty_i + 1, empty_j, empty_i, empty_j)
        if (i == 'right'):
            swap_solve(empty_i, empty_j + 1, empty_i, empty_j)
        if (i == 'left'):
            swap_solve(empty_i, empty_j - 1, empty_i, empty_j)
        draw_board()

    for i in range(9):
        start[i] = i + 1

def main():
    global screen, board

    # Screen setup
    screen = turtle.Screen()
    screen.setup(600, 600)
    screen.title("8 Puzzle")
    screen.bgcolor("aliceblue")
    screen.tracer(0)
    register_images()

    #  display
    board = create_table()
    create_button(text='Giải BFS', callback=solve_bfs, x=-160, y=-250)
    create_button(text='Giải DFS', callback=solve_dfs, x=-80, y=-250)
    create_button(text='Giải A*', callback=solve_a_star, x=0, y=-250)
    
    create_button(text='Random puzzle', callback=random_puzzle, x=20, y=-210)
    create_button(text='Mẫu 1', callback=temp_one, x=-120, y=-210)
    create_button(text='Mẫu 2', callback=temp_two, x=-60, y=-210)

    create_label(text="Thời gian giải", x=170, y=-170)
    create_label(text="Số bước đi", x=170, y=-110)
    create_label(text="Trạng thái đã duyệt", x=190, y=-50)

    global label_time, label_step, label_state
    canvas = screen.getcanvas()
    label_time = tk.Label(canvas.master, text="0 ms", background='aliceblue', font=FONT)
    canvas.create_window(170, -140, window=label_time)

    canvas = screen.getcanvas()
    label_step = tk.Label(canvas.master, text="0", background='aliceblue', font=FONT)
    canvas.create_window(170, -80, window=label_step)

    canvas = screen.getcanvas()
    label_state = tk.Label(canvas.master, text="0", background='aliceblue', font=FONT)
    canvas.create_window(170, -20, window=label_state)

    draw_board()
    screen.tracer(1)

main()
turtle.done()
