#! /usr/bin/env python3
import numpy as np
import pygame
import sys
import rospy
from robot.msg import board, value_table
from utils import *
from v import Value


class Grid:

    def __init__(self) -> None:
        self.robot_x, self.robot_y = 0, 0
        self.dir = 0
        self.grid_size = [0, 0]
        self.grid = None
        self.is_init = False

        self.test_table = Value(self.grid_size)

        self.shape = NODE_RES*SCALE_RATE - 1
        self.vel = NODE_RES*SCALE_RATE

    def main(self):
        rospy.init_node('grid_node', anonymous=True)
        rospy.Subscriber('robot/cordinate', board, self.robot_cordinate_cb)
        rospy.Subscriber('robot/grid_value', value_table, self.value_table_cb)
        self.rate_30 = rospy.Rate(30)
        self.main_UI()

    def main_UI(self):
        while not rospy.is_shutdown():
            self.disp()
            self.rate_30.sleep()

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
            if np.abs(score)/self.test_table.goal_reward >= 1:
                pygame.draw.rect(self.win, BLUE,
                                    (self.vel*j+1, self.vel*i+1,
                                    self.shape, self.shape))
            else:
                color = 1 - np.abs(score)/self.test_table.goal_reward
                pygame.draw.rect(self.win, (255*color,
                                            255*color,
                                            255),
                                    (self.vel*j+1, self.vel*i+1,
                                    self.shape, self.shape))
        elif score == 0:
            pygame.draw.rect(self.win, WHITE,
                                (self.vel*j+1, self.vel*i+1,
                                self.shape, self.shape))
        else:
            color = 1 - score/(self.test_table.goal_reward)
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
        board = msg.table
        self.grid_size = [msg.height, msg.width]
        self.grid = np.reshape(board, self.grid_size)


if __name__ == '__main__':
    grid = Grid()
    grid.main()