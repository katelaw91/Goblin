### VILLAGER
import pygame
import random
from Constants import *
import pygwidgets
import pyghelpers

class Villager():
    def __init__(self, window, pos, spritesheet_loc, text, direction):
        # pass in position and walking direction for each NPC
        self.window = window
        self.text = text
        self.font_name = 'gothicpixels'
        #self.font_name = 'pixeledenglishfont'
        self.direction = direction
        self.collision = False
        self.CM = 1

        self.range = random.randrange(0,15)
        self.pacing = 0
        self.paceRight = 0
        self.paceLeft = 100
        self.randomPace = random.randrange(0,2)
        self.idleAmt = random.choice([100, 200,300,400,500,600,100])
        self.idleTimer = 0
        self.state = WALKING

        # state/animation variables
        self.currentFrame = 0  # up to number of frames in an animation
        self.last_update = 0
        self.spritesheet = pygame.image.load(SPRITESHEET_VILLAGERS).convert()
        self.frames = []
        # self.chooseAction = random.randrange(0,10)
        # self.randomTime = random.randrange(0,2)
        # self.myTimer = pyghelpers.Timer(.5)
        # self.finished = self.myTimer.update()
        # self.stateList = [IDLING, WALKING]
        # self.directionList = [RIGHT,LEFT]
        # self.randomPace = random.randrange(0,20)
        # self.actionTimer = 0

        for n in range(18):
            width = 62
            height = 44
            rect = pygame.Rect((n * width, spritesheet_loc), (width, height))
            image = pygame.Surface(rect.size).convert()
            image.blit(self.spritesheet, (0, 0), rect)
            alpha = image.get_at((0, 0))
            image.set_colorkey(alpha)
            self.frames.append(image)

        self.idleFrames_R = self.frames[17:19]
        self.idleFrames_L = self.frames[17:19]
        self.walkFrames_R = self.frames[8:16]
        self.walkFrames_L = self.frames[8:16]
        self.attackFrames_L = self.frames[:9]
        self.attackFrames_R = self.frames[:9]


        for frame in range(2):
            self.idleFrames_L.append(pygame.transform.flip(self.idleFrames_L[frame], True, False))
        self.idleFrames_L = self.idleFrames_L[2:]

        for frame in range(8):
            self.walkFrames_L.append(pygame.transform.flip(self.walkFrames_L[frame], True, False))
        self.walkFrames_L = self.walkFrames_L[9:]

        for frame in range(8):
            self.attackFrames_L.append(pygame.transform.flip(self.attackFrames_L[frame], True, False))
        self.attackFrames_L = self.attackFrames_L[9:]

        self.idleFrame_L = 0
        self.idleFrame_R = 0
        self.idleSpeed = 16
        self.walkFrame_R = 0
        self.walkFrame_L = 0
        self.walkSpeed = 8
        self.attackSpeed = 12
        self.attackFrame_L = 0
        self.attackFrame_R = 0

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

        self.textBox = pygwidgets.DisplayText(window, (self.pos.x + 3, self.pos.y + 15), "", fontName=self.font_name, \
                                              fontSize=12, textColor=WHITE)
        self.shadow = pygwidgets.DisplayText(window, (self.pos.x + 0.5, self.pos.y + 17), "", fontName=self.font_name, \
                                             fontSize=12, textColor=BLACK)

        # instantiate collision platforms
        self.collision_map = pygame.image.load(CM_LEVEL_1)
        self.setCM = False

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
            if flag == 1:
                self.collision_map = pygame.image.load(CM_LEVEL_1)
            elif flag ==2:
                self.collision_map = pygame.image.load(CM_LEVEL_2)
            elif flag ==3:
                self.collision_map = pygame.image.load(CM_LEVEL_3)
            elif flag ==4:
                self.collision_map = pygame.image.load(CM_LEVEL_4)
            elif flag ==5:
                self.collision_map = pygame.image.load(CM_LEVEL_5)
            self.CM = flag

        if self.state == IDLING:
            self.vel.x = 0
            self.acc.x = 0
            self.idleTimer = self.idleTimer + 1
            if self.direction == LEFT:
                self.image = self.idleFrames_L[int(self.idleFrame_L / self.idleSpeed)]
                self.idleFrame_L += 1
                if self.idleFrame_L >= len((self.idleFrames_L * self.idleSpeed)):
                    self.idleFrame_L = 0
            if self.direction == RIGHT:
                self.image = self.idleFrames_R[int(self.idleFrame_R / self.idleSpeed)]
                self.idleFrame_R += 1
                if self.idleFrame_R >= len((self.idleFrames_R * self.idleSpeed)):
                    self.idleFrame_R = 0
            if self.idleTimer > self.idleAmt:
                self.state = WALKING
                self.idleTimer = 0
            # if now - self.actionTimer > 2000 + random.choice([0, 2000,3000,4000,5000,6000,7000,8000,9000,10000]):
            # self.state = random.choice(self.stateList)
            # self.actionTimer = now
        elif self.state == WALKING:
            if self.direction == RIGHT:
                self.image = self.walkFrames_R[int(self.walkFrame_R / self.walkSpeed)]
                self.walkFrame_R += 1
                if self.walkFrame_R >= len((self.walkFrames_R * self.walkSpeed)):
                    self.walkFrame_R = 0
                # self.pos.x = self.pos.x + GOB_SPEED
            elif self.direction == LEFT:
                self.image = self.walkFrames_L[int(self.walkFrame_L / self.walkSpeed)]
                self.walkFrame_L += 1
                if self.walkFrame_L >= len((self.walkFrames_L * self.walkSpeed)):
                    self.walkFrame_L = 0
                # self.pos.x = self.pos.x - GOB_SPEED
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
                    if self.state == IDLING:
                        self.pos.x = self.pos.x


        '''if self.chooseAction <= 7:
            self.state = WALKING
            self.myTimer.start()
        else:
            self.state = IDLING
            self.myTimer.start()

        if self.finished:
            self.chooseAction = random.randrange(0,2)'''



        # determine collision based on pixel color from collision map
        try:
            for pixel in range(int(self.pos.y + self.height), int((self.pos.y + self.height) + self.halfHeight + 1)):
                self.color_DOWN = self.collision_map.get_at((int(self.pos.x), int(pixel)))
                if self.color_DOWN == HIT and self.vel.y > 0:
                    self.vel.y = 0
                    self.pos.y = pixel - self.height - 1
                    self.collision = True
                    break
                else:
                    self.acc = VEC(0, .5)


        except:
            self.acc = VEC(0, 0)

        self.rect.left = self.pos.x
        self.rect.top = self.pos.y

    def handleInputs(self, eventsList, keyPressedList):
        self.eventsList = eventsList
        self.keyPressedList = keyPressedList

        for event in eventsList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("pressing enter..")
                    if self.interact == True:
                        "entered interact true condition"
                        print(self.text)
                        self.idle()
                        self.textBox.setValue(self.text)
                        self.shadow.setValue(self.text)


    def panCam(self, levelState):
        if levelState == GOBLIN_LOWER:
            self.CM = 1
        elif levelState == GOBLIN_UPPER:
            self.CM = 2
        elif levelState == CITY_LOWER:
            self.CM = 3
        elif levelState == CITY_UPPER:
            self.CM = 4
        elif levelState == LEVEL_END:
            self.CM = 5

    def draw(self):
        self.window.blit(self.image, (self.pos.x, self.pos.y))
        self.shadow.draw()
        self.textBox.draw()

    def collidesWith(self, playerRect):
        biggerGoblinRect = self.rect.inflate(2, 2)
        if biggerGoblinRect.colliderect(playerRect):
            self.interact = True
            return True
        self.interact = False
        self.textBox.setValue('')
        self.shadow.setValue('')
        # self.state = WALKING
        return False

    def directionFlip(self):
        if self.direction == RIGHT:
            self.direction = LEFT
        else:
            self.direction = RIGHT

    def idle(self):
        self.state = IDLING
        self.vel.x = 0

    '''def walk(self):
        self.state = WALKING
        walkCount = random.randrange(1,4)
        if self.direction == LEFT:
            for n in range(walkCount):
                self.pos.x = self.pos.x - 0.8
        if self.direction == RIGHT:
            for n in range(walkCount):
                self.pos.x = self.pos.x + 0.8'''

    # GOBLINMGR


class VillagersMgr():

    def __init__(self, window):
        self.window = window
        self.villagersList = []
        self.levelState = GOBLIN_LOWER
        self.setNewCM = False

        self.oVillager_Susie = Villager(self.window, (420, 310), 0, "Hey theree!", LEFT)
        self.oVillager_Bob = Villager(self.window, (80, 130), 0, "Out for a stroll?", RIGHT)
        self.oVillager_Eck = Villager(self.window, (10, 250), 0, "I'm hunting bugs...", RIGHT)

        self.villagersList.append(self.oVillager_Susie)
        self.villagersList.append(self.oVillager_Bob)

    def reset(self):

        self.villagersList = []

        if self.levelState == CITY_LOWER:
            self.villagersList = []
            self.oVillager_Susie = Villager(self.window, (415, 150), 0, "HALT!", LEFT)
            self.villagersList.append(self.oVillager_Susie)
        elif self.levelState == CITY_UPPER:
            self.villagersList = []
            self.oVillager_Bob = Villager(self.window, (80, 510), 0, "Out for a stroll?", RIGHT)
            self.oVillager_Urk = Villager(self.window, (450, 294), 0, "Ew a grownup!", RIGHT)
            self.oVillager_Meemaw = Villager(self.window, (70, 58), 0, "You'll catch a chill dearie", LEFT)
            self.oVillager_Sal = Villager(self.window, (420, 250), 0, "Hey there!", LEFT)
            self.oVillager_Kruk = Villager(self.window, (160, 290), 0, "Got any fish?", RIGHT)
            self.villagersList.append(self.oVillager_Bob)
            self.villagersList.append(self.oVillager_Urk)
            self.villagersList.append(self.oVillager_Meemaw)
            self.villagersList.append(self.oVillager_Sal)
            self.villagersList.append(self.oVillager_Kruk)
        else:
            self.villagersList = []

    def update(self):
        if self.levelState == GOBLIN_LOWER:
            flag = 1
        elif self.levelState == GOBLIN_UPPER:
            flag = 2
        elif self.levelState == CITY_LOWER:
            flag = 3
        elif self.levelState == CITY_UPPER:
            flag = 4
        elif self.levelState == LEVEL_END:
            flag = 5
        for villager in self.villagersList:
            villager.update(flag)

    def handleInputs(self, eventsList, keyPressedList):
        self.eventsList = eventsList
        self.keyPressedList = keyPressedList
        for villager in self.villagersList:
            villager.handleInputs(self.eventsList, self.keyPressedList)

    def panCam(self, panDirection, currentState):
        if panDirection == 'Up':
            if currentState == GOBLIN_LOWER:
                self.levelState = GOBLIN_UPPER
                self.oVillager_Bob.panCam(self.levelState)
                self.reset()
            elif currentState == GOBLIN_UPPER:
                self.levelState = CITY_LOWER
                self.oVillager_Bob.panCam(self.levelState)
                self.reset()
            elif currentState == CITY_LOWER:
                self.levelState = CITY_UPPER
                self.oVillager_Bob.panCam(self.levelState)
                self.reset()
            elif currentState == CITY_UPPER:
                self.levelState = LEVEL_END
                self.oVillager_Bob.panCam(self.levelState)
                self.reset()
        elif panDirection == 'Down':
            if currentState == GOBLIN_UPPER:
                self.levelState = GOBLIN_LOWER
                self.oVillager_Bob.panCam(self.levelState)
                self.reset()
            elif currentState == CITY_LOWER:
                self.levelState = GOBLIN_UPPER
                self.oVillager_Bob.panCam(self.levelState)
                self.reset()
            elif currentState == CITY_UPPER:
                self.levelState = CITY_LOWER
                self.oVillager_Bob.panCam(self.levelState)
                self.reset()
            elif currentState == LEVEL_END:
                self.levelState = CITY_UPPER
                self.oVillager_Bob.panCam(self.levelState)
                self.reset()

    def draw(self):
        for villager in self.villagersList:
            villager.draw()

    def hasPlayerHitVillager(self, playerRect):
        for villager in self.villagersList:
            villager.collidesWith(playerRect)
            biggerRect = villager.rect.inflate(2, 2)
            if biggerRect.colliderect(playerRect):
                return True
        return False
