import numpy as np
import rospy
import os
import pygame
import time
import random
from collections import deque
from matplotlib import pyplot as plt
from control import deep_mobile_control
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense, Activation, Dropout, Input
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.optimizers import Adam

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

LR = 0.001
GAMMA = 0.9
EPSILON = 1
MIN_EPSILON = 0.1
EPSILON_DECAY = 0.99999

BUFFER_SIZE = 20000
MIN_BUFFER_SIZE = 4000
BATCH_SIZE = 128
EPOCHS = 10
TARGET_NET_UPDATE_FREQ = 10

REPLAY_BUFFER = deque(maxlen=BUFFER_SIZE)

run = True
terminal = False
update_counter = 1
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
    vel = Robot.odom_data.linear.x
    if vel > 0.1:
        reward = (vel * 20)
    elif -0.1 <= vel <= 0.1:
        reward = -10
    else:
        reward = -5
    #             (2 - n_state[0] - n_state[4]) + \
    #             (2 - n_state[1] - n_state[3]) * 2 + \
    #             (1 - n_state[2]) * 4 - 20
    return n_state, reward


def get_state():
    s_temp = Robot.laser_data
    ang_sp = Robot.odom_data.angular.z
    lin_sp = Robot.odom_data.linear.x
    s_temp = np.append(s_temp, [ang_sp, lin_sp])
    return s_temp


def get_model():
    model = Sequential()
    model.add(Input(shape=(7,)))
    model.add(Dense(42, activation='relu'))
    model.add(Dense(21, activation='relu'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(ACTION_SPACE))
    model.compile(loss="mse",
                  optimizer=Adam(lr=LR),
                  metrics=["accuracy"])
    model.summary()
    return model


def train():
    SAMPLES = random.sample(REPLAY_BUFFER, BATCH_SIZE)
    current_states = np.array([item[0] for item in SAMPLES])
    new_current_state = np.array([item[2] for item in SAMPLES])
    current_qs_list = []
    future_qs_list = []
    current_qs_list = main_nn.predict(current_states)
    future_qs_list = target_nn.predict(new_current_state)

    X = []
    Y = []
    for index, (state, action, _, reward, done) in enumerate(SAMPLES):
        if not done:
            new_q = reward + GAMMA * np.max(future_qs_list[index])
        else:
            new_q = reward

        current_qs = current_qs_list[index]
        current_qs[action] = new_q

        X.append(state)
        Y.append(current_qs)
    main_nn.fit(np.array(X), np.array(Y), epochs=EPOCHS,
                batch_size=BATCH_SIZE, shuffle=False, verbose=1)


def event_handler():
    global terminal, run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminal = True
            run = False
            rospy.signal_shutdown('GG')
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                Robot.reset()


def game_cap(msg):
    pygame.display.set_caption(msg)


def summary():
    plt.plot(avg_rew['ep'], avg_rew['rew'])
    plt.show()


try:
    main_nn = load_model(f"main.h5")
    target_nn = load_model(f"main.h5")
    print('LOADING MODEL')
except IOError:
    main_nn = get_model()
    target_nn = get_model()
    target_nn.set_weights(main_nn.get_weights())
    print('CREATING MODEL')


while run:
    Robot.reset()
    time.sleep(0.5)
    state = get_state()
    terminal = False
    end_counter = 0
    ep_reward = 0
    while not terminal:
        if np.random.random() < EPSILON:
            action_ind = np.random.randint(ACTION_SPACE)
        else:
            action_values = main_nn.predict(np.expand_dims(state, axis=0))[0]
            action_ind = np.argmax(action_values)
        EPSILON = max(EPSILON * EPSILON_DECAY, MIN_EPSILON)
        action = VELS[action_ind]
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
        game_cap(f'ep:{episode}rew:{round(reward,3)} eps:{round(EPSILON, 6)}')
        event_handler()

        REPLAY_BUFFER.append([state, action_ind, new_state, reward, terminal])

        if len(REPLAY_BUFFER) >= MIN_BUFFER_SIZE:
            train()
            update_counter += 1

        if update_counter % TARGET_NET_UPDATE_FREQ == 0:
            target_nn.set_weights(main_nn.get_weights())
            update_counter = 1
            print('target_net update')

    episode += 1
    if episode % 10 == 0:
        avg_rew['ep'].append(episode)
        avg_rew['rew'].append(ep_reward)
        main_nn.save('main.h5')

main_nn.save('main.h5')
summary()
