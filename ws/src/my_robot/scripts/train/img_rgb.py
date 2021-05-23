import numpy as np
from cv_bridge import CvBridge
import cv2
import pygame
import rospy
from PIL import Image as pil_img
from sensor_msgs.msg import Image

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 177, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

NODE_RES = 20
PIXEL_SKIP_RATE = 10

OBS_HEIGHT = 0.5
CAMERA_HEIGHT = 3

WIN_WIDTH = 640
WIN_HEIGHT = 480


class ImgGrid:

    def __init__(self):
        pygame.init()
        self.bridge = CvBridge()
        self.clock = pygame.time.Clock()
        self.robot_pos = (30, 20)
        self.is_init = False
        self.grid = None
        self.win = None
        self.grid_height = 0
        self.grid_width = 0
        self.fps = 30
        self.shape = NODE_RES - 1
        self.vel = NODE_RES
        self.ground = None
        self.robot_color = None
        # self.pub = rospy.Publisher('/robot_cordinate', board, queue_size=1)

    def main(self):
        rospy.init_node('img_rgb_node')
        rospy.Subscriber('/camera/color/image_raw', Image, self.callback)
        rospy.spin()

    def callback(self, msg):
        self.pygame_event()

        self.grid_height = msg.height//NODE_RES
        self.grid_width = msg.width//NODE_RES
        self.grid = np.zeros((self.grid_height, self.grid_width),
                             dtype=np.uint8)

        # msg to cv-img
        img = self.bridge.imgmsg_to_cv2(msg)

        # cv-img to np-ndarray
        image = np.array(img, dtype=np.float32)
        cv2.normalize(image, image, 0, 255, cv2.NORM_MINMAX)
        image = np.round(image).astype(np.uint8)
        if not self.is_init:
            self.is_init = True
            self.win = pygame.display.set_mode((msg.width, msg.height))
            pygame.display.set_caption("GRID {}x{}".format(self.grid_width,
                                                           self.grid_height))
        image = np.swapaxes(image, 0, 1)
        self.win.fill((0, 0, 0))
        self.max_sum = 0
        self.robot_cor = [0, 0]
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                pix_sum = self.get_img(image, i, j)
                if pix_sum > self.max_sum:
                    if i != 0 and j != 0:
                        if i != 1 and j != 23:
                            self.max_sum = pix_sum
                            self.robot_cor[0] = i
                            self.robot_cor[1] = j
        self.draw_node(self.robot_cor[1], self.robot_cor[0], RED)
        pygame.display.flip()
        # self.clock.tick(self.fps)
        # self.pub.publish(self.grid.tobytes())

    def pygame_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rospy.signal_shutdown("EXIT")
                quit()
            elif event.type == pygame.KEYDOWN:
                pass

    def get_img(self, array, w, h):
        pix_sum = 0
        for pix_1 in range(w*NODE_RES,
                           (w+1)*NODE_RES-1,
                           1+PIXEL_SKIP_RATE):
            for pix_2 in range(h*NODE_RES,
                               (h+1)*NODE_RES-1,
                               1+PIXEL_SKIP_RATE):
                pix_sum += np.mean(array[pix_1][pix_2])
                self.win.set_at((pix_1, pix_2), array[pix_1][pix_2])
        return pix_sum

    def draw_grid(self):
        for i in range(self.grid_width+1):
            pygame.draw.line(self.win, BLACK, (i*self.vel, 0),
                             (i*self.vel, self.grid_height*self.vel))
        for i in range(self.grid_height+1):
            pygame.draw.line(self.win, BLACK, (0, i*self.vel),
                             (self.grid_width*self.vel, i*self.vel))

    def draw_node(self, i, j, color):
        pygame.draw.rect(self.win, color,
                         (self.vel*j, self.vel*i,
                          self.vel, self.vel))


if __name__ == '__main__':
    img_grid = ImgGrid()
    img_grid.main()
