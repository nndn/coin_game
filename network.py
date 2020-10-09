import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import random
import copy

class network(nn.Module):
    def __init__(self):
        super(network,self).__init__()
        self.fc1 = nn.Linear(8,12)
        self.fc2 = nn.Linear(12,6)
        self.fc3 = nn.Linear(6,4)

    def forward(self,state):

        out = T.tensor(state).type(T.FloatTensor)

        out = F.relu(self.fc1(out))
        out = F.relu(self.fc2(out))
        out = F.relu(self.fc3(out))

        out = T.sigmoid(out)

        for i in range(len(out)):
            if out[i] > 0.5:
                out[i] = 1
            else:
                out[i] = 0

        return out.tolist()

def breed(parent1, parent2):

    child_agent = network()

    parent1 = list(parent1.parameters())
    parent2 = list(parent2.parameters())

    n = 0

    for param in child_agent.parameters():

        if(len(param.shape)==2): #weights of linear layer
            for i0 in range(param.shape[0]):
                for i1 in range(param.shape[1]):
                    
                    param.data[i0][i1] = random.choice([parent1[n][i0][i1],parent2[n][i0][i1]])
                        

        elif(len(param.shape)==1): #biases of linear layer or conv layer
            for i0 in range(param.shape[0]):
                
                param.data[i0] = random.choice([parent1[n][i0],parent2[n][i0]])

        n = n + 1

    return child_agent

def mutate(agent, power):

    child_agent = network()
    child_agent.load_state_dict(agent.state_dict())
    
    mutation_power = power
            
    for param in child_agent.parameters():         

        if(len(param.shape)==2): #weights of linear layer
            for i0 in range(param.shape[0]):
                for i1 in range(param.shape[1]):
                    
                    param.data[i0][i1] += mutation_power * np.random.randn()
                        

        elif(len(param.shape)==1): #biases of linear layer or conv
            for i0 in range(param.shape[0]):
                
                param.data[i0] += mutation_power * np.random.randn()

    return child_agent