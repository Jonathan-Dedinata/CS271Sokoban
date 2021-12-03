import numpy as np
import block
import tkinter as tk
import tkinter.messagebox
import time
from RL import QLearning
from copy import deepcopy

def next_position(direction, _x, _y):
    if direction == 1:
        return _x - 1, _y
    elif direction == 2:
        return _x + 1, _y
    elif direction == 3:
        return _x, _y - 1
    elif direction == 4:
        return _x, _y + 1
    else:
        raise AttributeError("wrong direction")

class freeze:
    def __init__(self):
        self.freeze_flag = False

class game:
    player_x = -1
    player_y = -1
    board = {}
    number_of_box = -1
    number_of_box_on_target = -1
    v = 0
    h = 0
    '''board is dict, given (x,y) => block'''

    def __init__(self, _player_x, _player_y, number, data, _v, _h):
        self.player_x = _player_x
        self.player_y = _player_y
        self.number_of_box = number
        self.board = data
        self.number_of_box_on_target = 0  # fix latter
        self.v = _v
        self.h = _h
        self.copy_player_x = self.player_x
        self.copy_player_y = self.player_y
        self.copy_board = deepcopy(self.board)
        print("unfinished")

    def reset(self):
        self.player_x = self.copy_player_x
        self.player_y = self.copy_player_y
        self.board =  deepcopy(self.copy_board)
        self.number_of_box_on_target = 0

    

    def p_not_move_check(self, direction):
        next_player_position = next_position(direction, self.player_x, self.player_y)
        next_box_position = next_position(direction, next_player_position[0], next_player_position[1])
        return self.board[next_position(direction, self.player_x, self.player_y)].is_wall() or ( self.board[next_box_position].is_box() and self.board[next_player_position].is_box())

    def p_hit_block_check(self, direction):
        return self.board[next_position(direction, self.player_x, self.player_y)].tag == 0

    def p_hit_box_check(self, direction):
        _next_player_position = next_position(direction, self.player_x, self.player_y)
        # _next_box_position = next_position(direction,_next_player_position[0],_next_player_position[1])
        return self.board[_next_player_position].is_box()  # self.board[_next_box_position].is_box()

    def p_hit_target_check(self, direction):
        return self.board[next_position(direction, self.player_x, self.player_y)].is_target()

    def p_hit_score_check(self, direction):
        return self.board[next_position(direction, self.player_x, self.player_y)].is_score()

    def update_player(self, direction):

        if direction == 1:
            self.player_x -= 1
        elif direction == 2:
            self.player_x += 1
        elif direction == 3:
            self.player_y -= 1
        elif direction == 4:
            self.player_y += 1

    def step(self, direction):
        next_player_x = -1
        '''d = 1 up, d = 2 down, d = 3 left, d = 4 up'''
        if self.player_x == -1 or self.player_y == -1:
            print("not initialized..... exit")
            exit(1)
        # if direction == 1:
        next_player_position = next_position(direction, self.player_x, self.player_y)
        next_box_position = next_position(direction, next_player_position[0], next_player_position[1])
        if not self.p_not_move_check(direction):
            if (self.p_hit_block_check(direction) or self.p_hit_target_check(direction)) and not self.p_hit_score_check(direction):
                self.update_player(direction)
            elif self.p_hit_box_check(direction) and (not self.p_hit_score_check(direction)):
                #next_player_position = next_position(direction, self.player_x, self.player_y)
                #next_box_position = next_position(direction, next_player_position[0], next_player_position[1])
                if not self.board[next_box_position].is_wall():
                    self.update_player(direction)
                    self.board[next_player_position] = block.block(next_box_position[0], next_box_position[1])
                    if self.board[next_box_position].is_target():
                        self.board[next_box_position] = block.score(next_box_position[0], next_box_position[1])
                        self.number_of_box_on_target += 1
                        print("hit target" + str(self.number_of_box_on_target) + "/" + str(self.number_of_box))
                    else:
                        self.board[next_box_position] = block.box(next_box_position[0], next_box_position[1])
            elif self.p_hit_score_check(direction):
                #next_player_position = next_position(direction, self.player_x, self.player_y)
                #next_box_position = next_position(direction, next_player_position[0], next_player_position[1])
                if not self.board[next_box_position].is_wall():
                    self.update_player(direction)
                    self.board[next_player_position] = block.target(next_box_position[0], next_box_position[1])
                    self.number_of_box_on_target -= 1
                    print("lose target" + str(self.number_of_box_on_target) + "/" +str(self.number_of_box))
                    if self.board[next_box_position].is_target():
                        self.board[next_box_position] = block.score(next_box_position[0], next_box_position[1])
                        self.number_of_box_on_target += 1
                        print("hit target"+ str(self.number_of_box_on_target) + "/" +str(self.number_of_box))
                    else:
                        self.board[next_box_position] = block.box(next_box_position[0], next_box_position[1])



        '''
         if direction == 2:
            if not self.p_hit_wall_check(direction):
                if self.p_hit_block_check(direction) or self.p_hit_target_check(direction):
                    self.update_player(direction)
                elif self.p_hit_box_check(direction) and (not self.p_hit_score_check(direction)):
                    next_player_position = next_position(direction, self.player_x, self.player_y)
                    next_box_position = next_position(direction, next_player_position[0], next_player_position[1])
                    if not self.board[next_box_position].is_wall():
                        self.update_player(direction)
                        self.board[next_player_position] = block.block(next_box_position[0], next_box_position[1])
                        self.board[next_box_position] = block.box(next_box_position[0],next_box_position[1])
        if direction == 3:
            if not self.p_hit_wall_check(direction):
                if self.p_hit_block_check(direction) or self.p_hit_target_check(direction):
                    self.update_player(direction)
                elif self.p_hit_box_check(direction) and (not self.p_hit_score_check(direction)):
                    next_player_position = next_position(direction, self.player_x, self.player_y)
                    next_box_position = next_position(direction, next_player_position[0], next_player_position[1])
                    if not self.board[next_box_position].is_wall():
                        self.update_player(direction)
                        self.board[next_player_position] = block.block(next_box_position[0], next_box_position[1])
                        self.board[next_box_position] = block.box(next_box_position[0],next_box_position[1])
        if direction == 4:
            if not self.p_hit_wall_check(direction):
                if self.p_hit_block_check(direction) or self.p_hit_target_check(direction):
                    self.update_player(direction)
                elif self.p_hit_box_check(direction) and (not self.p_hit_score_check(direction)):
                    next_player_position = next_position(direction, self.player_x, self.player_y)
                    next_box_position = next_position(direction, next_player_position[0], next_player_position[1])
                    if not self.board[next_box_position].is_wall():
                        self.update_player(direction)
                        self.board[next_player_position] = block.block(next_box_position[0], next_box_position[1])
                        self.board[next_box_position] = block.box(next_box_position[0],next_box_position[1])
        
        
        '''
    def getState(self):
        state = []
        # print("board = ", self.board)
        for i in range(1, self.h + 1):
            for j in range(1, self.v + 1):
                if self.board[i, j].is_box():
                    state.append([i, j])
        for i in range(1, self.h + 1):
            for j in range(1, self.v + 1):
                if self.board[i, j].is_player():
                    state.append([i, j])
        return state

    def Manhattan_Dis(self, x, y):
        return abs(x[0] - y[0]) + abs(x[1] - y[1])

    def evaluateAction(self, action, target, totalSteps):
        if(action == 1):
            left()
        elif(action == 2):
            up()
        elif(action == 3):
            right()
        elif(action == 4):
            down()
        new_state = self.getState()
        finished = True
        stuck = False
        reward = 0
        occupiedList = []
        # for i in range(len(target)):
        #     if self.board[target[i][0], target[i][1]].is_box():
        #         occupiedList.append(1)
        #     else:
        #         occupiedList.append(0)

        for i in range(len(target)):
            x, y = new_state[i][0], new_state[i][1]
            if self.board[x, y].is_target():
                occupiedList.append(1)
            else:
                occupiedList.append(0)
                if self.board[x - 1, y].is_wall() and self.board[x, y + 1].is_wall(): stuck = True
                if self.board[x, y + 1].is_wall() and self.board[x + 1, y].is_wall(): stuck = True
                if self.board[x + 1, y].is_wall() and self.board[x, y - 1].is_wall(): stuck = True
                if self.board[x, y - 1].is_wall() and self.board[x - 1, y].is_wall(): stuck = True
            if stuck:
                reward -= 10

        for i in range(len(target)):
            r = 100000
            for j in range(len(target)):
                if occupiedList[j] == 1: continue
                r = min(r, self.Manhattan_Dis(new_state[i], target[j]))
            if r == 0:
                reward += 50
            else:
                finished = False
                # reward -= r
        if finished:
            reward += 500
        reward -= 0.1 * totalSteps
        return new_state, reward, finished, stuck

def read_input(file_name):
    data_flow = []
    with open(file_name, "r") as  f:
        for line in f:
            values = line.split()
            values = list(map(int, values))
            for v in values:
                data_flow.append(v)
    print("done reading")
    # print("data_flow = ", data_flow)
    number_of_box = 0
    vertical_length = data_flow.pop(0)
    horizontal_length = data_flow.pop(0)
    x = -1
    y = -1
    # print("data_flow = ", data_flow)
    grids = {}
    for i in range(data_flow.pop(0)):
        x = data_flow.pop(0)
        y = data_flow.pop(0)
        grids[x, y] = block.wall(x, y)
    number_of_box = data_flow.pop(0)
    box_positions = []
    for i in range(number_of_box):
        x = data_flow.pop(0)
        y = data_flow.pop(0)
        box_positions.append([x, y])
        grids[x, y] = block.box(x, y)
    target_positions = []
    for i in range(data_flow.pop(0)):
        x = data_flow.pop(0)
        y = data_flow.pop(0)
        target_positions.append([x, y])
        grids[x, y] = block.target(x, y)
    x = data_flow.pop(0)
    y = data_flow.pop(0)
    # grids[x, y] = block.player(x, y)

    for i in range(1, vertical_length + 1):
        for j in range(1, horizontal_length + 1):
            if (i, j) not in grids:
                grids[i, j] = block.block(i, j)

    return data_flow, grids, box_positions, target_positions, vertical_length, horizontal_length, number_of_box, x, y


def draw(canvas, grids_data, x, y):
    for key, val in grids_data.items():
        if grids_data[key].is_wall():
            canvas.itemconfig(grids[key[0] - 1][key[1] - 1], fill='brown')
        # elif grids_data[key].is_player():
        # canvas.itemconfig(grids[key[0] - 1][key[1] - 1], fill='blue')
        elif grids_data[key].is_box() and (not grids_data[key].is_target()):
            canvas.itemconfig(grids[key[0] - 1][key[1] - 1], fill='yellow')
        elif grids_data[key].is_target()and (not grids_data[key].is_score()):
            canvas.itemconfig(grids[key[0] - 1][key[1] - 1], fill='red')
        elif grids_data[key].is_score():
            canvas.itemconfig(grids[key[0] - 1][key[1] - 1], fill='black')
        else:
            canvas.itemconfig(grids[key[0] - 1][key[1] - 1], fill='white')
    print(canvas.bbox(grids[x - 1][y - 1]))
    canvas.delete('player')
    canvas.create_oval(canvas.bbox(grids[x - 1][y - 1]), fill='grey', tag='player')
    return canvas



    # left()
    # return 0






if __name__ == "__main__":
    print("this is game class")
    print("test starts")

    data, grids_data, box_positions, target_positions, v, h, n, x, y = read_input("sokoban01.txt")
    # print("data = ", data)
    # print("grids_data = ", grids_data)
    # print("v = ", v)
    # print("h = ", h)
    # print("n = ", n)
    # print("x = ", x)
    # print("y = ", y)
    # print("states = ", box_positions)
    # exit()
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
    print(grids)
    # exit()
    # draw

    canvas = draw(canvas, grids_data, x, y)
    canvas.pack()
    g = game(x, y, n, grids_data, v, h)
    # exit()

    control_box = freeze()




    def AI_Sokoban(grids, state, target):
        agent = QLearning()
        control_box.freeze_flag = False
        for episode in range(1000):
            print("episode ", episode)
            soft_reset_for_ML()
            totalSteps = 0
            preAction = 0
            while True:
                if control_box.freeze_flag:
                    break
                action = agent.chooseAction(str(state), preAction, totalSteps)
                totalSteps = totalSteps + 1
                next_state, reward, finished, stuck = g.evaluateAction(action, target, totalSteps)
                agent.Q_learning(str(state), action, reward, str(next_state), finished)
                state = next_state
                preAction = action
                if finished or totalSteps > 1000 or stuck:
                    break
                time.sleep(0.0001)

                print('currSteps = ', totalSteps)
        print('totalSteps = ', totalSteps)


    def up():
        g.step(1)
        draw(canvas, g.board, g.player_x, g.player_y)
        canvas.update()
        print("up")
        if g.number_of_box == g.number_of_box_on_target:
            tk.messagebox.showinfo("result", "Successful")
        return canvas


    def down():
        g.step(2)
        draw(canvas, g.board, g.player_x, g.player_y)
        canvas.update()
        print("down")
        if g.number_of_box == g.number_of_box_on_target:
            tk.messagebox.showinfo("result", "Successful")
        return canvas


    def left():
        g.step(3)
        draw(canvas, g.board, g.player_x, g.player_y)
        canvas.update()
        print("left")
        if g.number_of_box == g.number_of_box_on_target:
            tk.messagebox.showinfo("result", "Successful")
        return canvas


    def right():
        g.step(4)
        draw(canvas, g.board, g.player_x, g.player_y)
        canvas.update()
        print("right")
        if g.number_of_box == g.number_of_box_on_target:
            tk.messagebox.showinfo("result", "Successful")
        return canvas


    def reset():
        control_box.freeze_flag = True
        g.reset()
        draw(canvas, g.board, g.player_x, g.player_y)
        canvas.update()

    def soft_reset_for_ML():
        g.reset()
        draw(canvas, g.board, g.player_x, g.player_y)
        canvas.update()




    state = g.getState()
    b_up = tk.Button(window, text='UP', command=up).place(x=100, y=700)
    b_down = tk.Button(window, text='DOWN', command=down).place(x=200, y=700)
    b_left = tk.Button(window, text='LEFT', command=left).place(x=300, y=700)
    b_right = tk.Button(window, text='RIGHT', command=right).place(x=400, y=700)
    b_run = tk.Button(window, text='RUN', command=lambda :AI_Sokoban(grids_data, state, target_positions)).place(x=500, y=700)
    b_reset = tk.Button(window, text='RESET', command = reset).place(x=600, y=700)
    b_soft_rest = tk.Button(window, text='SOFT_RESET', command = soft_reset_for_ML).place(x=600, y=600)
    #b_freeze = tk.Button(window, text='FREEZE', command =freeze).place(x=700, y=700)
    #b_restart = tk.Button(window, text='RESTART', command =restart).place(x=800, y=700)
    print("load game")
    # exit()

    # AI_Sokoban(grids_data, box_positions, target_positions)
    # AI_Sokoban(grids_data, box_positions, target_positions)
    window.mainloop()
