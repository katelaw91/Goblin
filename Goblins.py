### GOBLIN
import pygame
import random
import pygwidgets
import pyghelpers
from fontTools import *
from Constants import *

class Goblin():

    def __init__(self, window, pos, spritesheet_loc, text):
        # pass in position and walking direction for each NPC
        self.window = window
        self.text = text
        #self.font_name = 'cweblarge'
        #self.font_name = 'pixelatedregular'
        #self.font_name = 'pixeledregular'
        self.font_name = '04b03'
        self.direction = random.choice([LEFT, RIGHT])
        self.collision = False
        self.CM = 0

        self.range = random.randrange(0, 15)
        self.pacing = 0
        self.paceRight = 0
        self.paceLeft = 100
        self.randomPace = random.randrange(0, 2)
        '''self.idleAmt = random.choice([100, 200, 300, 400, 500, 600, 700,800,900,1000])
        self.idleTimer = 0
        self.walkAmt = random.choice([100, 200, 300, 400, 500, 600, 100, 200, 300])
        self.walkTimer = 0'''
        self.state = WALKING

        #state/animation variables
        self.currentFrame = 0  # up to number of frames in an animation
        self.last_update = 0
        self.spritesheet = pygame.image.load(SPRITESHEET_GOBLINS).convert()
        self.frames = []


        for n in range(10):
            width = 26
            height = 31
            rect = pygame.Rect((n*width, spritesheet_loc), (width, height))
            image = pygame.Surface(rect.size).convert()
            image.blit(self.spritesheet, (0, 0), rect)
            alpha = image.get_at((0,0))
            image.set_colorkey(alpha)
            self.frames.append(image)

        self.idleFrames_R = self.frames[8:]
        self.idleFrames_L = self.frames[8:]
        self.idleFrame_L = 0
        self.idleFrame_R = 0
        self.idleSpeed = 16
        self.walkFrames_R = self.frames
        self.walkFrames_R = self.walkFrames_R[::-1]
        self.walkFrames_L = self.frames
        self.walkFrames_L = self.walkFrames_L[::-1]
        self.walkFrame_R = 0
        self.walkFrame_L = 0
        self.walkSpeed = 10

        for frame in range(2):
            self.idleFrames_L.append(pygame.transform.flip(self.idleFrames_L[frame], True, False))
        self.idleFrames_L = self.idleFrames_L[3:]

        for frame in range(2):
            self.idleFrames_L.append(self.idleFrames_L[frame])
            self.idleFrames_R.append(self.idleFrames_R[frame])
        for frame in range(4):
            self.idleFrames_L.append(self.idleFrames_L[frame])
            self.idleFrames_R.append(self.idleFrames_R[frame])

        for frame in range(8):
            self.walkFrames_L.append(pygame.transform.flip(self.walkFrames_L[frame], True, False))
        self.walkFrames_L = self.walkFrames_L[9:]

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.height = self.rect.height
        self.halfHeight = self.height / 2
        self.width = self.rect.width
        self.halfWidth = self.width / 2

        # VEC(X,Y)
        self.pos = VEC(pos)
        self.vel = VEC(0, 0)
        self.acc = VEC(0, 0)

        self.textBox = pygwidgets.DisplayText(window,(self.pos.x + 3 ,self.pos.y + 15),"",fontName=self.font_name,\
                                              fontSize=15, textColor = WHITE)
        self.shadow = pygwidgets.DisplayText(window, (self.pos.x + 0.5, self.pos.y + 17), "", fontName=self.font_name, \
                                              fontSize=15, textColor=BLACK)

        # instantiate collision platforms
        self.collision_map = pygame.image.load(CM_LEVEL_1)

        self.collide_DOWN = False
        self.collide_RIGHT = False
        self.collide_LEFT = False

        self.color_DOWN = TEAL
        self.color_LEFT = TEAL
        self.color_RIGHT = TEAL

        self.interact = False


    def update(self,flag):

        # motion
        self.acc.x += self.vel.x * PLAYER_FRICTION  # apply friction
        self.vel += self.acc  # calculate velocity
        self.pos += self.vel + (0.5 * self.acc)  # calculate position

        if self.CM != flag:
            if flag == 0:
                self.collision_map = pygame.image.load(CM_LEVEL_1)
            else:
                self.collision_map = pygame.image.load(CM_LEVEL_2)
            self.CM = flag

        if self.state == IDLING:
            self.vel.x = 0
            self.acc.x = 0
            if self.direction == LEFT:
                self.image = self.idleFrames_L[int(self.idleFrame_L/self.idleSpeed)]
                self.idleFrame_L += 1
                if self.idleFrame_L >= len((self.idleFrames_L * self.idleSpeed)):
                    self.idleFrame_L = 0
            if self.direction == RIGHT:
                self.image = self.idleFrames_R[int(self.idleFrame_R/self.idleSpeed)]
                self.idleFrame_R += 1
                if self.idleFrame_R >= len((self.idleFrames_R * self.idleSpeed)):
                    self.idleFrame_R = 0
        elif self.state == WALKING:
            if self.direction == RIGHT:
                self.image = self.walkFrames_R[int(self.walkFrame_R / self.walkSpeed)]
                self.walkFrame_R += 1
                if self.walkFrame_R >= len((self.walkFrames_R * self.walkSpeed)):
                    self.walkFrame_R = 0
            elif self.direction == LEFT:
                self.image = self.walkFrames_L[int(self.walkFrame_L / self.walkSpeed)]
                self.walkFrame_L += 1
                if self.walkFrame_L >= len((self.walkFrames_L * self.walkSpeed)):
                    self.walkFrame_L = 0
            if self.pos.x >= WINDOW_WIDTH - self.width:
                self.direction = LEFT
            elif self.pos.x <= 0 + self.rect.width:
                self.direction = RIGHT
            if self.paceRight <= (random.randrange(20, 50)):
                self.pos.x = self.pos.x + .8
                self.paceRight = self.paceRight + 1
                self.direction = RIGHT
                if self.paceRight >= 50:
                    self.paceLeft = 0
                    self.direction = LEFT
            if self.paceLeft <= (random.randrange(20, 50)):
                self.pos.x = self.pos.x - .8
                self.paceLeft = self.paceLeft - 1
                self.direction = LEFT
                if self.paceLeft <= -50:
                    self.paceRight = 0
                    self.paceLeft = 100
                    self.direction = RIGHT


        '''if self.chooseAction <= 7:
            self.state = WALKING
            self.myTimer.start()
        else:
            self.state = IDLING
            self.myTimer.start()

        if self.finished:
            self.chooseAction = random.randrange(0,2)'''


        '''if self.paceRight <= (random.randrange(20,50)):
            self.pos.x = self.pos.x + .8
            self.paceRight = self.paceRight + 1
            self.direction = RIGHT
            if self.paceRight >= 50:
                self.paceLeft = 0
                self.direction = LEFT
            if self.state == IDLING:
                self.pos.x = self.pos.x

        if self.paceLeft <= (random.randrange(20,50)):
            self.pos.x = self.pos.x - .8
            self.paceLeft = self.paceLeft - 1
            self.direction = LEFT
            if self.paceLeft <= -50:
                self.paceRight = 0
                self.paceLeft = 100
                self.direction = RIGHT
                if self.state == IDLING:
                    self.pos.x = self.pos.x'''


        # determine collision based on pixel color from collision map
        try:
            for pixel in range(int(self.pos.y + self.height), int((self.pos.y + self.height) + self.halfHeight + 1)):
                self.color_DOWN = self.collision_map.get_at((int(self.pos.x), int(pixel)))
                '''self.color_LEFT = self.collision_map.get_at((int(self.pos.x - self.width + 5), int(pixel)))
                self.color_RIGHT = self.collision_map.get_at((int(self.pos.x + self.width - 5), int(pixel)))'''
                if self.color_DOWN == HIT and self.vel.y > 0:
                    self.vel.y = 0
                    self.pos.y = pixel - self.height - 1
                    self.collision = True
                    break
                else:
                    self.acc = VEC(0, .5)
                '''if self.color_RIGHT == (255,0,0):
                    self.directionFlip()
                    self.state = IDLING
                if self.color_LEFT == (255,0,0):
                    self.state = IDLING
                    self.directionFlip()'''

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
                        self.shadow.setValue(self.text)


    def panCam(self, levelState):
        print("pan cam called")
        if levelState == GOBLIN_LOWER:
            self.CM = 0
            print("set to 0")
        else:
            self.CM = 1
            print("set to 1")






    def draw(self):
        self.window.blit(self.image, (self.pos.x, self.pos.y))
        self.shadow.draw()
        self.textBox.draw()



    def collidesWith(self, playerRect):
        biggerGoblinRect = self.rect.inflate(2,2)
        if biggerGoblinRect.colliderect(playerRect):
            self.interact = True
            return True
        self.interact = False
        self.textBox.setValue('')
        self.shadow.setValue('')
        return False

    def directionFlip(self):
        if self.direction == RIGHT:
            self.direction = LEFT
        else:
            self.direction = RIGHT


# GOBLINMGR
class GoblinMgr():

    def __init__(self, window):
        self.window = window
        self.goblinsList = []
        self.levelState = GOBLIN_LOWER

        self.oGoblin_Susie = Goblin(self.window, (420, 310), 62, "Hey theree!")
        self.oGoblin_Bob = Goblin(self.window, (80,130), 31, "Out for a stroll?")
        self.oGoblin_Eck = Goblin(self.window, (10, 250), 183, "I'm hunting bugs...")


        self.goblinsList.append(self.oGoblin_Susie)
        self.goblinsList.append(self.oGoblin_Bob)

    def reset(self):

        self.goblinsList = []

        if self.levelState == GOBLIN_LOWER:
            self.oGoblin_Susie = Goblin(self.window, (420, 310), 62, "Hey theree!")
            self.oGoblin_Bob = Goblin(self.window, (80,130), 31, "Out for a stroll?")
            self.oGoblin_Eck = Goblin(self.window, (10, 250), 183, "I'm hunting bugs...")
            self.goblinsList.append(self.oGoblin_Susie)
            self.goblinsList.append(self.oGoblin_Bob)
            self.goblinsList.append(self.oGoblin_Eck)
        elif self.levelState == GOBLIN_UPPER:
            self.oGoblin_Bob = Goblin(self.window, (80, 510), 31, "Out for a stroll?")
            self.oGoblin_Urk = Goblin(self.window, (450, 294), 152, "Ew a grownup!")
            self.oGoblin_Meemaw = Goblin(self.window, (70, 58), 214, "You'll catch a chill dearie")
            self.oGoblin_Sal = Goblin(self.window, (420, 250), 124, "Hey there!")
            self.oGoblin_Kruk = Goblin(self.window, (160,290), 93, "Got any fish?")
            self.goblinsList.append(self.oGoblin_Bob)
            self.goblinsList.append(self.oGoblin_Urk)
            self.goblinsList.append(self.oGoblin_Meemaw)
            self.goblinsList.append(self.oGoblin_Sal)
            self.goblinsList.append(self.oGoblin_Kruk)
        else:
            self.goblinsList = []


    def update(self):
        if self.levelState == GOBLIN_LOWER:
            flag = 0
        else:
            flag = 1
        for goblin in self.goblinsList:
            goblin.update(flag)

    def handleInputs(self, eventsList, keyPressedList):
        self.eventsList = eventsList
        self.keyPressedList = keyPressedList
        for goblin in self.goblinsList:
            goblin.handleInputs(self.eventsList, self.keyPressedList)

    def panCam(self, panDirection, currentState):
        if panDirection == 'Up':
            if currentState == GOBLIN_LOWER:
                self.levelState = GOBLIN_UPPER
            elif currentState == GOBLIN_UPPER:
                self.levelState = CITY_LOWER
            elif currentState == CITY_LOWER:
                self.levelState = CITY_UPPER
            elif currentState == CITY_UPPER:
                self.levelState = LEVEL_END
        elif panDirection == 'Down':
            if currentState == GOBLIN_UPPER:
                self.levelState = GOBLIN_LOWER
            elif currentState == CITY_LOWER:
                self.levelState = GOBLIN_UPPER
            elif currentState == CITY_UPPER:
                self.levelState = CITY_LOWER
            elif currentState == LEVEL_END:
                self.levelState = CITY_UPPER
        for oGoblin in self.goblinsList:
            oGoblin.panCam(self.levelState)
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
