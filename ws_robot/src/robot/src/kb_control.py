#! /usr/bin/env python3
from my_mqtt import PahoMqtt
import pygame

BROKER = '127.0.0.1'
NODE = 'kb_control'

motor_topic = 'robot/cmd'

win = pygame.display.set_mode((200, 200))
pygame.display.set_caption('Control')
clock = pygame.time.Clock()

node = PahoMqtt(BROKER, NODE)
node.loop_start()

action = ''

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                action = 'fw'
            elif event.key == pygame.K_DOWN:
                action = 'bw'
            elif event.key == pygame.K_LEFT:
                action = 'le'
            elif event.key == pygame.K_RIGHT:
                action = 'ri'
            print(action)
        elif event.type == pygame.KEYUP:
            node.publish(motor_topic, 'st')
            action = 'st'
    if action is not '':
        node.publish(motor_topic, action)
        action = ''
    pygame.display.flip()
