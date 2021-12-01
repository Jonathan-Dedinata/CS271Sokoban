import numpy as np
import pandas as pd
import random

class QLearning:

    def __init__(self, learning_rate=0.1, reward_decay=0.9, e_greedy=0.8):
        self.actions = [1, 2, 3, 4]  # a list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def chooseAction(self, state):
        # action = 1
        self.checkQTable(state)
        if(random.random() < self.epsilon):
            actions = self.q_table.loc[state, :]
            action = np.random.choice(actions[actions == actions.max()].index)
        else:
            action = np.random.choice(self.actions)
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
        self.q_table.loc[state, action] += self.lr * (nextQ - curQ)

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
            