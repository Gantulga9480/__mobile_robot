#! /usr/bin/env python3
from pickle import FALSE
import numpy as np
from cv_bridge import CvBridge
import cv2 as cv
import rospy
import math
from robot.msg import board
from sensor_msgs.msg import Image
from utils import *


class ImgDisp:

    def __init__(self):
        self.bridge = CvBridge()
        self.x = 0
        self.y = 0
        self.dir_alpha = 0

        self.x_val_tmp = 0
        self.y_val_tmp = 0
        self.is_placed = False

        self.x_ball_tmp = 0
        self.y_ball_tmp = 0
        self.is_ball_placed = False

    def rgb_callback(self, msg):
        ball_center = []
        robot_cor = []
        img = self.bridge.imgmsg_to_cv2(msg)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray = cv.medianBlur(gray, 5)
        circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 1,
                                  param1=150, param2=5,
                                  minRadius=10, maxRadius=11)
        robot = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 1,
                                param1=150, param2=5,
                                minRadius=34, maxRadius=35)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                if self.is_ball_placed:
                    if self.x_ball_tmp - 10 < i[1] < self.x_ball_tmp + 10:
                        if self.y_ball_tmp - 10 < i[0] < self.y_ball_tmp + 10:
                            ball_center.append(i[0])
                            ball_center.append(i[1])
                            self.x_ball_tmp = i[1]
                            self.y_ball_tmp = i[0]
                            cv.circle(img, tuple(ball_center), i[2], (255, 0, 255), 1)
                            break
                else:
                    self.is_ball_placed = True
                    ball_center.append(i[0])
                    ball_center.append(i[1])
                    self.x_ball_tmp = i[1]
                    self.y_ball_tmp = i[0]
                    cv.circle(img, tuple(ball_center), i[2], (255, 0, 255), 1)
                    break
        if robot is not None:
            robot = np.uint16(np.around(robot))
            for i in robot[0, :]:
                if self.is_placed:
                    if self.x_val_tmp - 20 < i[1] < self.x_val_tmp + 20:
                        if self.y_val_tmp - 20 < i[0] < self.y_val_tmp + 20:
                            robot_cor.append(i[0])
                            robot_cor.append(i[1])
                            self.x_val_tmp = i[1]
                            self.y_val_tmp = i[0]
                            self.x, self.y = int(i[1]//(SCALE_RATE*NODE_RES)),\
                                int(i[0]//(SCALE_RATE*NODE_RES))
                            cv.circle(img, tuple(robot_cor), i[2], (255, 0, 255), 1)
                            break
                else:
                    self.is_placed = True
                    robot_cor.append(i[0])
                    robot_cor.append(i[1])
                    self.x_val_tmp = i[1]
                    self.y_val_tmp = i[0]
                    self.x, self.y = int(i[1]//(SCALE_RATE*NODE_RES)),\
                        int(i[0]//(SCALE_RATE*NODE_RES))
                    cv.circle(img, tuple(robot_cor), i[2], (255, 0, 255), 1)
                    break
        try:
            dir_vect = [int(robot_cor[0]) - int(ball_center[0]),
                        int(robot_cor[1]) - int(ball_center[1])]
            if dir_vect[0] > 0 and dir_vect[1] <= 0:
                self.dir_alpha = \
                    math.atan(-dir_vect[1]/dir_vect[0]) / math.pi * 180
            elif dir_vect[0] > 0 and dir_vect[1] > 0:
                self.dir_alpha = 360 + \
                    math.atan(-dir_vect[1]/dir_vect[0]) / math.pi * 180
            elif dir_vect[0] < 0 and dir_vect[1] >= 0:
                self.dir_alpha = \
                    math.atan(-dir_vect[1]/dir_vect[0]) / math.pi * 180 + 180
            elif dir_vect[0] < 0 and dir_vect[1] < 0:
                self.dir_alpha = \
                    math.atan(-dir_vect[1]/dir_vect[0]) / math.pi * 180 + 180
            elif dir_vect[0] == 0 and dir_vect[1] < 0:
                self.dir_alpha = 90
            elif dir_vect[0] == 0 and dir_vect[1] > 0:
                self.dir_alpha = 270
            cv.line(img, tuple(ball_center), tuple(robot_cor), (255, 0, 0), 3)
            cv.imshow('dst_rt', img)
            cv.waitKey(1)
        except IndexError:
            pass

    def codir(self):
        ...

    def main(self):
        rospy.init_node('img_rgb_node', anonymous=True)
        rospy.Subscriber('/camera/rgb/image_color', Image, self.rgb_callback)
        rate = rospy.Rate(15)
        pub = rospy.Publisher('robot/cordinate', board, queue_size=1)
        while not rospy.is_shutdown():
            if self.x and self.y:
                msg = board()
                msg.robot_x = self.x
                msg.robot_y = self.y
                msg.robot_dir = int(self.dir_alpha)
                pub.publish(msg)
            try:
                rate.sleep()
            except Exception:
                pass


if __name__ == '__main__':
    img_disp = ImgDisp()
    img_disp.main()