### PLAYER
import pygame
import pygwidgets
from Constants import *

class Player():
    def __init__(self, window):
        self.window = window
        #self.image = pygame.image.load('images/goblin_R1.png')
        self.level_bottom = True
        self.level_top = False
        self.interact = False
        self.collision = False
        self.state = IDLING
        self.direction = RIGHT

        #state/animation variables
        self.currentFrame = 0  # up to number of frames in an animation
        self.last_update = 0
        self.spritesheet = pygame.image.load(SPRITESHEET_PLAYER).convert()
        self.frames = []

        for n in range(18):
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
        self.fallFrames_L = self.frames[16:]
        self.fallFrames_R = self.frames[16:]

        for frame in range(5):
            self.idleFrames_L.append(pygame.transform.flip(self.idleFrames_L[frame], True, False))
        self.idleFrames_L = self.idleFrames_L[6:]
        print("self.idleFrames_L: ", len(self.idleFrames_L))

        for frame in range(8):
            self.walkFrames_L.append(pygame.transform.flip(self.walkFrames_L[frame], True, False))
        self.walkFrames_L = self.walkFrames_L[9:]
        print("self.walkFrames_L: ", len(self.walkFrames_L))

        for frame in range(3):
            self.jumpFrames_L.append(pygame.transform.flip(self.jumpFrames_L[frame], True, False))
        self.jumpFrames_L = self.jumpFrames_L[4:]
        print("self.jumpFrames_L: ", len(self.jumpFrames_L))

        for frame in range(2):
            self.fallFrames_L.append(pygame.transform.flip(self.fallFrames_L[frame], True, False))
        self.fallFrames_L = self.fallFrames_L[3:]
        print("self.fallFrames_L: ", len(self.fallFrames_L))

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
        self.collision_map = pygame.image.load(IMAGE_COLLISION_MAP)

        self.collide_DOWN = False
        self.collide_RIGHT = False
        self.collide_LEFT = False

        self.color_DOWN = TEAL
        self.color_LEFT = TEAL
        self.color_RIGHT = TEAL

        #self.myAnimation = pygwidgets.SpriteSheetAnimation(window, (self.pos.x, self.pos.y), SPRITESHEET_PLAYER, 14, 14, 26, 38, 2)

    def reset(self):
        self.rect.center = (50, WINDOW_HEIGHT + 50)

    def update(self):
        self.camera = 0
        #self.animate()

       #motion
        self.acc.x += self.vel.x * PLAYER_FRICTION  # apply friction
        self.vel += self.acc  # calculate velocity
        self.pos += self.vel + (0.5 * self.acc)  # calculate position

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

        if self.pos.x >= WINDOW_WIDTH - self.width:
            self.pos.x = WINDOW_WIDTH - self.width
        if self.pos.x <= 0 + self.width/2:
            self.pos.x = 0 + self.width/2
        if (self.pos.y >= 538.675) and (self.level_bottom == True):
            self.pos.y = 535

        try:
            # determine collision based on pixel color from collision map
            for pixel in range(int(self.pos.y + self.height), int((self.pos.y + self.height) + self.halfHeight + 1)):
                self.color_DOWN = self.collision_map.get_at((int(self.pos.x), int(pixel - OFFSET + self.camera)))
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

        for event in eventsList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
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

    '''def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 250:
            self.last_update = now
            self.currentFrame = (self.currentFrame + 1) % len(self.framesList)
            self.image = self.framesList[self.currentFrame]
            if self.currentFrame >= len(self.framesList):
                print(self.currentFrame)
                print(self.framesList[self.currentFrame])
                self.currentFrame = 0'''

    '''def setFrame(self, keys):
        if self.state == WALKRIGHT:
            #set animation for walkright
            self.currentFrame = 0
            self.framesList = [pygame.image.load('images/goblin_R1.png'),\
                                                 pygame.image.load('images/goblin_R2.png')]
        if self.state == WALKLEFT:
            #set animation for walkleft
            self.framesList = [pygame.image.load('images/goblin_R1.png'),\
                               pygame.image.load('images/goblin_R2.png')]

            for frame in self.framesList:
                self.framesList.append(pygame.transform.flip(frame,True,False))

            self.currentFrame = 0
        elif self.state == JUMP:
            self.jumping()
            self.currentFrame = 0
        elif self.state == FALL:
            self.falling()
        elif self.state == DEATH:
            #play animation and sounds
            #return state so scenemgr can play gameover screen
            pass'''

    def getFrame(self):
        return self.currentFrame

    def getPos(self, xOrY):
        if xOrY == 'y':
            return self.rect.centery
        elif xOrY == 'x':
            return self.rect.centerx
        else:
            return self.rect.midbottom

    def getVel(self, xOrY):
        if xOrY == 'y':
            return self.vel.y
        elif xOrY == 'x':
            return self.vel.x
        else:
            return self.vel

    def getRect(self):
        return self.rect

    def panCam(self, direction):
        self.direction = direction

        if self.direction == 'Up':
            if (self.pos.y <= WINDOW_HEIGHT/6) and (self.level_top == False):
                print("Reached top of screen")
                self.pos.y = WINDOW_HEIGHT - (WINDOW_HEIGHT/6)
                self.collision_map.scroll(dx=0, dy=350)
                self.level_bottom = False
                self.level_top = True
            elif (self.pos.y <= WINDOW_HEIGHT/4) and (self.level_top == True):
                pass
        else:
            if self.pos.y > WINDOW_HEIGHT:
                print("Reached bottom of screen")
                self.pos.y = WINDOW_HEIGHT/6 + 130
                self.collision_map = pygame.image.load(IMAGE_COLLISION_MAP)
                self.level_bottom = True
                self.level_top = False

    def jump(self):
        self.vel.y = -PLAYER_JUMP
        self.state = JUMPING
        self.collision = False
        self.falling()

    def falling(self):
        self.state = FALLING

    def dying(self,keys):
        pass

    '''def interact(self, TorF):
        self.TorF = TorF
        if TorF == True:
            self.interact = True
        else:
            self.interact = False'''

