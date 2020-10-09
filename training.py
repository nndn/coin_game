from network import *
from utility import *
import torch as T

T.set_grad_enabled(False)

game = game()

plays = 1000
no_bots = 800

agents = []
scores = []

for i in range(no_bots):
    agents.append(network())

for play in range(plays):

    scores = []

    for bot in agents:

        game.reset()
        net_reward = 0

        done = False
        while not done:

            if game.is_over():
                done = True
                continue

            state = game.get_state()
            reward = game.take_action(bot.forward(state))
            net_reward = net_reward + reward

        scores.append((bot,net_reward))
    
    scores.sort(key = lambda x:x[1],reverse=True)

    if plays%10 == 0:
        total_score = 0
        
        for (bot,score) in scores[:20]:
            total_score = total_score + score

        print(total_score)

    agents = []
        
    for i in range(200):
        (bot,score) = scores[i]
        agents.append(bot)

    for i in range(20):
        (bot,score) = scores[i]
        agents.append(mutate(bot,0.01))
        agents.append(mutate(bot,0.02))
        agents.append(mutate(bot,0.03))
        agents.append(mutate(bot,0.03))
        agents.append(mutate(bot,0.1))

    (no1,sco) = scores[0]
    (no2,sco) = scores[1]
    (no3,sco) = scores[2]

    for i in range(40):
        (bot,score) = scores[i+1]
        agents.append(breed(bot,no1))
        agents.append(breed(bot,no1))
        agents.append(breed(bot,no2))
        agents.append(breed(bot,no2))
        agents.append(breed(bot,no3))

    for i in range(300):
        agents.append(network())

    if play % 10 == 0:
        T.save(no1,'bots/'+str(play/10))

    



            


