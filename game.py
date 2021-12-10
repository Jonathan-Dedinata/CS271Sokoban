
import block
import tkinter as tk
import tkinter.messagebox
import time
from RL import QLearning
from copy import deepcopy
import platform
import pprint
import pandas as pd

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

class control:
    def __init__(self):
        self.gamma  = -1
        self.lr = -1
        self.p = -1
        self.freeze_flag = False
        self.T1 = time.time()
        self.T2 = -1
        self.p_qtable = pd.DataFrame()
    def get_t2(self):
        self.T2 = time.time()
    def set_gamma(self,g):
        self.gamma = g
    def set_p(self,p):
        self.p = p
    def set_lr(self,lr):
        self.lr = lr

    def print_parameters(self):
        return "    gemma: "+str(self.gamma) + "    learning rate: "+str(self.p) +"    probility: "+ str(self.lr)

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
        state.append([self.player_x, self.player_y])
        for i in range(1, self.h + 1):
            for j in range(1, self.v + 1):
                if self.board[i, j].is_box():
                    state.append([i, j])
        

        return state

    def Manhattan_Dis(self, x, y):
        return abs(x[0] - y[0]) + abs(x[1] - y[1])

    def evaluateAction(self, action, target, totalSteps, occupiedList):
        old_state = self.getState()
        if(action == 1):
            left('')
        elif(action == 2):
            up('')
        elif(action == 3):
            right('')
        elif(action == 4):
            down('')
        new_state = self.getState()
        finished = True
        stuck = False
        badMove = False
        reward = 0

        # for i in range(len(target)):
        #     if self.board[target[i][0], target[i][1]].is_box():
        #         occupiedList.append(1)
        #     else:
        #         occupiedList.append(0)
        for i in range(1, len(target) + 1):
            r = 100000
            if (new_state[i][0], new_state[i][1]) in occupiedList:
                if occupiedList[new_state[i][0], new_state[i][1]] == True:
                    continue
            for j in range(len(target)):
                if occupiedList[target[j][0], target[j][1]] == True:
                    continue
                r = min(r, self.Manhattan_Dis(new_state[i], target[j]))
            # print("r", i, " = ", r)
            # print(" r2 = ", r)
            # print(" r3 = ", r)
            # print("\n")
            if r == 0:
                reward += 200
            else:
                # print("test")
                finished = False
                # reward -= r
                # reward += round(10 / r, 2)
            # some problem
            # if old_state == new_state:
            #     reward -= 1000
            #     finished = False
            # elif r == 0:
            #     reward += 50
            # else:
            #     finished = False
            #     reward -= r

        for i in range(1, len(target) + 1):
            x, y = new_state[i][0], new_state[i][1]
            if self.board[x, y].is_target():
                occupiedList[x, y] = True
            else:
                # occupiedList[x, y] = False
                if self.board[x - 1, y].is_wall() and self.board[x, y + 1].is_wall(): stuck = True
                if self.board[x, y + 1].is_wall() and self.board[x + 1, y].is_wall(): stuck = True
                if self.board[x + 1, y].is_wall() and self.board[x, y - 1].is_wall(): stuck = True
                if self.board[x, y - 1].is_wall() and self.board[x - 1, y].is_wall(): stuck = True

                if self.board[x - 1, y].is_box() and self.board[x, y + 1].is_wall(): stuck = True
                if self.board[x, y + 1].is_box() and self.board[x + 1, y].is_wall(): stuck = True
                if self.board[x + 1, y].is_box() and self.board[x, y - 1].is_wall(): stuck = True
                if self.board[x, y - 1].is_box() and self.board[x - 1, y].is_wall(): stuck = True

                if self.board[x - 1, y].is_wall() and self.board[x, y + 1].is_box(): stuck = True
                if self.board[x, y + 1].is_wall() and self.board[x + 1, y].is_box(): stuck = True
                if self.board[x + 1, y].is_wall() and self.board[x, y - 1].is_box(): stuck = True
                if self.board[x, y - 1].is_wall() and self.board[x - 1, y].is_box(): stuck = True
        if stuck:
            reward -= 1000
        if badMove:
            reward -= 10

        # for i in range(len(target)):
        #     r = 1000
        #     for j in range(len(target)):
        #         if occupiedList[j] != 1:
        #             r = min(r, self.Manhattan_Dis(new_state[i], target[j]))
        #         else: break
        #     # some problem
        #     # if old_state == new_state:
        #     #     reward -= 1000
        #     #     finished = False
        #     # elif r == 0:
        #     #     reward += 50
        #     # else:
        #     #     finished = False
        #     #     reward -= r
        #     if occupiedList[j] == 1: break

        if old_state == new_state:
            reward -= 5
        if finished:
            # print("yes")
            reward += 10000
        # reward -= 1 * totalSteps
        print("reward = ", reward)
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
    file_name = input("enter file name")
    try:
        f = open(file_name + "_result")
        f.close()
    except IOError:
        f = open(file_name + "_result", 'w')
        config = {platform.machine(),platform.version(),platform.platform(),platform.uname(),platform.processor()}
        config = pprint.pformat(config) + "\n"
        f.write(str(config))
        f.flush()
        f.close()



    result = open(file_name + "_result",'a')


    data, grids_data, box_positions, target_positions, v, h, n, x, y = read_input(file_name)
    #"sokoban01.txt"
    # print("data = ", data)
    # print("grids_data = ", grids_data)
    # print("v = ", v)
    # print("h = ", h)
    # print("n = ", n)
    # print("x = ", x)
    # print("y = ", y)
    # print("states = ", box_positions)
    # exit()

    window = tk.Tk()

    window.title('game')

    window.geometry('800x800')

    canvas = tk.Canvas(window, bg='white', height=600, width=600)

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
    control_box = control()
    agent = QLearning()
    def AI_Sokoban(grids, state, target,lr,gamma,p,r):

        agent.learning_rate = lr
        agent.gamma = gamma
        agent.possibility = p
        control_box.p = p
        control_box.gamma = gamma
        control_box.lr = lr
        control_box.freeze_flag = False
        control_box.T1  = time.time()
        if r:
            agent.q_table = control_box.p_qtable.copy(deep=True)

        for episode in range(100000):
            if control_box.freeze_flag:
                break
            occupiedList = {}
            for i in range(len(target)):
                occupiedList[target[i][0], target[i][1]] = False
            print("episode ", episode)
            soft_reset_for_ML()
            totalSteps = 0
            preAction = 0
            success_times = 0
            while True:
                # print(state)
                if control_box.freeze_flag:
                    break
                action = agent.chooseAction(state, preAction, totalSteps, success_times)
                totalSteps = totalSteps + 1
                next_state, reward, finished, stuck = g.evaluateAction(action, target, totalSteps,occupiedList)
                if finished:
                    success_times += 1
                    break
                agent.Q_learning(str(state), action, reward, str(next_state), finished)
                state = next_state
                preAction = action
                if totalSteps > 2000 or stuck:
                    break
                # time.sleep(0.00005)

        #         print('currSteps = ', totalSteps)
        # print('totalSteps = ', totalSteps)


    def up(e):
        g.step(1)
        draw(canvas, g.board, g.player_x, g.player_y)
        canvas.update()
        print("up")
        if g.number_of_box == g.number_of_box_on_target:
            control_box.T2 = time.time()
            result.write(str((control_box.T2 - control_box.T1))+control_box.print_parameters()+"\n")
            result.flush()
            tk.messagebox.showinfo("result", "Successful, it takes" + str((control_box.T2 - control_box.T1))+ "  seconds")
            control_box.p_qtable = agent.q_table.copy(deep=True)
            reset()
        return canvas


    def down(e):
        g.step(2)
        draw(canvas, g.board, g.player_x, g.player_y)
        canvas.update()
        print("down")
        if g.number_of_box == g.number_of_box_on_target:
            control_box.T2 = time.time()
            result.write(str((control_box.T2 - control_box.T1))+control_box.print_parameters()+"\n")
            result.flush()
            tk.messagebox.showinfo("result", "Successful, it takes" + str((control_box.T2 - control_box.T1))+ "  seconds")
            control_box.p_qtable = agent.q_table.copy(deep=True)
            reset()
        return canvas


    def left(e):
        g.step(3)
        draw(canvas, g.board, g.player_x, g.player_y)
        canvas.update()
        print("left")
        if g.number_of_box == g.number_of_box_on_target:
            control_box.T2 = time.time()
            result.write(str((control_box.T2 - control_box.T1))+control_box.print_parameters()+"\n")
            result.flush()
            tk.messagebox.showinfo("result", "Successful, it takes" + str((control_box.T2 - control_box.T1))+ "  seconds")
            control_box.p_qtable = agent.q_table.copy(deep=True)
            reset()
        return canvas


    def right(e):
        g.step(4)
        draw(canvas, g.board, g.player_x, g.player_y)
        canvas.update()
        print("right")
        if g.number_of_box == g.number_of_box_on_target:
            control_box.T2 = time.time()
            result.write(str((control_box.T2 - control_box.T1))+control_box.print_parameters()+'\n')
            result.flush()
            tk.messagebox.showinfo("result", "Successful, it takes  " + str((control_box.T2 - control_box.T1)) + "  seconds")
            control_box.p_qtable = agent.q_table.copy(deep=True)
            reset()
        return canvas


    def reset():
        control_box.freeze_flag = True
        control_box.T1 = time.time()
        g.reset()
        draw(canvas, g.board, g.player_x, g.player_y)
        canvas.update()

    def soft_reset_for_ML():
        g.reset()
        #control_box.T1 = time.time()
        draw(canvas, g.board, g.player_x, g.player_y)
        canvas.update()




    state = g.getState()
    f = tk.Frame()
    f.pack()




    f1 = tk.Frame()
    f1.pack()
    L1 = tk.Label(f1, text="learning_rate")
    L1.pack(side='left')
    E1 = tk.Entry(f1, bd=5)
    E1.pack(side='right')

    f2 = tk.Frame()
    f2.pack()
    L2 = tk.Label(f2, text="gamma")
    L2.pack(side='left')
    E2 = tk.Entry(f2, bd=5)
    E2.pack(side='right')

    f3 = tk.Frame()
    f3.pack()
    L3 = tk.Label(f3, text="possibility")
    L3.pack(side='left')
    E3 = tk.Entry(f3, bd=5)
    E3.pack(side='right')

    b_run_ = tk.Button(f, text='RUN', command=lambda: AI_Sokoban(grids_data, state, target_positions,float(E1.get()),float(E2.get()),float(E3.get()),False )).pack()
    b_run_p = tk.Button(f, text='RUN_WITH_PREVIOUS_Qtable',
                       command=lambda: AI_Sokoban(grids_data, state, target_positions, float(E1.get()), float(E2.get()),
                                                  float(E3.get()),True)).pack()
    b_reset_ = tk.Button(f, text='RESET', command=reset).pack()
    #b_soft_rest_ = tk.Button(f, text='SOFT_RESET', command=soft_reset_for_ML).pack()


   # b_run = tk.Button(window, text='RUN', command=lambda :AI_Sokoban(grids_data, state, target_positions)).place(x=500, y=700)
    #b_reset = tk.Button(window, text='RESET', command = reset).place(x=600, y=700)
    #b_soft_rest = tk.Button(window, text='SOFT_RESET', command = soft_reset_for_ML).place(x=600, y=600)

    window.bind('<Up>',up)
    window.bind('<Down>', down)
    window.bind('<Left>', left)
    window.bind('<Right>', right)
    #b_freeze = tk.Button(window, text='FREEZE', command =freeze).place(x=700, y=700)
    #b_restart = tk.Button(window, text='RESTART', command =restart).place(x=800, y=700)
    print("load game")
    # exit()

    # AI_Sokoban(grids_data, box_positions, target_positions)
    # AI_Sokoban(grids_data, box_positions, target_positions)
    window.mainloop()
