#! /usr/bin/env python3
import numpy as np
import pygame
import rospy
import sys
from robot.msg import board
from std_msgs.msg import Int32MultiArray
from utils import *
from v import Value


class Grid:

    def __init__(self) -> None:
        self.robot_x, self.robot_y = 0, 0
        self.dir = 0
        self.grid_size = [24, 32]
        self.grid = None
        self.is_init = False

        self.table = Value(self.grid_size)
        self.path = []

        self.goal_pos = [0, 0]

        self.ghost_reached_goal = False

        self.shape = NODE_RES*SCALE_RATE - 1
        self.vel = NODE_RES*SCALE_RATE

    def main(self):
        rospy.init_node('grid_node', anonymous=True)
        rospy.Subscriber('robot/cordinate', board, self.robot_cordinate_cb)
        rospy.Subscriber('robot/grid_value', Int32MultiArray, self.value_table_cb)
        self.rate_30 = rospy.Rate(30)
        self.main_UI()

    def main_UI(self):
        while not rospy.is_shutdown():
            self.disp()
            self.pygame_event()
            if self.goal_pos[0] and self.goal_pos[1]:
                if self.table.update_count > 2*self.grid_size[1]:
                    if not self.ghost_reached_goal:
                        self.get_path()
                    if self.ghost_reached_goal:
                        try:
                            # msg = next_move()
                            # msg.x = self.path[1][1][0]
                            # msg.y = self.path[1][1][1]
                            # msg.dir = self.action_dirs[self.path[1][0]]
                            # self.pub.publish(msg)
                            nst_x = self.path[1][1][0]
                            nst_y = self.path[1][1][1]
                            dif_1 = np.abs(nst_x - self.robot_x)
                            dif_2 = np.abs(nst_y - self.robot_y)
                            if dif_1 <= 0 and dif_2 <= 0:
                                print('reached goal')
                                self.path.pop(0)
                        except IndexError:
                            pass
                        if self.robot_x == self.goal_pos[0] and \
                                self.robot_y == self.goal_pos[1]:
                            print('REACHED GOAL')
                            self.reset(goal=True)
                else:
                    # self.table.update(self.grid.copy())
                    # self.table.reset(self.grid.copy())
                    pass
            try:
                self.table.update(self.grid.copy())
                # self.table.reset(self.grid.copy())
            except AttributeError:
                pass
            try:
                self.rate_30.sleep()
            except Exception:
                pass

    def get_path(self):
        if self.path.__len__() == 0:
            self.ghost_pos = [self.robot_x, self.robot_y]
            self.path.append([99, [self.robot_x, self.robot_y]])
        move = self.table.getAction(self.ghost_pos)
        self.ghost_pos = move[1]
        self.path.append(move)
        if self.ghost_pos[0] == self.goal_pos[0] and \
                self.ghost_pos[1] == self.goal_pos[1]:
            self.ghost_reached_goal = True

    def reset(self, robot=False, goal=False):
        if robot:
            # self.robot.reset()
            pass
        if robot or goal:
            self.grid[self.goal_pos[0], self.goal_pos[1]] = 0
            self.goal_pos = [0, 0]
            self.table.reset(self.grid.copy())
        self.path.clear()
        self.grid = np.zeros((self.grid_size[0], self.grid_size[1]), dtype=int)
        self.ghost_reached_goal = False
        # msg = next_move()
        # msg.x = 0
        # msg.y = 0
        # msg.dir = 0
        # self.pub.publish(msg)

    def disp(self):
        if not self.is_init:
            self.is_init = True
            self.win = pygame.display.set_mode((640, 480))
            pygame.display.set_caption(f'{self.grid_size[1]}x{self.grid_size[0]}')
        else:
            for i in range(self.grid_size[0]):
                for j in range(self.grid_size[1]):
                    val = self.grid[i][j]
                    self.draw_table(val, i, j)
            self.draw_node((self.robot_x, self.robot_y), YELLOW)
            self.draw_grid()
            pygame.display.flip()

    def pygame_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rospy.signal_shutdown("EXIT")
                self.run = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # self.reset(robot=True)
                    ...
                elif event.key == pygame.K_c:
                    self.colorful = True if not self.colorful else False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cursor_pos = event.pos
                y = int(np.floor(cursor_pos[0] / self.vel)) # col
                x = int(np.floor(cursor_pos[1] / self.vel)) # row
                if self.grid[x, y] == 0:
                    # self.path.clear()
                    self.grid[self.goal_pos[0], self.goal_pos[1]] = 0
                    self.goal_pos = [x, y]
                    self.grid[x, y] = 2
                    self.ghost_reached_goal = False
                    # self.table.reset(self.grid.copy())
                elif self.grid[x, y] == 2:
                    self.reset(goal=True)

    def draw_grid(self):
        for i in range(self.grid_size[1]+1):
            pygame.draw.line(self.win, BLACK, (i*self.vel, 0),
                            (i*self.vel, self.grid_size[0]*self.vel))
        for i in range(self.grid_size[0]+1):
            pygame.draw.line(self.win, BLACK, (0, i*self.vel),
                            (self.grid_size[1]*self.vel, i*self.vel))

    def draw_node(self, pos, color):
        pygame.draw.rect(self.win, color,
                         (self.vel*pos[1], self.vel*pos[0],
                          self.vel, self.vel))

    def draw_table(self, score, i, j):
        if score < 0:
            if np.abs(score)/self.table.goal_reward >= 1:
                pygame.draw.rect(self.win, BLUE,
                                    (self.vel*j+1, self.vel*i+1,
                                    self.shape, self.shape))
            else:
                color = 1 - np.abs(score)/self.table.goal_reward
                pygame.draw.rect(self.win, (255*color,
                                            255*color,
                                            255),
                                    (self.vel*j+1, self.vel*i+1,
                                    self.shape, self.shape))
        elif score == 0:
            pygame.draw.rect(self.win, WHITE,
                                (self.vel*j+1, self.vel*i+1,
                                self.shape, self.shape))
        elif score == 1:
            pygame.draw.rect(self.win, BLACK,
                                (self.vel*j+1, self.vel*i+1,
                                self.shape, self.shape))
        else:
            color = 1 - score/(self.table.goal_reward)
            pygame.draw.rect(self.win, (255*color,
                                        255,
                                        255*color),
                                (self.vel*j+1, self.vel*i+1,
                                self.shape, self.shape))

    def robot_cordinate_cb(self, msg):
        self.robot_x = int(msg.robot_x)
        self.robot_y = int(msg.robot_y)
        self.dir = int(msg.robot_dir)

    def value_table_cb(self, msg):
        board = msg.data
        self.grid = np.reshape(board, self.grid_size)


if __name__ == '__main__':
    grid = Grid()
    grid.main()