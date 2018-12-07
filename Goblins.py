### GOBLIN
import pygame
import random
import pygwidgets
from Constants import *

class Goblin():

    def __init__(self, window, pos, image, text):
        # pass in position and walking direction for each NPC
        self.window = window
        self.image = pygame.image.load(image)
        self.text = text
        self.rect = self.image.get_rect()
        self.height = self.rect.height
        self.halfHeight = self.height / 2
        self.width = self.rect.width
        self.halfWidth = self.width / 2
        self.font_name = pygame.font.match_font(FONT_NAME)


        self.currentFrame = 0  # up to number of frames in an animation
        self.range = random.randrange(0,15)
        self.pacing = 0
        self.paceRight = 0
        self.paceLeft = 100
        self.randomPace = random.randrange(0,2)
        self.state = WALKLEFT

        # VEC(X,Y)
        self.pos = VEC(pos)
        self.vel = VEC(0, 0)
        self.acc = VEC(0, 0)

        print(self.font_name)
        self.textBox = pygwidgets.DisplayText(window,(self.pos.x - 3,self.pos.y - 3),"",fontName=self.font_name,\
                                              fontSize=16, textColor = WHITE)

        # instantiate collision platforms
        self.collision_map = pygame.image.load(IMAGE_COLLISION_MAP)

        self.collide_DOWN = False
        self.collide_RIGHT = False
        self.collide_LEFT = False

        self.color_DOWN = TEAL
        self.color_LEFT = TEAL
        self.color_RIGHT = TEAL

        self.camera = 0
        self.interact = False

        # Goblin Dictionary of Dictionaries
        '''self.susieDict = {'Location': ( 0, 0), 'Image': 'images/goblin_scarf_R1.png', 'Interact_1': "Hello World!", 'Interact_2': "That's it..."}
        self.bobDict = {'Location': ( 0, 0), 'Image': 'images/goblin_purple_R1.png', 'Interact_1': "I am Bob", 'Interact_2': "Scram guy..."}
        self.goblinDict = {oGoblin_Susie:susieDict, oGoblin_Bob:bobDict}'''


    def update(self):

        # motion
        self.acc.x += self.vel.x * PLAYER_FRICTION  # apply friction
        self.vel += self.acc  # calculate velocity
        self.pos += self.vel + (0.5 * self.acc)  # calculate position



        if self.paceRight <= (random.randrange(20,50)):
            self.pos.x = self.pos.x + .8
            self.paceRight = self.paceRight + 1
            if self.paceRight >= 50:
                self.paceLeft = 0

        if self.paceLeft <= (random.randrange(20,50)):
            self.pos.x = self.pos.x - .8
            self.paceLeft = self.paceLeft - 1

        if self.paceLeft <= -50:
            self.paceRight = 0
            self.paceLeft = 100


        # determine collision based on pixel color from collision map
        try:
            for pixel in range(int(self.pos.y + self.height), int((self.pos.y + self.height) + self.halfHeight + 1)):
                self.color_DOWN = self.collision_map.get_at((int(self.pos.x), int(pixel - OFFSET + self.camera)))
                if self.color_DOWN == HIT and self.vel.y > 0:
                    self.vel.y = 0
                    self.pos.y = pixel - self.height - 1
                    self.collision = True
                    break
                else:
                    self.acc = VEC(0, .5)
        except:
            self.acc = VEC(0,0)

        self.rect.left = self.pos.x
        self.rect.top = self.pos.y




    def handleInputs(self, eventsList, keyPressedList):
        self.eventsList = eventsList
        self.keyPressedList = keyPressedList

        for event in eventsList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.interact == True:
                        print(self.text)
                        self.textBox.setValue(self.text)


    def panCam(self, direction):
        self.direction = direction
        if direction == 'Up':
            self.collision_map.scroll(dx=0, dy=350)
        else:
            self.collision_map = pygame.image.load(IMAGE_COLLISION_MAP)


    def draw(self):
        self.window.blit(self.image, (self.pos.x, self.pos.y))
        self.textBox.draw()


    def collidesWith(self, playerRect):
        biggerGoblinRect = self.rect.inflate(2,2)
        if biggerGoblinRect.colliderect(playerRect):
            self.interact = True
            return True
        self.interact = False
        self.textBox.setValue('')
        return False




# GOBLINMGR
class GoblinMgr():

    def __init__(self, window):
        self.window = window
        self.goblinsList = []

        self.oGoblin_Susie = Goblin(self.window, (420, 310), 'images/goblin_scarf_R1.png', "Hello World!")
        self.oGoblin_Bob = Goblin(self.window, (80,130),'images/goblin_purple_R1.png', "I am Bob")

        self.goblinsList.append(self.oGoblin_Susie)
        self.goblinsList.append(self.oGoblin_Bob)

    def reset(self):  # Called when starting a new game
        self.goblinsList = []

        self.oGoblin_Susie = Goblin(self.window, (420, 310), 'images/goblin_scarf_R1.png', "Hello World!")
        self.oGoblin_Bob = Goblin(self.window, (80,130),'images/goblin_purple_R1.png', "I am Bob")

        self.goblinsList.append(self.oGoblin_Susie)
        self.goblinsList.append(self.oGoblin_Bob)
    def update(self):
        for goblin in self.goblinsList:
            goblin.update()

    def handleInputs(self, eventsList, keyPressedList):
        self.eventsList = eventsList
        self.keyPressedList = keyPressedList
        for goblin in self.goblinsList:
            goblin.handleInputs(self.eventsList, self.keyPressedList)

    def panCam(self, direction):
        self.direction = direction

        if direction == 'Up':
            for goblin in self.goblinsList:
                goblin.pos.y = goblin.pos.y + 350
                goblin.panCam('Up')
        else:
            for goblin in self.goblinsList:
                goblin.panCam('Down')
            self.reset()
    def draw(self):
        for goblin in self.goblinsList:
            goblin.draw()

    def hasPlayerHitGoblin(self, playerRect):
        for goblin in self.goblinsList:
            goblin.collidesWith(playerRect)
            biggerGoblinRect = goblin.rect.inflate(2,2)
            if biggerGoblinRect.colliderect(playerRect):
                return True
        return False
