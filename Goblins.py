### GOBLIN
import pygame
import random
from Constants import *

class Goblin():
    MIN_SPEED = 1
    MAX_SPEED = 9  # max plus one
    RIGHT = 'right'
    LEFT = 'left'

    def __init__(self, window):
        self.window = window
        zeroOrOne = random.randrange(0, 2)
        if zeroOrOne == 0:
            self.direction = Goblin.RIGHT
            self.image = pygame.image.load('images/goblin_R1.png')
            self.rect = self.image.get_rect()
            self.speed = random.randrange(Goblin.MIN_SPEED, Goblin.MAX_SPEED)
        else:
            self.direction = Goblin.LEFT
            self.image = pygame.image.load('images/goblin_L1.png')
            self.rect = self.image.get_rect()
            self.speed = - random.randrange(Goblin.MIN_SPEED, Goblin.MAX_SPEED)

    def update(self):
        self.rect.left = self.rect.left + self.speed
        if self.direction == Goblin.RIGHT:
            if self.rect.left > WINDOW_WIDTH:
                return True  # needs to be deleted
            else:
                return False  # stays in window
        else:  # moving left
            if self.rect.left < 0:
                return True  # needs to be deleted
            else:
                return False  # stays in window

    def draw(self):
        self.window.blit(self.image, self.rect)

    def collidesWith(self, playerRect):
        if self.rect.colliderect(playerRect):
            return True
        else:
            return False


# GOBLINMGR
class GoblinMgr():

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self):  # Called when starting a new game
        self.goblinsList = []
        self.frameCounter = 0
        self.createGoblinMax = 2

    def update(self):
        # If the correct amount of frames have passed,
        # add a new goblin at the left or right of the window

        self.frameCounter = self.frameCounter + 1
        if self.frameCounter == self.createGoblinMax:
            # Time to add a new goblin (and reset the counter)
            oGoblin = Goblin(self.window)
            self.goblinsList.append(oGoblin)
            self.frameCounter = 0
            # add a new goblin every createGoblinMax frames
            self.createGoblinMax = random.randrange(0,1)

        # Tell each goblin to update itself.
        # If a goblin goes off an edge, remove it
        for goblin in self.goblinsList:
            deleteMe = goblin.update()
            if deleteMe:
                self.goblinsList.remove(goblin)         

    def draw(self):
        for goblin in self.goblinsList:
            goblin.draw()

    def hasPlayerHitGoblin(self, playerRect):
        for goblin in self.goblinsList:
            if goblin.collidesWith(playerRect):
                print('player collided with Goblin')
                self.goblinsList.remove(goblin)  # remove this goblin from the list
                return True

        return False
