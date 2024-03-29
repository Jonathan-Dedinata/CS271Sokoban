import numpy as np
import pandas as pd
import random

class QLearning:

    def __init__(self, _learning_rate=0.1, _gamma=0.9, _possibility=0.85):
        self.actions = [1, 2, 3, 4]  # a list
        self.learning_rate = _learning_rate
        self.gamma = _gamma
        self.possibility = _possibility
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def chooseAction(self, state, preAction, totalSteps, success_times):
        self.checkQTable(str(state))
        # up_state = state
        # down_state = state
        # left_state = state
        # right_state = state
        # up_state[0][0] += 1
        # down_state[0][0] -= 1
        # right_state[0][1] += 1
        # left_state[0][1] -= 1
        # self.checkQTable(str(up_state))
        # self.checkQTable(str(down_state))
        # self.checkQTable(str(right_state))
        # self.checkQTable(str(left_state))
        p = self.possibility + 0.01 * success_times
        if(random.random() < p):
            actions = self.q_table.loc[str(state), :]
            action = np.random.choice(actions[actions == actions.max()].index)
        else:
            action = np.random.choice(self.actions)
        # if abs(action - preAction) == 2:
        #     action = np.random.choice(self.actions)
        return action

    def Q_learning(self, state, action, reward, next_state, finished):
        self.checkQTable(next_state)
        if not finished:
            nextQ = reward + self.gamma * self.q_table.loc[next_state, :].max()
        else:
            nextQ = reward
        # print(self.q_table[state, action])
        curQ = self.q_table.loc[state, action]
        self.q_table.loc[state, action] += self.learning_rate * (nextQ - curQ)

    def checkQTable(self, state):
        # print(state)
        # print(self.q_table.index)
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state
                )
            )

    def getQTableSize(self):
        return self.q_table.size
