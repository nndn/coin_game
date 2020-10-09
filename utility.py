import pygame
import random

def clearScreen():
    screen.fill((0,0,0))

def disp(object):
    screen.blit(object.image,(object.x-int(object.image.get_size()[0]/2),
								object.y-int(object.image.get_size()[1]/2)))

def getKeyboardInput():

    key = pygame.key.get_pressed()

    keyup =  key[pygame.K_UP]
    keydown = key[pygame.K_DOWN]
    keyright = key[pygame.K_RIGHT]
    keyleft = key[pygame.K_LEFT]

    return [keyup,keydown,keyright,keyleft]

class obj:
    def __init__(self,image,width = 0,height = 0,x = 0,y = 0):
        self.image = pygame.image.load("assets/"+image).convert_alpha()
        self.x = x
        self.y = y
        self.width = self.image.get_size()[0] / 5
        self.height = self.image.get_size()[1] / 5

        if height != 0 and width != 0:
            self.height = int(height)
            self.width = int(width)

        self.image = pygame.transform.scale(self.image, (int(self.width), int(self.height)))

    def disp(self):
        disp(self)

class player(obj):

    def __init__(self, image, x, y, width = 0,height = 0):
        super(player,self).__init__(image, width, height)
        self.x = x
        self.y = y
        self.x_velocity = 0
        self.y_velocity = 0
        self.health = 100
        self.speed = 2
        self.maxspeed = 5
        self.tick = 0
        self.reactiontime = 1

    def get_pos(self):
        return (self.x,self.y)
    
    def control(self, keys):

        #move around

        self.x = self.x + self.x_velocity
        self.y = self.y + self.y_velocity

        if self.tick == self.reactiontime:
            self.tick = 0

        self.tick = self.tick + 1

        if self.tick != 1:
            return

        [keyup,keydown,keyright,keyleft] = keys

        if self.x_velocity > 0:
            self.x_velocity = self.x_velocity - 1

            if self.x_velocity > self.maxspeed:
                self.x_velocity = self.maxspeed

        if self.x_velocity < 0:
            self.x_velocity = self.x_velocity + 1

            if self.x_velocity < -1 * self.maxspeed:
                self.x_velocity = -1 * self.maxspeed

        if self.y_velocity > 0:
            self.y_velocity = self.y_velocity - 1

            if self.y_velocity > self.maxspeed:
                self.y_velocity = self.maxspeed

        if self.y_velocity < 0:
            self.y_velocity = self.y_velocity + 1

            if self.y_velocity < -1 * self.maxspeed:
                self.y_velocity = -1 * self.maxspeed

        if keyup:
            self.y_velocity = self.y_velocity - self.speed

        if keydown:
            self.y_velocity = self.y_velocity + self.speed
        
        if keyleft:
            self.x_velocity = self.x_velocity - self.speed

        if keyright:
            self.x_velocity = self.x_velocity + self.speed

        if self.y_velocity > self.maxspeed:
            self.y_velocity = self.maxspeed
        
        if self.x_velocity > self.maxspeed:
            self.x_velocity = self.maxspeed


class bot(player):
    def __init__(self, image, x, y, agent, width = 0,height = 0):
        super(bot,self).__init__(image, x, y, width, height)

    def getInput(self, input):
        return 


def savescreen(n):
    pygame.image.save(screen,"recording/frame"+str(n)+".jpeg")

class game:
    def __init__(self):
        pygame.init()
        global screen
        screen = pygame.display.set_mode((600,600))
        self.winx,self.winy = screen.get_size()

        self.arena = obj("arena.png",500,500,self.winx/2,self.winy/2)
        self.player = player("red.png",self.winx/2,self.winy/2)
        self.coin = obj("coin.png",20,20)
        self.coin_exists = 0
        self.time = 0
        self.coins_collected = 0
        self.isdead = 0

        self.game_length = 60*20

        #rewards
        self.reward_dead = -0.6
        self.reward_coin = 300
        self.reward_complete = 0

    def reset(self):
        self.player = player("red.png",self.winx/2,self.winy/2)
        self.coin.x = 0
        self.coin.y = 0
        self.coin_exists = 0
        self.coins_collected = 0
        self.time = 0
        self.isdead = 0

    def set_coin_randomly(self):
        self.coin_exists = 1
        self.coin.x = random.randint(100,500)
        self.coin.y = random.randint(100,500)

    def display(self):
        
        clearScreen()
        disp(self.arena)

        if self.coin_exists:
            disp(self.coin)

        disp(self.player)

        pygame.display.update()

    def isDead(self,i):
        if i.x > 550 or i.x < 50 or i.y>550 or i.y<50:
            return 1
        else:
            return 0

    def get_coin_pos(self):
        return (self.coin.x,self.coin.y)

    def is_over(self):
        if self.time >= self.game_length or self.isdead:
            return 1
        else:
            return 0

    def get_state(self):
        return [self.player.x,self.player.y,self.player.x_velocity,self.player.y_velocity,self.coin.x,self.coin.y,50,550]
        return [self.player.x,self.player.y,self.player.x_velocity,self.player.y_velocity,self.coin.x,self.coin.y,50,550]

    def collide(self,obj1,obj2):

        if abs(obj1.x - obj2.x)*2 < max(obj1.width,obj2.width) and abs(obj1.y - obj2.y)*2 < max(obj1.height,obj2.height):
            return 1
        else:
            return 0

    def take_action(self,action):

        self.time = self.time + 1

        if self.time % (60*4) == 1:
            self.coin_exists = 0

        if self.coin_exists == 0:
            self.set_coin_randomly()
        
        self.player.control(action)
        
        if self.isDead(self.player):
            self.isdead = 1
            return self.reward_dead

        if self.coin_exists and self.collide(self.player,self.coin):
            self.coins_collected = self.coins_collected + 1
            self.coin_exists = 0

            return self.reward_coin

        if self.is_over():
            return self.reward_complete

        reward = 1 - (abs(self.coin.x - self.player.x) * abs(self.coin.x - self.player.x)  + abs(self.coin.y - self.player.y) * abs(self.coin.y - self.player.y))/1000000

        return reward


        



