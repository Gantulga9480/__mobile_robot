#! /usr/bin/env python3
from utils import *
from sensor_msgs.msg import Image
from robot.msg import value_table
import rospy
import numpy as np
from cv_bridge import CvBridge
import cv2 as cv
from v import Value


class DepthGrid:

    def __init__(self) -> None:
        self.is_init = False
        self.colorful = False
        self.ground = 100
        self.bridge = CvBridge()

    def depth_cb(self, msg):
        img = self.bridge.imgmsg_to_cv2(msg)
        cv.normalize(img, img, 0, 255, cv.NORM_MINMAX)
        img_rgb = cv.cvtColor(img, cv.COLOR_GRAY2RGB).astype(np.uint8)
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
        for i in range(self.re_height):
            for j in range(self.re_width):
                pix_sum = self.get_data(image, j, i)
                if pix_sum:
                    self.grid[i][j] = 1
                else:
                    self.grid[i][j] = 0
        cv.imshow('Depth', img_rgb)
        cv.waitKey(1)

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

    def value(self):
        while not rospy.is_shutdown():
            try:
                self.table.update(self.grid.copy())
                msg = value_table()
                msg.width = self.re_width
                msg.height = self.re_height
                msg.table = self.table.getValue().flatten()
                self.pub.publish(msg)
            except AttributeError:
                ...
            self.rate.sleep()

    def main(self):
        rospy.init_node('img_depth_node', anonymous=True)
        rospy.Subscriber('/camera/depth/image', Image, self.depth_cb)
        self.pub = rospy.Publisher('robot/grid_value', value_table, queue_size=1)
        self.rate = rospy.Rate(10)
        self.value()

if __name__ == "__main__":
    depth = DepthGrid()
    depth.main()
