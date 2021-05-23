import numpy as np
import rospy
import pygame
import time
import random
from collections import deque
from matplotlib import pyplot as plt
from control import deep_mobile_control


pygame.init()
pygame.display.set_caption('Control')
win = pygame.display.set_mode((500, 200))
rospy.init_node('Mobile_Control', anonymous=True)
Robot = deep_mobile_control()
Robot.reset()
time.sleep(1)

#     Forward  Soft-right Soft-left  Hard-right Hard-left Back
VELS = [[1, 0], [0.5, 1], [0.5, -1], [0, 1], [0, -1], [-0.8, 0]]
ACTION_SPACE = len(VELS)

LR = 0.1
GAMMA = 0.99
EPSILON = 1
MIN_EPSILON = 0.1
EPSILON_DECAY = 0.9999

Q_TABLE = np.zeros((32, 21, 21, ACTION_SPACE))

run = True
terminal = False
episode = 1

avg_rew = {'ep': [], 'rew': []}


def take_action(a):
    Robot.vel.linear.x = a[0]
    Robot.vel.angular.z = a[1]
    Robot.cmd_vel.publish(Robot.vel)
    try:
        rospy.sleep(0.1)
    except Exception:
        print('rospy sleep exception')
    n_state = get_state()
    vel = n_state[2] / 10 - 1
    if vel >= 0.1:
        reward = (vel * 10) ** 2
    elif -0.1 < vel < 0.1:
        reward = -50
    else:
        reward = -20
    return n_state, reward


def get_state():
    s_temp = Robot.laser_data
    laser = 0
    for i, item in enumerate(s_temp):
        if item == 1:
            laser += 2**i
    a_s = np.round(Robot.odom_data.angular.z, 1)
    l_s = np.round(Robot.odom_data.linear.x, 1)
    if a_s > 1:
        a_s = 1
    elif a_s < -1:
        a_s = -1
    ang_sp = int((a_s + 1) * 10)
    lin_sp = int((l_s + 1) * 10)
    s_temp = [laser, ang_sp, lin_sp]
    print(np.round(Robot.odom_data.angular.z, 1))
    return s_temp


def event_handler():
    global terminal, run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminal = True
            run = False
            rospy.signal_shutdown('GG')
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                Robot.reset()


def game_cap(msg):
    pygame.display.set_caption(msg)


def summary():
    plt.plot(avg_rew['ep'], avg_rew['rew'])
    plt.show()


while run:
    Robot.reset()
    time.sleep(0.5)
    state = get_state()
    terminal = False
    end_counter = 0
    ep_reward = 0
    while not terminal:
        event_handler()
        if np.random.random() < EPSILON:
            action_ind = np.random.randint(ACTION_SPACE)
        else:
            action_ind = np.argmax(Q_TABLE[state[0]][state[1]][state[2]])
        action = VELS[action_ind]
        EPSILON = max(EPSILON * EPSILON_DECAY, MIN_EPSILON)
        new_state, reward = take_action(action)
        state = new_state
        ep_reward += reward
        if Robot.odom_data.linear.x <= 0:
            end_counter += 1
        else:
            if Robot.odom_data.linear.x > 0.1 and end_counter > 0:
                end_counter -= 1
        if end_counter >= 30:
            terminal = True

        current_q = Q_TABLE[state[0]][state[1]][state[2]][action_ind]
        max_future_q = \
            np.max(Q_TABLE[new_state[0]][new_state[1]][new_state[2]])
        Q_TABLE[state[0]][state[1]][state[2]][action_ind] = current_q + LR * \
            (reward + GAMMA * max_future_q - current_q)
        game_cap(f'ep:{episode}rew:{round(reward,3)} eps:{round(EPSILON, 6)}')

    episode += 1
    if episode % 10 == 0:
        avg_rew['ep'].append(episode)
        avg_rew['rew'].append(ep_reward)

np.save('q_table.npy', Q_TABLE)
summary()
