import numpy as np
import pandas as pd
import random

class QLearning:

    def __init__(self, _learning_rate=0.2, _gamma=0.8, _possibility=0.85):
        self.actions = [1, 2, 3, 4]  # a list
        self.learning_rate = _learning_rate
        self.gamma = _gamma
        self.possibility = _possibility
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def chooseAction(self, state, preAction, totalSteps):
        # action = 1
        self.checkQTable(state)
        # if totalSteps > 1000: p = 0.7
        # elif totalSteps > 500: p = 0.8
        # else: p = self.possibility
        p = self.possibility
        if(random.random() < p):
            actions = self.q_table.loc[state, :]
            action = np.random.choice(actions[actions == actions.max()].index)
        else:
            action = np.random.choice(self.actions)
        # if abs(action - preAction) == 2:
        #     action = np.random.choice(self.actions)
        return action
    
    def Q_learning(self, state, action, reward, next_state, finished):
        # nextQ = -100000
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
            