#! /usr/bin/env python3
import rospy
import numpy as np
from mobile_control import deep_mobile_control
from my_robot.msg import next_move, board, board_cmd
# from my_mqtt import Mqtt


# BROKER = 'localhost'
# NODE = 'robot_control'
# motor_node = Mqtt(BROKER, NODE)
# motor_node.loop_start()


FORWARD = [0.8, 0]
BACKWARD = [-0.5, 0]
HARD_LEFT = [0, -0.4]
HARD_RIGHT = [0, 0.4]
SOFT_LEFT = [0.25, -1]
SOFT_RIGHT = [0.25, 1]
STOP = [0, 0]

UP = 90
DOWN = 270
RIGHT = 0
LEFT = 180
UPPER_RIGHT = 45
UPPER_LEFT = 135
DOWN_LEFT = 225
DOWN_RIGHT = 315

robot = deep_mobile_control()
robot_x = None
robot_y = None
robot_dir = None

next_x = None
next_y = None
next_dir = None

state_counter = 0
x_temp = 0
y_temp = 0


def robot_move(action):
    robot.vel.linear.x = action[0]
    robot.vel.angular.z = action[1]
    robot.cmd_vel.publish(robot.vel)
    # motor_node.publish('robot/motor_cmd', f'{action}')


def robot_reset():
    robot_move(STOP)
    msg = board_cmd()
    msg.reset = True
    pub.publish(msg)


def robot_state():
    return robot.laser_data


def robot_cor_cb(msg):
    global robot_x, robot_y, robot_dir
    robot_x = int(msg.robot_x)
    robot_y = int(msg.robot_y)
    robot_dir = int(msg.robot_dir)


def next_move_cb(msg):
    global next_x, next_y, next_dir
    next_x = int(msg.x)
    next_y = int(msg.y)
    next_dir = int(msg.dir)


def move():
    global state_counter, x_temp, y_temp
    rot = False
    print('next', next_dir, 'cur', robot_dir)
    print(robot_x - next_x, robot_y - next_y)
    if np.abs(next_dir - robot_dir) > 8:
        # print('rotate', np.abs(robot_dir - next_dir))
        rotate()
        rot = True
    if next_dir == UP:
        if np.abs(robot_y - next_y) > 0 or robot_x - next_x < 0:
            robot_reset()
            return
    elif next_dir == DOWN:
        if np.abs(robot_y - next_y) > 0 or robot_x - next_x > 0:
            robot_reset()
    elif next_dir == LEFT:
        if np.abs(robot_x - next_x) > 0 or robot_y - next_y < 0:
            robot_reset()
            return
    elif next_dir == RIGHT:
        if np.abs(robot_x - next_x) > 0 or robot_y - next_y > 0:
            robot_reset()
            return
    elif next_dir == UPPER_LEFT:
        if robot_x - next_x != 1 or robot_y - next_y != 1:
            robot_move(STOP)
            msg = board_cmd()
            msg.reset = True
            pub.publish(msg)
            return
    elif next_dir == UPPER_RIGHT:
        if robot_x - next_x != 1 or robot_y - next_y != -1:
            robot_move(STOP)
            msg = board_cmd()
            msg.reset = True
            pub.publish(msg)
            return
    elif next_dir == DOWN_LEFT:
        if robot_x - next_x != -1 or robot_y - next_y != 1:
            robot_move(STOP)
            msg = board_cmd()
            msg.reset = True
            pub.publish(msg)
            return
    elif next_dir == DOWN_RIGHT:
        if robot_x - next_x != -1 or robot_y - next_y != -1:
            robot_move(STOP)
            msg = board_cmd()
            msg.reset = True
            pub.publish(msg)
            return
    if not rot:
        forward()


def rotate():
    if next_dir - robot_dir > 0:
        if next_dir - robot_dir <= 180:
            robot_move(HARD_LEFT)
        elif next_dir - robot_dir > 180:
            robot_move(HARD_RIGHT)
    elif next_dir - robot_dir < 0:
        if next_dir - robot_dir >= -180:
            robot_move(HARD_RIGHT)
        elif -180 > next_dir - robot_dir:
            robot_move(HARD_LEFT)


def forward():
    state = robot_state()
    # print(state)
    if state[1] < 0.21:
        robot_move(BACKWARD)
        robot_move(HARD_LEFT)
        robot_move(SOFT_LEFT)
        # print('left')
    elif state[3] < 0.21:
        robot_move(BACKWARD)
        robot_move(HARD_RIGHT)
        robot_move(SOFT_RIGHT)
        # print('right')
    elif state[0] < 0.17:
        robot_move(BACKWARD)
        robot_move(HARD_LEFT)
        robot_move(SOFT_LEFT)
        # print('left')
    elif state[4] < 0.17:
        robot_move(BACKWARD)
        robot_move(HARD_RIGHT)
        robot_move(SOFT_RIGHT)
        # print('right')
    elif state[2] < 0.23:
        robot_move(BACKWARD)
        robot_move(BACKWARD)
        # print('back')
    else:
        robot_move(FORWARD)
        # print('forward')


def main():
    global pub
    rospy.init_node('control_node', anonymous=True)
    rospy.Subscriber('robot_cor', board, robot_cor_cb)
    rospy.Subscriber('next_move_state', next_move, next_move_cb)
    pub = rospy.Publisher('board_control', board_cmd, queue_size=1)
    rate = rospy.Rate(10)
    # robot.reset()
    while not rospy.is_shutdown():
        if next_x and next_y:
            move()
            pass
        try:
            rate.sleep()
        except Exception:
            pass
        robot_move(STOP)
    rospy.signal_shutdown('EXIT')


if __name__ == '__main__':
    main()
