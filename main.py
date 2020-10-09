import pygame
import random
import torch as T
from utility import *
from network import *
import sys

done = False
clock = pygame.time.Clock()

game = game()
game.set_coin_randomly()

agent = T.load("bots/"+sys.argv[1]+".0")

net_reward = 0

while not done: #this is game loop

    #to check if done==1 i.e window closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if game.is_over():
        print("score:",game.coins_collected)
        print("net_reward:",net_reward)
        net_reward = 0
        game.reset()
        #done = True

    if pygame.key.get_pressed()[pygame.K_LCTRL] == 1:
        game.reset()

    #ip = getKeyboardInput()
    ip = agent(game.get_state())

    reward = game.take_action(ip)
    net_reward = net_reward + reward
    
    game.display()
    clock.tick(60)


    
