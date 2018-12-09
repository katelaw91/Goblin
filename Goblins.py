### GOBLIN
import pygame
import random
import pygwidgets
from Constants import *

class Goblin():

    def __init__(self, window, pos, spritesheet_loc, text, direction):
        # pass in position and walking direction for each NPC
        self.window = window
        self.text = text
        self.font_name = 'Apple'
        self.direction = direction

        self.range = random.randrange(0,15)
        self.pacing = 0
        self.paceRight = 0
        self.paceLeft = 100
        self.randomPace = random.randrange(0,2)
        self.state = WALKING

        #state/animation variables
        self.currentFrame = 0  # up to number of frames in an animation
        self.last_update = 0
        self.spritesheet = pygame.image.load(SPRITESHEET_GOBLINS).convert()
        self.frames = []


        for n in range(8):
            width = 26
            height = 31
            rect = pygame.Rect((n*width, spritesheet_loc), (width, height))
            image = pygame.Surface(rect.size).convert()
            image.blit(self.spritesheet, (0, 0), rect)
            alpha = image.get_at((0,0))
            image.set_colorkey(alpha)
            self.frames.append(image)

        self.idleFrames = self.frames[0]
        self.walkFrames_R = self.frames
        self.walkFrames_R = self.walkFrames_R[::-1]
        self.walkFrames_L = self.frames
        self.walkFrames_L = self.walkFrames_L[::-1]

        for frame in range(8):
            self.walkFrames_L.append(pygame.transform.flip(self.walkFrames_L[frame], True, False))
        self.walkFrames_L = self.walkFrames_L[9:]

        self.walkFrame_R = 0
        self.walkFrame_L = 0
        self.walkSpeed = 10

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
                                              fontSize=7, textColor = WHITE)
        self.shadow = pygwidgets.DisplayText(window, (self.pos.x + 0.5, self.pos.y + 17), "", fontName=self.font_name, \
                                              fontSize=8, textColor=BLACK)

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


    def update(self):

        # motion
        self.acc.x += self.vel.x * PLAYER_FRICTION  # apply friction
        self.vel += self.acc  # calculate velocity
        self.pos += self.vel + (0.5 * self.acc)  # calculate position

        if self.state == IDLING:
            self.image = self.idleFrames
        if self.state == WALKING:
            if self.direction == RIGHT:
                self.image = self.walkFrames_R[int(self.walkFrame_R/self.walkSpeed)]
                self.walkFrame_R += 1
                if self.walkFrame_R >= len((self.walkFrames_R * self.walkSpeed)):
                    self.walkFrame_R = 0
            elif self.direction == LEFT:
                self.image = self.walkFrames_L[int(self.walkFrame_L/self.walkSpeed)]
                self.walkFrame_L += 1
                if self.walkFrame_L >= len((self.walkFrames_L * self.walkSpeed)):
                    self.walkFrame_L = 0
            if self.pos.x >= WINDOW_WIDTH - self.width:
                self.direction = LEFT
            elif self.pos.x <= 0 + self.rect.width:
                self.direction = RIGHT

        if self.paceRight <= (random.randrange(20,50)):
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
            if self.state == IDLING:
                self.pos.x = self.pos.x

        if self.paceLeft <= -50:
            self.paceRight = 0
            self.paceLeft = 100
            self.direction = RIGHT
            if self.state == IDLING:
                self.pos.x = self.pos.x

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
                        self.idle()
                        self.textBox.setValue(self.text)
                        self.shadow.setValue(self.text)


    def panCam(self, direction):
        self.direction = direction
        if direction == 'Up':
            self.collision_map.scroll(dx=0, dy=350)
        else:
            self.collision_map = pygame.image.load(IMAGE_COLLISION_MAP)


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
        self.state = WALKING
        return False

    def chooseAction(self):
        chooseAction = random.randrange(0,10)

        #pause
        if chooseAction <= 5:
            self.idle()
        #walk right
        elif (chooseAction <=10) and (chooseAction > 5):
            self.walk()
    def idle(self):
        self.state = IDLING
        self.vel.x = 0
    def walk(self):
        self.state = WALKING
        walkCount = random.randrange(1,4)
        if self.direction == LEFT:
            for n in range(walkCount):
                self.pos.x = self.pos.x - 0.8
        if self.direction == RIGHT:
            for n in range(walkCount):
                self.pos.x = self.pos.x + 0.8

# GOBLINMGR
class GoblinMgr():

    def __init__(self, window):
        self.window = window
        self.goblinsList = []

        self.oGoblin_Susie = Goblin(self.window, (420, 310), 62, "Hello World!", LEFT)
        self.oGoblin_Bob = Goblin(self.window, (80,130), 31, "I am Bob", RIGHT)
        self.oGoblin_Urk = Goblin(self.window,(80, 200), 152, "Ew a grownup!", RIGHT)
        self.oGoblin_Meemaw = Goblin(self.window,(300, 200), 152, "You'll catch a chill dearie", LEFT)


        self.goblinsList.append(self.oGoblin_Susie)
        self.goblinsList.append(self.oGoblin_Bob)
        self.goblinsList.append(self.oGoblin_Urk)
        self.goblinsList.append(self.oGoblin_Meemaw)


    def reset(self):  # Called when starting a new game
        self.goblinsList = []

        self.oGoblin_Susie = Goblin(self.window, (420, 310), 62, "Hello World!", LEFT)
        self.oGoblin_Bob = Goblin(self.window, (80,130),31, "I am Bob", RIGHT)
        self.oGoblin_Urk = Goblin(self.window,(80, 200), 152, "Ew a grownup!", RIGHT)
        self.oGoblin_Meemaw = Goblin(self.window,(300, 200), 214, "You'll catch a chill dearie", LEFT)

        self.goblinsList.append(self.oGoblin_Susie)
        self.goblinsList.append(self.oGoblin_Bob)
        self.goblinsList.append(self.oGoblin_Urk)
        self.goblinsList.append(self.oGoblin_Meemaw)

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
