#! /usr/bin/env python3
import rospy
import numpy as np
import cv2 as cv
import math

from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from my_robot.msg import board
from utils import *

x = 0
y = 0
dir_alpha = 0

def rgb_callback(msg):
    global x, y, dir_alpha
    ball_center = []
    robot_cor = []
    img = bridge.imgmsg_to_cv2(msg)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # gray = cv.medianBlur(gray, 5)
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 1,
                              param1=50, param2=10,
                              minRadius=4, maxRadius=5)
    robot = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 1,
                            param1=30, param2=25,
                            minRadius=19, maxRadius=20)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            ball_center.append(i[0])
            ball_center.append(i[1])
            # cv.circle(img, tuple(ball_center), i[2], (255, 0, 255), 1)
            break
    if robot is not None:
        robot = np.uint16(np.around(robot))
        for i in robot[0, :]:
            robot_cor.append(i[0])
            robot_cor.append(i[1])
            x, y = int(i[1]//(SCALE_RATE*NODE_RES)),\
                int(i[0]//(SCALE_RATE*NODE_RES))
            # cv.circle(img, tuple(robot_cor), i[2], (255, 0, 255), 1)
            break
    try:
        dir_vect = [int(robot_cor[0]) - int(ball_center[0]),
                    int(robot_cor[1]) - int(ball_center[1])]
        if dir_vect[0] > 0 and dir_vect[1] <= 0:
            dir_alpha = \
                math.atan(-dir_vect[1]/dir_vect[0]) / math.pi * 180
        elif dir_vect[0] > 0 and dir_vect[1] > 0:
            dir_alpha = 360 + \
                math.atan(-dir_vect[1]/dir_vect[0]) / math.pi * 180
        elif dir_vect[0] < 0 and dir_vect[1] >= 0:
            dir_alpha = \
                math.atan(-dir_vect[1]/dir_vect[0]) / math.pi * 180 + 180
        elif dir_vect[0] < 0 and dir_vect[1] < 0:
            dir_alpha = \
                math.atan(-dir_vect[1]/dir_vect[0]) / math.pi * 180 + 180
        elif dir_vect[0] == 0 and dir_vect[1] < 0:
            dir_alpha = 90
        elif dir_vect[0] == 0 and dir_vect[1] > 0:
            dir_alpha = 270
        # cv.line(img, tuple(ball_center),
        #     tuple(robot_cor), (255, 0, 0), 3)
        # cv.imshow('dst_rt', img)
        # cv.waitKey(1)
    except IndexError:
        pass


def main():
    rospy.init_node('robot_cor_node', anonymous=True)
    rospy.Subscriber('/camera/color/image_raw', Image, rgb_callback)
    rate = rospy.Rate(30)
    pub = rospy.Publisher('robot_cor', board, queue_size=1)
    print('robot_cor_node start')
    while not rospy.is_shutdown():
        if x and y:
            msg = board()
            msg.robot_x = x
            msg.robot_y = y
            msg.robot_dir = int(dir_alpha)
            pub.publish(msg)
        try:
            rate.sleep()
        except Exception:
            pass


if __name__ == '__main__':
    bridge = CvBridge()
    main()
