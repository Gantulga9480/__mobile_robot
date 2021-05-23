import numpy as np
from cv_bridge import CvBridge
import cv2 as cv
import rospy
from sensor_msgs.msg import Image


class ImgDisp:

    def __init__(self):
        self.bridge = CvBridge()

    def callback(self, msg):
        img = self.bridge.imgmsg_to_cv2(msg)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray = cv.medianBlur(gray, 5)
        rows = gray.shape[0]
        circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 1,
                                  param1=50, param2=10,
                                  minRadius=4, maxRadius=5)
        robot = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 1,
                                  param1=30, param2=25,
                                  minRadius=19, maxRadius=20)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # print('circle', (i[0], i[1]))
                center = (i[0], i[1])
                # cv.circle(img, center, 1, (0, 100, 100), 3)
                radius = i[2]
                cv.circle(img, center, radius, (255, 0, 255), 1)
        if robot is not None:
            robot = np.uint16(np.around(robot))
            for i in robot[0, :]:
                # print('robot', (i[0], i[1]))
                center = (i[0], i[1])
                # cv.circle(img, center, 1, (0, 100, 100), 3)
                radius = i[2]
                cv.circle(img, center, radius, (255, 0, 255), 1)
        cv.imshow('dst_rt', img)
        cv.waitKey(1)

    def main(self):
        rospy.init_node('img_disp_node')
        rospy.Subscriber('/camera/color/image_raw', Image, self.callback)
        rospy.spin()


if __name__ == '__main__':
    img_disp = ImgDisp()
    img_disp.main()
