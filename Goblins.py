### GOBLIN
import pygame
import random
from Constants import *

class Goblin():

    def __init__(self, window, pos, image):
        # pass in position and walking direction for each NPC
        self.window = window
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.height = self.rect.height
        self.halfHeight = self.height / 2
        self.width = self.rect.width
        self.halfWidth = self.width / 2

        self.currentFrame = 0  # up to number of frames in an animation
        self.state = WALKLEFT

        # VEC(X,Y)
        self.pos = VEC(pos)
        self.vel = VEC(0, 0)
        self.acc = VEC(0, 0)

        # instantiate collision platforms
        self.collision_map = pygame.image.load(IMAGE_COLLISION_MAP)

        self.collide_DOWN = False
        self.collide_RIGHT = False
        self.collide_LEFT = False

        self.color_DOWN = TEAL
        self.color_LEFT = TEAL
        self.color_RIGHT = TEAL

        # Goblin Dictionary of Dictionaries
        '''self.susieDict = {'Location': ( 0, 0), 'Image': 'images/goblin_scarf_R1.png', 'Interact_1': "Hello World!", 'Interact_2': "That's it..."}
        self.bobDict = {'Location': ( 0, 0), 'Image': 'images/goblin_purple_R1.png', 'Interact_1': "I am Bob", 'Interact_2': "Scram guy..."}
        self.goblinDict = {oGoblin_Susie:susieDict, oGoblin_Bob:bobDict}'''


    def update(self):

        # motion
        self.acc.x += self.vel.x * PLAYER_FRICTION  # apply friction
        self.vel += self.acc  # calculate velocity
        self.pos += self.vel + (0.5 * self.acc)  # calculate position

        # determine collision based on pixel color from collision map
        for pixel in range(int(self.pos.y + self.height), int((self.pos.y + self.height) + self.halfHeight + 1)):
            self.color_DOWN = self.collision_map.get_at((int(self.pos.x), int(pixel - OFFSET)))
            if self.color_DOWN == HIT and self.vel.y > 0:
                self.vel.y = 0
                self.pos.y = pixel - self.height - 1
                self.collision = True
                break
            else:
                self.acc = VEC(0, PLAYER_GRAVITY)

    def draw(self):
        self.window.blit(self.image, (self.pos.x, self.pos.y))

    def collidesWith(self, playerRect):
        if self.rect.colliderect(playerRect):
            return True
        else:
            return False


# GOBLINMGR
class GoblinMgr():

    def __init__(self, window):
        self.window = window
        self.goblinsList = []

        self.oGoblin_Susie = Goblin(self.window, (50, 450), 'images/goblin_scarf_R1.png')
        self.oGoblin_Bob = Goblin(self.window, (80,130),'images/goblin_purple_R1.png')

        self.goblinsList.append(self.oGoblin_Susie)
        self.goblinsList.append(self.oGoblin_Bob)

    def reset(self):  # Called when starting a new game
        self.goblinsList = [self.oGoblin_Susie, self.oGoblin_Bob]

    def update(self):
        for goblin in self.goblinsList:
            goblin.update()


    def draw(self):
        for goblin in self.goblinsList:
            goblin.draw()

    def hasPlayerHitGoblin(self, playerRect):
        for goblin in self.goblinsList:
            if goblin.collidesWith(playerRect):
                print('player collided with Goblin')
                return True
