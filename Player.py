### PLAYER
import pygame
from Constants import *

class Player():
    def __init__(self, window):
        self.window = window
        self.image = pygame.image.load('images/goblin_R1.png')
        self.rect = self.image.get_rect()
        self.height = self.rect.height
        self.halfHeight = self.height / 2
        self.width = self.rect.width
        self.halfWidth = self.width / 2

        self.maxX = WINDOW_WIDTH - self.rect.width
        self.maxY = GAME_HEIGHT - self.rect.height

        self.currentFrame = 0  # up to number of frames in an animation
        self.state = WALKLEFT

        #VEC(X,Y)
        self.pos = VEC(50, 450)
        self.vel = VEC(0,0)
        self.acc = VEC(0,0)

        # instantiate collision platforms
        self.collision_map = pygame.image.load(IMAGE_COLLISION_MAP)

        self.collide_DOWN = False
        self.collide_RIGHT = False
        self.collide_LEFT = False

        self.color_DOWN = TEAL
        self.color_LEFT = TEAL
        self.color_RIGHT = TEAL


    def reset(self):
        self.rect.center = (50, WINDOW_HEIGHT + 50)
        self.state = WALKLEFT


    def update(self):
        self.collision = False
        self.camera = 0

       # motion
        self.acc.x += self.vel.x * PLAYER_FRICTION  # apply friction
        self.vel += self.acc  # calculate velocity
        self.pos += self.vel + (0.5 * self.acc)  # calculate position


        # determine collision based on pixel color from collision map
        for pixel in range(int(self.pos.y + self.height), int((self.pos.y + self.height) + self.halfHeight + 1)):
            self.color_DOWN = self.collision_map.get_at((int(self.pos.x), int(pixel - OFFSET + self.camera)))
            if self.color_DOWN == HIT and self.vel.y > 0:
                self.vel.y = 0
                self.pos.y = pixel - self.height - 1
                self.collision = True
                break
            else:
                self.acc = VEC(0,PLAYER_GRAVITY)


    def handleInputs(self, eventsList, keyPressedList):
        self.eventsList = eventsList
        self.keyPressedList = keyPressedList

        if keyPressedList[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
            self.state = WALKLEFT
        if keyPressedList[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            self.state = WALKRIGHT
        if keyPressedList[pygame.K_DOWN]:
            self.pos.y = self.pos.y + 2

        for event in eventsList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print('Keydown Space')
                    print('vel: ', self.vel.y)
                    if self.state != FALL:
                        self.state = JUMP
                        self.jumping()
                elif event.key == pygame.K_RETURN:
                    if self.interact == True:
                        pass
                        #tell sceneplay that interact key was pressed

    def draw(self):
        self.window.blit(self.image, (self.pos.x, self.pos.y))

    def setFrame(self, keys):
        if self.state == WALKLEFT:
            #set animation for walkleft
            self.currentFrame = 0
        if self.state == WALKRIGHT:
            #set animation for walkright
            self.currentFrame = 0
        elif self.state == JUMP:
            self.jumping()
            self.currentFrame = 0
        elif self.state == FALL:
            self.falling()
        elif self.state == DEATH:
            #play animation and sounds
            #return state so scenemgr can play gameover screen
            pass

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

    def panCam(self):
        self.pos.y += abs(self.vel.y)

    def walking(self,direction):
        self.direction = direction
        if direction == 'R':
            #insert frames for R
            pass
        elif direction == 'L':
            #insert frames for L
            pass

    def jumping(self):
        self.vel.y = -PLAYER_JUMP
        self.state = FALL

    def falling(self,keys):
        if self.vel.y != -PLAYER_JUMP:
            self.state = WALKLEFT

    def dying(self,keys):
        pass

    def interact(self, TorF):
        self.TorF = TorF
        if TorF == True:
            self.interact = True
        else:
            self.interact = False

