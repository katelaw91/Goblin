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


        #state/animation variables
        self.currentFrame = 0  # up to number of frames in an animation
        self.last_update = 0
        self.idling = True
        self.walking_R = False
        self.walking_L = False
        self.jumping = False
        self.spritesheet = pygame.image.load(SPRITESHEET_PLAYER).convert()
        self.frames = []

        for n in range(14):
            width = 26
            height = 31.5
            rect = pygame.Rect(n*width, 0, width, height)
            image = pygame.Surface(rect.size).convert()
            image.blit(self.spritesheet, (0,0), rect)
            alpha = image.get_at((0,0))
            image.set_colorkey(alpha)
            self.frames.append(image)

        self.idleFrames = self.frames[8:14]
        self.walkFrames_R = self.frames[:9]
        self.walkFrames_R = self.walkFrames_R[::-1]
        self.walkFrames_L = self.frames[:9]
        self.walkFrames_L = self.walkFrames_L[::-1]
        self.jumpFrames = self.frames[13:18]


        for frame in range(9):
            self.walkFrames_L.append(pygame.transform.flip(self.walkFrames_L[frame], True, False))

        self.idleFrame = 0
        self.idleSpeed = 16
        self.walkFrame_R = 0
        self.walkFrame_L = 0
        self.walkSpeed = 8
        self.jumpFrame = 0
        self.jumpSpeed = 8
        self.fallFrame = 0
        self.fallSpeed = 5

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

        if self.idling:
            self.image = self.idleFrames[int(self.idleFrame/self.idleSpeed)]
            self.idleFrame += 1
            if self.idleFrame >= len((self.idleFrames * self.idleSpeed)):
                self.idleFrame = 0
        if self.walking_R:
            self.walking_L = False
            self.idling = False
            self.image = self.walkFrames_R[int(self.walkFrame_R/self.walkSpeed)]
            self.walkFrame_R += 1
            if self.walkFrame_R >= len((self.walkFrames_R * self.walkSpeed)):
                self.walkFrame_R = 0
        if self.walking_L:
            self.walking_R = False
            self.idling = False
            self.image = self.walkFrames_L[int(self.walkFrame_L/self.walkSpeed)]
            self.walkFrame_L += 1
            if self.walkFrame_L >= len((self.walkFrames_L * self.walkSpeed)):
                self.walkFrame_L = 0
        if self.jumping:
            self.walking_R = False
            self.walking_L = False
            self.idling = False
            self.image = self.jumpFrames[int(self.jumpFrame/self.jumpSpeed)]
            self.jumpFrame += 1
            if self.jumpFrame >= len((self.jumpFrames * self.jumpSpeed)):
                self.jumpFrame = 0

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
                    self.idling = True
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
            self.walking_L = True
            self.idling = False
            self.state = WALKING_LEFT
            #myAnimation.start()
        if keyPressedList[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            self.walking_R = True
            self.idling = False
            self.state = WALKING_RIGHT
            #myAnimation.start()
        if keyPressedList[pygame.K_DOWN]:
            self.pos.y = self.pos.y + 2

        for event in eventsList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.collision == True:
                        self.jump()
                        self.jumping = True
                        self.idling = False
                        self.walking_L = False
                        self.walking_R = False
                        self.state = JUMPING
                elif event.key == pygame.K_RETURN:
                    if self.interact == True:
                        pass
                        #tell sceneplay that interact key was pressed
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.state = FALLING
                else:
                    self.idling = True
                    self.walking_L = False
                    self.walking_R = False
                    self.jumping = False
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
        self.collision = False
        self.jumping = True
        self.idling = False
        self.walking = False

    def dying(self,keys):
        pass

    '''def interact(self, TorF):
        self.TorF = TorF
        if TorF == True:
            self.interact = True
        else:
            self.interact = False'''

