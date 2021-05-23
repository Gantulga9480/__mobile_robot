import numpy as np


class Node:

    def __init__(self, cor) -> None:
        self.x = cor[0]
        self.y = cor[1]
        self.val = 0
        self.obs_dis = 0


class Nodes:

    def __init__(self, size) -> None:
        self.size = size
        self.table = []
        for i in range(size[0]):
            self.table.append([])
            for j in range(size[1]):
                self.table[i].append(Node([i, j]))
        assert self.table.__len__() == size[0]
    
    def reset(self):
        self.table.clear()
        for i in range(self.size[0]):
            self.table.append([])
            for j in range(self.size[1]):
                self.table[i].append(Node([i, j]))
        assert self.table.__len__() == self.size[0]

class Value:

    def __init__(self, size) -> None:
        self.size = size
        self.table = Nodes(size)
        self.goal_reward = 200
        self.obs_reward = -100
        self.step_rew = 0
        self.gamma = 0.9
        self.update_rate = 10
        self.update_count = 0

    def reset(self, board):
        self.update_count = 0
        self.init_table(board)
        self.update(board, reset=True)

    def update(self, board, reset=False, ur=None):
        if ur is None:
            pass
        else:
            self.update_rate = ur
        temp_value = self.table.table.copy()
        itr = 0
        if reset:
            itr = self.update_rate
        else:
            itr = 1
        for _ in range(itr):
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    if board[i][j] == 1:
                        temp_value[i][j].val = self.obs_reward
                    elif board[i][j] == 2:
                        temp_value[i][j].val = self.goal_reward
                    else:
                        temp_value[i][j].val = self.getStateVal([i, j])
            self.table.table = temp_value.copy()
            self.update_count += 1

    def getAction(self, state):
        next_state = [[state[0]-1, state[1]], [state[0]+1, state[1]],
                      [state[0], state[1]-1], [state[0], state[1]+1],
                      [state[0]-1, state[1]-1], [state[0]-1, state[1]+1],
                      [state[0]+1, state[1]+1], [state[0]+1, state[1]-1]]
        vals = []
        for i, item in enumerate(next_state):
            try:
                if item[0] >= 0 and item[1] >= 0:
                    vals.append(self.table.table[item[0]][item[1]].val)
                else:
                    vals.append(self.obs_reward)
            except IndexError:
                vals.append(self.obs_reward)
        i = np.argmax(vals)
        cor = next_state[i]
        return [i, cor]

    def getStateVal(self, state):
        next_state_ = [[state[0]-1, state[1]], [state[0], state[1]+1],
                       [state[0], state[1]-1], [state[0]+1, state[1]]]

        next_state = [[state[0]-1, state[1]], [state[0]+1, state[1]],
                      [state[0], state[1]-1], [state[0], state[1]+1],
                      [state[0]-1, state[1]-1], [state[0]-1, state[1]+1],
                      [state[0]+1, state[1]+1], [state[0]+1, state[1]-1]]
        vals = []
        is_negative = False
        dists = []
        for i, item in enumerate(next_state):
            try:
                if item[0] >= 0 and item[1] >= 0:
                    val = self.table.table[item[0]][item[1]].val
                    if val == self.obs_reward and not is_negative:
                        self.table.table[state[0]][state[1]].obs_dis = 1
                        is_negative = True
                    elif self.table.table[item[0]][item[1]].obs_dis > 0 and \
                            not is_negative:
                        dists.append(self.table.table[item[0]][item[1]].obs_dis)
                    vals.append(self.gamma*val + self.step_rew)
                else:
                    pass
            except IndexError:
                pass
        if len(dists) > 0 and not is_negative:
            self.table.table[state[0]][state[1]].obs_dis = np.min(dists) + 1
        if self.table.table[state[0]][state[1]].obs_dis <= 1:
            return np.mean(vals)    
        else:
            return np.max(vals)

    def init_table(self, board):
        self.table = Nodes(self.size)
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if board[i][j] == 1:
                    self.table.table[i][j].val = self.obs_reward
                elif board[i][j] == 2:
                    self.table.table[i][j].val = self.goal_reward