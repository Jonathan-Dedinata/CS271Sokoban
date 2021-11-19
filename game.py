import numpy as np
import block
import tkinter as tk


def next_position(direction, _x, _y):
    if direction == 1:
        return _x-1, _y
    elif direction == 2:
        return _x+1, _y
    elif direction == 3:
        return _x , _y -1
    elif direction == 4:
        return _x , _y +1
    else:
        raise AttributeError("wrong direction")


class game:
    player_x = -1
    player_y = -1
    board = {}
    number_of_box = -1
    number_of_box_on_target = -1

    '''board is dict, given (x,y) => block'''

    def __init__(self, _player_x, _player_y, number, data):
        self.player_x = _player_x
        self.player_y = _player_y
        self.number_of_box = number
        self.board = data
        self.number_of_box_on_target = 0 #fix latter

        print("unfinished")

    def hit_wall_check(self, direction):
        return self.board[next_position(direction, self.player_x, self.player_y)].is_wall()

    def hit_box_check(self, direction):
        return self.board[next_position(direction, self.player_x, self.player_y)].is_box()

    def make_push(self, direction):
        exit(1)

    def make_move(self, direction):
        if direction == 1:
            self.board[(self.player_x, self.player_y)] = block.block(self.player_x, self.player_y)
            self.board[(self.player_x -1, self.player_y)] = block.player(self.player_x -1, self.player_y)
            self.player_x -= 1
        elif direction == 2:
            self.board[(self.player_x, self.player_y)] = block.block(self.player_x, self.player_y)
            self.board[(self.player_x+1, self.player_y )] = block.player(self.player_x+1, self.player_y + 1)
            self.player_x += 1
        elif direction == 3:
            self.board[(self.player_x, self.player_y)] = block.block(self.player_x, self.player_y)
            self.board[(self.player_x , self.player_y-1)] = block.player(self.player_x  , self.player_y-1)
            self.player_y -= 1
        elif direction == 4:
            self.board[(self.player_x, self.player_y)] = block.block(self.player_x, self.player_y)
            self.board[(self.player_x , self.player_y+1)] = block.player(self.player_x, self.player_y+1)
            self.player_y += 1

    def step(self, direction):
        next_player_x = -1
        '''d = 1 up, d = 2 down, d = 3 left, d = 4 up'''
        if self.player_x == -1 or self.player_y == -1:
            print("not initialized..... exit")
            exit(1)
        if direction == 1:
            if not self.hit_wall_check(direction):
                self.make_move(1)
        if direction == 2:
            if not self.hit_wall_check(direction):
                self.make_move(2)
        if direction == 3:
            if not self.hit_wall_check(direction):
                self.make_move(3)
        if direction == 4:
            if not self.hit_wall_check(direction):
                self.make_move(4)






def read_input(file_name):
    data_flow = []
    with open(file_name, "r") as  f:
        for line in f:
            values = line.split()
            values = list(map(int, values))
            for v in values:
                data_flow.append(v)
    print("done reading")
    number_of_box = 0
    vertical_length = data_flow.pop(0)
    horizontal_length = data_flow.pop(0)
    x = -1
    y = -1

    grids = {}
    for i in range(data_flow.pop(0)):
        x = data_flow.pop(0)
        y = data_flow.pop(0)
        grids[x, y] = block.wall(x, y)
    number_of_box = data_flow.pop(0)
    for i in range(number_of_box):
        x = data_flow.pop(0)
        y = data_flow.pop(0)
        grids[x, y] = block.box(x, y)
    for i in range(data_flow.pop(0)):
        x = data_flow.pop(0)
        y = data_flow.pop(0)
        grids[x, y] = block.target(x, y)
    x = data_flow.pop(0)
    y = data_flow.pop(0)
    grids[x, y] = block.player(x, y)

    for i in range(1,vertical_length+1):
        for j in range(1,horizontal_length+1):
            if (i,j) not in grids:
                grids[i,j]  = block.block(i,j)


    return data_flow, grids, vertical_length, horizontal_length, number_of_box, x, y


def draw(canvas, grids_data):
    for key, val in grids_data.items():
        if grids_data[key].is_wall():
            canvas.itemconfig(grids[key[0] - 1][key[1] - 1], fill='brown')
        elif grids_data[key].is_player():
            canvas.itemconfig(grids[key[0] - 1][key[1] - 1], fill='blue')
        elif grids_data[key].is_box():
            canvas.itemconfig(grids[key[0] - 1][key[1] - 1], fill='yellow')
        elif grids_data[key].is_target():
            canvas.itemconfig(grids[key[0] - 1][key[1] - 1], fill='red')
        elif grids_data[key].is_score():
            canvas.itemconfig(grids[key[0] - 1][key[1] - 1], fill='black')
        else:
            canvas.itemconfig(grids[key[0] - 1][key[1] - 1], fill='white')
    return canvas


if __name__ == "__main__":
    print("this is game class")
    print("test starts")

    data, grids_data, v, h, n, x, y = read_input("sokoban00.txt")

    '''
    
    
    
    '''

    window = tk.Tk()

    window.title('game')

    window.geometry('800x800')

    canvas = tk.Canvas(window, bg='white', height=780, width=780)

    grids = []
    for i in range(v):
        row = []
        for j in range(h):
            row.append(canvas.create_rectangle(j * 20 + 50, i * 20 + 30, j * 20 + 20 + 50, i * 20 + 30 + 20))
        grids.append(row)

    # draw

    canvas = draw(canvas, grids_data)

    canvas.pack()
    g = game(x, y, n, grids_data)


    def up():
        g.step(1)
        draw(canvas,g.board)
        print("up")
        return canvas


    def down():
        g.step(2)
        draw(canvas, g.board)
        print("down")
        return canvas



    def left():
        g.step(3)
        draw(canvas, g.board)
        print("left")
        return canvas


    def right():
        g.step(4)
        draw(canvas, g.board)
        print("right")
        return canvas

    b_up = tk.Button(window, text='UP', command=up).place(x=100, y=700)
    b_down = tk.Button(window, text='DOWN', command=down).place(x=200, y=700)
    b_left = tk.Button(window, text='LEFT', command=left).place(x=300, y=700)
    b_right = tk.Button(window, text='RIGHT', command=right).place(x=400, y=700)

    print("load game")

    window.mainloop()
