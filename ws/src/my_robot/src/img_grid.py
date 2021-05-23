#! /usr/bin/env python3
import numpy as np
from cv_bridge import CvBridge
import cv2 as cv
import pygame
import sys
import rospy
from mobile_control import deep_mobile_control
from sensor_msgs.msg import Image
from my_robot.msg import board, next_move, board_cmd
from v import Value
from utils import *


class ImgGrid:

    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.colorful = True
        self.shape = NODE_RES*SCALE_RATE - 1
        self.vel = NODE_RES*SCALE_RATE

        self.bridge = CvBridge()

        self.robot = deep_mobile_control()
        self.robot.reset()
        self.action_dirs = [90, 270, 180, 0, 135, 45, 315, 225]
        self.robot_cor_val = [0, 0]
        self.robot_cor = [0, 0]
        self.goal_pos = [0, 0]
        self.dir_alpha = 0
        self.path = []
        self.ghost_reached_goal = False

        self.ghost_pos = [0, 0]

        self.is_init = False
        self.grid = None
        self.ground = None

        self.img = []

    def main(self):
        rospy.init_node('img_depth_node', anonymous=True)
        self.pub = rospy.Publisher('next_move_state', next_move, queue_size=1)
        rospy.Subscriber('/camera/depth/image_raw', Image, self.depth_callback)
        rospy.Subscriber('/robot_cor', board, self.robot_cor_cb)
        rospy.Subscriber('/board_control', board_cmd, self.board_cmd_cb)
        self.run()

    def run(self):
        rate = rospy.Rate(30)
        while not rospy.is_shutdown():
            self.pygame_event()
            if self.goal_pos[0] and self.goal_pos[1]:
                if self.table.update_count > 2*self.re_width:
                    if not self.ghost_reached_goal:
                        self.get_path()
                    if self.ghost_reached_goal:
                        try:
                            msg = next_move()
                            msg.x = self.path[1][1][0]
                            msg.y = self.path[1][1][1]
                            msg.dir = self.action_dirs[self.path[1][0]]
                            self.pub.publish(msg)
                            nst_x = self.path[1][1][0]
                            nst_y = self.path[1][1][1]
                            dif_1 = np.abs(nst_x - self.robot_cor_val[0])
                            dif_2 = np.abs(nst_y - self.robot_cor_val[1])
                            if dif_1 <= 0 and dif_2 <= 0:
                                print('reached goal')
                                self.path.pop(0)
                        except IndexError:
                            pass
                        if self.robot_cor_val[0] == self.goal_pos[0] and \
                                self.robot_cor_val[1] == self.goal_pos[1]:
                            print('REACHED GOAL')
                            self.reset(goal=True)
                else:
                    self.table.update(self.grid.copy())
            try:
                rate.sleep()
            except Exception:
                pass

    def draw_win(self):
        if not self.colorful:
            try:
                surf = pygame.surfarray.make_surface(self.img)
                self.win.blit(surf, (0, 0))
            except Exception:
                pass
        if self.is_init:
            if self.colorful:
                for i in range(self.re_height):
                    for j in range(self.re_width):
                        val = self.table.table.table[i][j].val
                        self.draw_table(val, i, j)
                self.draw_node(self.robot_cor_val, YELLOW)
            self.draw_grid()
        if self.goal_pos[0] and self.goal_pos[1]:
            self.draw_node(self.goal_pos, GREEN)
            if self.path.__len__() > 1:
                for i, item in enumerate(self.path):
                    if i == self.path.__len__() - 1:
                        break
                    st = item[1]
                    nst = self.path[i+1][1]
                    pygame.draw.line(self.win, RED,
                                    (st[1]*self.vel+self.vel/2,
                                    st[0]*self.vel+self.vel/2),
                                    (nst[1]*self.vel+self.vel/2,
                                    nst[0]*self.vel+self.vel/2), 5)
        pygame.display.flip()

    def board_cmd_cb(self, msg):
        self.reset()

    def robot_cor_cb(self, msg):
        self.robot_cor_val[0] = int(msg.robot_x)
        self.robot_cor_val[1] = int(msg.robot_y)
        self.dir_alpha = int(msg.robot_dir)
        self.draw_win()

    def depth_callback(self, msg):
        img = self.bridge.imgmsg_to_cv2(msg)
        cv.normalize(img, img, 0, 255, cv.NORM_MINMAX)
        self.re_width = int(img.shape[1] / SCALE_RATE / NODE_RES)
        self.re_height = int(img.shape[0] / SCALE_RATE / NODE_RES)
        image = cv.resize(img, (self.re_width * NODE_RES,
                                self.re_height * NODE_RES),
                          interpolation=cv.INTER_AREA)
        if not self.is_init:
            self.grid = np.zeros((self.re_height, self.re_width), dtype=int)
            self.is_init = True
            self.table = Value(size=(self.re_height, self.re_width))
            self.table.reset(self.grid.copy())
            self.ground = 130
            pygame.display.set_caption("GRID {}x{}".format(self.re_width,
                                                           self.re_height))
        if not self.colorful:
            self.img = cv.cvtColor(img.T, cv.COLOR_GRAY2RGB)
        for i in range(self.re_height):
            for j in range(self.re_width):
                pix_sum = self.get_data(image, j, i)
                if pix_sum:
                    self.grid[i][j] = 1
                else:
                    pass

    def pygame_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rospy.signal_shutdown("EXIT")
                self.run = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset(robot=True)
                elif event.key == pygame.K_c:
                    self.colorful = True if not self.colorful else False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cursor_pos = event.pos
                y = int(np.floor(cursor_pos[0] / self.vel)) # col
                x = int(np.floor(cursor_pos[1] / self.vel)) # row
                if self.grid[x, y] == 0:
                    self.path.clear()
                    self.grid[self.goal_pos[0], self.goal_pos[1]] = 0
                    self.goal_pos = [x, y]
                    self.grid[x, y] = 2
                    self.ghost_reached_goal = False
                    self.table.reset(self.grid.copy())
                elif self.grid[x, y] == 2:
                    self.reset(goal=True)

    def get_path(self):
        if self.path.__len__() == 0:
            self.ghost_pos = self.robot_cor_val
            self.path.append([99, self.robot_cor_val])
        move = self.table.getAction(self.ghost_pos)
        self.ghost_pos = move[1]
        self.path.append(move)
        if self.ghost_pos[0] == self.goal_pos[0] and \
                self.ghost_pos[1] == self.goal_pos[1]:
            self.ghost_reached_goal = True
    
    def reset(self, robot=False, goal=False):
        if robot:
            self.robot.reset()
        if robot or goal:
            self.grid[self.goal_pos[0], self.goal_pos[1]] = 0
            self.goal_pos = [0, 0]
            self.table.reset(self.grid.copy())
        self.path.clear()
        self.grid = np.zeros((self.re_height, self.re_width), dtype=int)
        self.ghost_reached_goal = False
        msg = next_move()
        msg.x = 0
        msg.y = 0
        msg.dir = 0
        self.pub.publish(msg)

    def get_data(self, img, w, h):
        for pix_1 in range(h*NODE_RES,
                           (h+1)*NODE_RES,
                            PIXEL_SKIP_RATE):
            for pix_2 in range(w*NODE_RES,
                               (w+1)*NODE_RES,
                                PIXEL_SKIP_RATE):
                if img[pix_1][pix_2] < self.ground:
                    return 1
        return 0

    def draw_grid(self):
        for i in range(self.re_width+1):
            pygame.draw.line(self.win, BLACK, (i*self.vel, 0),
                            (i*self.vel, self.re_height*self.vel))
        for i in range(self.re_height+1):
            pygame.draw.line(self.win, BLACK, (0, i*self.vel),
                            (self.re_width*self.vel, i*self.vel))

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
        else:
            color = 1 - score/(self.table.goal_reward)
            pygame.draw.rect(self.win, (255*color,
                                        255,
                                        255*color),
                                (self.vel*j+1, self.vel*i+1,
                                self.shape, self.shape))

if __name__ == '__main__':
    img_grid = ImgGrid()
    img_grid.main()
