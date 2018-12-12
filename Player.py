### PLAYER
import pygame
import pygwidgets
from Constants import *

class Player():
    def __init__(self, window):
        self.window = window
        self.levelState = GOBLIN_LOWER
        self.interact = False
        self.collision = False
        self.state = IDLING
        self.direction = RIGHT

        #state/animation variables
        self.currentFrame = 0  # up to number of frames in an animation
        self.last_update = 0
        self.spritesheet = pygame.image.load(SPRITESHEET_PLAYER).convert()
        self.frames = []

        for n in range(21):
            width = 26
            height = 31.5
            rect = pygame.Rect(n*width, 0, width, height)
            image = pygame.Surface(rect.size).convert()
            image.blit(self.spritesheet, (0,0), rect)
            alpha = image.get_at((0,0))
            image.set_colorkey(alpha)
            self.frames.append(image)

        self.idleFrames_R = self.frames[8:14]
        self.idleFrames_L = self.frames[8:14]
        self.walkFrames_R = self.frames[:9]
        self.walkFrames_R = self.walkFrames_R[::-1]
        self.walkFrames_L = self.frames[:9]
        self.walkFrames_L = self.walkFrames_L[::-1]
        self.jumpFrames_L = self.frames[13:16]
        self.jumpFrames_R = self.frames[13:16]
        self.fallFrames_L = self.frames[16:18]
        self.fallFrames_R = self.frames[16:18]
        self.attackFrames_L = self.frames[19:21]
        self.attackFrames_R = self.frames[19:21]

        for frame in range(5):
            self.idleFrames_L.append(pygame.transform.flip(self.idleFrames_L[frame], True, False))
        self.idleFrames_L = self.idleFrames_L[6:]

        for frame in range(8):
            self.walkFrames_L.append(pygame.transform.flip(self.walkFrames_L[frame], True, False))
        self.walkFrames_L = self.walkFrames_L[9:]

        for frame in range(3):
            self.jumpFrames_L.append(pygame.transform.flip(self.jumpFrames_L[frame], True, False))
        self.jumpFrames_L = self.jumpFrames_L[4:]

        for frame in range(2):
            self.fallFrames_L.append(pygame.transform.flip(self.fallFrames_L[frame], True, False))
        self.fallFrames_L = self.fallFrames_L[3:]

        for frame in range(3):
            self.attackFrames_L.append(pygame.transform.flip(self.attackFrames_L[frame], True, False))
        self.attackFrames_L = self.attackFrames_L[4:]

        self.idleFrame_L = 0
        self.idleFrame_R = 0
        self.idleSpeed = 16
        self.walkFrame_R = 0
        self.walkFrame_L = 0
        self.walkSpeed = 8
        self.jumpFrame_L = 0
        self.jumpFrame_R = 0
        self.jumpSpeed = 8
        self.fallFrame_R = 0
        self.fallFrame_L = 0
        self.fallSpeed = 8
        self.attackSpeed = 12
        self.attackFrame_L = 0
        self.attackFrame_R = 0

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.height = self.rect.height
        self.halfHeight = self.height / 2
        self.width = self.rect.width
        self.halfWidth = self.width / 2


        #VEC(X,Y)
        self.pos = VEC(50, 450)
        self.vel = VEC(0,0)
        self.acc = VEC(0,0)

        #instantiate collision platforms
        self.collision_map = pygame.image.load(CM_LEVEL_1)

        self.collide_DOWN = False
        self.collide_RIGHT = False
        self.collide_LEFT = False

        self.color_DOWN = TEAL
        self.color_LEFT = TEAL
        self.color_RIGHT = TEAL

    def reset(self):
        self.rect.center = (50, WINDOW_HEIGHT + 50)

    def update(self):

       #motion
        self.acc.x += self.vel.x * PLAYER_FRICTION  # apply friction
        self.vel += self.acc  # calculate velocity
        self.pos += self.vel + (0.5 * self.acc)  # calculate position

        #states
        if self.state == IDLING:
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
        elif self.state == WALKING_RIGHT:
            self.image = self.walkFrames_R[int(self.walkFrame_R/self.walkSpeed)]
            self.walkFrame_R += 1
            if self.walkFrame_R >= len((self.walkFrames_R * self.walkSpeed)):
                self.walkFrame_R = 0
        elif self.state == WALKING_LEFT:
            self.image = self.walkFrames_L[int(self.walkFrame_L/self.walkSpeed)]
            self.walkFrame_L += 1
            if self.walkFrame_L >= len((self.walkFrames_L * self.walkSpeed)):
                self.walkFrame_L = 0
        elif self.state == JUMPING:
            if self.direction == LEFT:
                self.image = self.jumpFrames_L[int(self.jumpFrame_L/self.jumpSpeed)]
                self.jumpFrame_L += 1
                if self.jumpFrame_L >= len((self.jumpFrames_L * self.jumpSpeed)):
                    self.jumpFrame_L = 0
            if self.direction == RIGHT:
                self.image = self.jumpFrames_R[int(self.jumpFrame_R/self.jumpSpeed)]
                self.jumpFrame_R += 1
                if self.jumpFrame_R >= len((self.jumpFrames_R * self.jumpSpeed)):
                    self.jumpFrame_R = 0
        elif self.state == FALLING:
            if self.direction == LEFT:
                self.image = self.fallFrames_L[int(self.fallFrame_L/self.fallSpeed)]
                self.fallFrame_L += 1
                if self.fallFrame_L >= len((self.fallFrames_L * self.fallSpeed)):
                    self.fallFrame_L = 0
            if self.direction == RIGHT:
                self.image = self.fallFrames_R[int(self.fallFrame_R/self.fallSpeed)]
                self.fallFrame_R += 1
                if self.fallFrame_R >= len((self.fallFrames_R * self.fallSpeed)):
                    self.fallFrame_R = 0
        elif self.state == ATTACKING:
            if self.direction == LEFT:
                self.image = self.attackFrames_L[int(self.attackFrame_L/self.attackSpeed)]
                self.attackFrame_L += 1
                if self.attackFrame_L >= len((self.attackFrames_L * self.attackSpeed)):
                    self.attackFrame_L = 0
            if self.direction == RIGHT:
                self.image = self.attackFrames_R[int(self.attackFrame_R/self.attackSpeed)]
                self.attackFrame_R += 1
                if self.attackFrame_R >= len((self.attackFrames_R * self.attackSpeed)):
                    self.attackFrame_R = 0

        if self.pos.x >= WINDOW_WIDTH + self.width:
            self.pos.x = WINDOW_WIDTH + self.width
        if self.pos.x <= 0 + self.width/8:
            self.pos.x = 0 + self.width/8
        if (self.pos.y >= 538.675) and (self.levelState == GOBLIN_LOWER):
            self.pos.y = 535

        try:
            # determine collision based on pixel color from collision map
            for pixel in range(int(self.pos.y + self.height), int((self.pos.y + self.height) + self.halfHeight + 1)):
                self.color_DOWN = self.collision_map.get_at((int(self.pos.x), int(pixel)))
                if self.color_DOWN == HIT and self.vel.y > 0:
                    self.vel.y = 0
                    self.pos.y = pixel - self.height - 1
                    self.collision = True
                    self.state = IDLING
                    break
                else:
                    self.acc = VEC(0,PLAYER_GRAVITY)
            return self.pos.y
        except:
            self.acc = VEC(0,PLAYER_GRAVITY)
            return self.pos.y



    def handleInputs(self, eventsList, keyPressedList):
        self.eventsList = eventsList
        self.keyPressedList = keyPressedList

        if keyPressedList[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
            self.direction = LEFT
            if self.state == IDLING:
                self.state = WALKING_LEFT
            #myAnimation.start()
        if keyPressedList[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            self.direction = RIGHT

            if self.state == IDLING:
                self.state = WALKING_RIGHT
            #myAnimation.start()
        if keyPressedList[pygame.K_DOWN]:
            self.pos.y = self.pos.y + 2

        if keyPressedList[pygame.K_r]:
            self.state = ATTACKING

        for event in eventsList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.collision == True:
                        self.jump()
                elif event.key == pygame.K_UP:
                    if self.collision == True:
                        self.jump()
                elif event.key == pygame.K_RETURN:
                    if self.interact == True:
                        pass
                        #tell sceneplay that interact key was pressed
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.state = FALLING
                else:
                    self.state = IDLING

        self.rect.left = self.pos.x
        self.rect.top = self.pos.y

    def draw(self):
        self.window.blit(self.image, (self.pos.x, self.pos.y))

    def getRect(self):
        return self.rect

    def panCam(self, direction):
        self.direction = direction

        if self.direction == 'Up':
            if (self.pos.y <= 0) and (self.levelState == GOBLIN_LOWER):
                self.collision_map = pygame.image.load(CM_LEVEL_2)
                self.pos.y = 394
                self.levelState = GOBLIN_UPPER
            elif (self.pos.y <= 0) and (self.levelState == GOBLIN_UPPER):
                self.collision_map = pygame.image.load(CM_LEVEL_3)
                self.pos.y = 380
                self.levelState = CITY_LOWER
            elif (self.pos.y <= 0) and (self.levelState == CITY_LOWER):
                self.collision_map = pygame.image.load(CM_LEVEL_4)
                self.pos.y = WINDOW_HEIGHT - 50
                self.levelState = CITY_UPPER
            elif (self.pos.y <= 0) and (self.levelState == CITY_UPPER):
                self.collision_map = pygame.image.load(CM_LEVEL_5)
                self.pos.y = WINDOW_HEIGHT - 50
                self.levelState = LEVEL_END


        else:
            if (self.pos.y > WINDOW_HEIGHT) and (self.levelState == GOBLIN_UPPER):
                self.collision_map = pygame.image.load(CM_LEVEL_1)
                self.pos.y = 198
                self.levelState = GOBLIN_LOWER
            elif (self.pos.y > WINDOW_HEIGHT) and (self.levelState == CITY_LOWER):
                self.collision_map = pygame.image.load(CM_LEVEL_2)
                self.pos.y = 160
                self.levelState = GOBLIN_UPPER
            elif (self.pos.y > WINDOW_HEIGHT) and (self.levelState == CITY_UPPER):
                self.collision_map = pygame.image.load(CM_LEVEL_3)
                self.levelState = CITY_LOWER
                self.pos.y = 50
            elif (self.pos.y > WINDOW_HEIGHT) and (self.levelState == LEVEL_END):
                self.collision_map = pygame.image.load(CM_LEVEL_4)
                self.levelState = CITY_UPPER
                self.pos.y = 50

    def jump(self):
        self.vel.y = -PLAYER_JUMP
        self.state = JUMPING
        self.collision = False
        self.falling()

    def falling(self):
        self.state = FALLING

    def dying(self,keys):
        pass
