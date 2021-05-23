#! /usr/bin/env python3
import pygame
import rospy
from mobile_control import deep_mobile_control

# from my_mqtt import Mqtt


# BROKER = 'localhost'
# NODE = 'robot_control'
# motor_node = Mqtt(BROKER, NODE)
# motor_node.loop_start()


pygame.init()
pygame.display.set_caption('Control')
win = pygame.display.set_mode((100, 100))
win.fill((0, 0, 0))
rospy.init_node('Mobile_Control', anonymous=True)
Robot = deep_mobile_control()
Robot.reset()


vels = [[0.5, 0], [0.5, 1], [0.5, -1], [0, 0.8], [0, -0.8], [-0.5, 0], [0, 0]]
a = vels[-1]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rospy.signal_shutdown('GG')
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                a = vels[0]
            elif event.key == pygame.K_DOWN:
                a = vels[-2]
            elif event.key == pygame.K_LEFT:
                a = vels[4]
                print('left', vels[4])
            elif event.key == pygame.K_RIGHT:
                a = vels[3]
                print('right', vels[3])
            elif event.key == pygame.K_r:
                Robot.reset()
                pass
            # motor_node.publish('robot/motor_cmd', f'{a}')
        elif event.type == pygame.KEYUP:
            a = vels[-1]
    Robot.vel.linear.x = a[0]
    Robot.vel.angular.z = a[1]
    Robot.cmd_vel.publish(Robot.vel)
    # print(Robot.laser_data)
    pygame.display.flip()
