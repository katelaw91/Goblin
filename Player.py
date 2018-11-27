### PLAYER
import pygame
from Constants import *

class Player():
    def __init__(self, window):
        self.window = window
        self.image = pygame.image.load('images/goblin_R1.png')
        self.rect = self.image.get_rect()
        self.rect.center = (50, WINDOW_HEIGHT + 50)  # set player to starting position
        self.height = self.rect.height
        self.halfHeight = self.height / 2
        self.width = self.rect.width
        self.halfWidth = self.width / 2

        self.maxX = WINDOW_WIDTH - self.rect.width
        self.maxY = GAME_HEIGHT - self.rect.height

        self.currentFrame = 0  # up to number of frames in an animation
        self.state = WALKLEFT

        #VEC(X,Y)
        self.pos = VEC(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.vel = VEC(0,0)
        self.acc = VEC(0,0)

        # instantiate collision platforms
        self.collision_map = pygame.Surface((540, 960))
        self.collision_map.blit(pygame.image.load(IMAGE_COLLISION_MAP), (0, 0))
        self.ground = pygame.draw.line(self.collision_map, BLACK, (0, WINDOW_HEIGHT), (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.collide_DOWN = False
        self.collide_RIGHT = False
        self.collide_LEFT = False

        self.color_DOWN = WHITE
        self.color_LEFT = WHITE
        self.color_RIGHT = WHITE


    def reset(self):
        self.rect.center = (50, WINDOW_HEIGHT + 50)
        self.state = WALKLEFT


    def update(self):
        self.acc = VEC(0, PLAYER_GRAVITY)  # calculate acceleration

       # motion
        self.acc.x += self.vel.x * PLAYER_FRICTION  # apply friction
        self.vel += self.acc  # calculate velocity
        self.pos += self.vel + (0.5 * self.acc)  # calculate position

        '''#do not pass sides of screen
        if self.pos.x > WINDOW_WIDTH:
            self.pos.x = WINDOW_WIDTH
        if self.pos.x < 0:
            self.pos.x = 0'''

        '''#do not fall off screen
        if self.pos.y > WINDOW_HEIGHT - self.height:
            self.pos.y = WINDOW_HEIGHT - self.height + 1
            self.vel.y = 0
            self.state = WALKLEFT'''

        # determine collision based on pixel color from collision map
        if ((self.pos.y + 1) < WINDOW_HEIGHT):
            self.color_DOWN = self.collision_map.get_at((int(self.pos.x), int(self.pos.y + 1)))
            print('color down value', self.color_DOWN)

        if ((self.pos.x +1) < WINDOW_WIDTH) and (self.pos.y < WINDOW_HEIGHT):
            self.color_RIGHT = self.collision_map.get_at((int(self.pos.x + 1), int(self.pos.y)))
            print('color right value', self.color_RIGHT)
        if ((self.pos.x -1) > 0) and (self.pos.y < WINDOW_HEIGHT):
            self.color_LEFT = self.collision_map.get_at((int(self.pos.x - 1), int(self.pos.y)))
            print('color left value', self.color_LEFT)

        if self.color_DOWN == HIT:
            self.collide_DOWN = True
            print("Collision beneath")
        if self.color_RIGHT == HIT:
            self.collide_RIGHT = True
            print("Collision to the right")
        if self.color_LEFT == HIT:
            self.collide_LEFT = True
            print("Collision to the left")

        if self.collide_DOWN:
            self.pos.y = self.pos.y
            self.vel.y = 0

        '''self.Rect = pygame.Rect(self.pos.x, self.pos.y, self.height, self.width)
        return self.Rect'''

    def handleInputs(self, eventsList, keyPressedList):
        self.eventsList = eventsList
        self.keyPressedList = keyPressedList

        if keyPressedList[pygame.K_LEFT]:
            print('Pressing Left')
            if not self.collide_LEFT:
                self.acc.x = -PLAYER_ACC
            self.state = WALKLEFT
        if keyPressedList[pygame.K_RIGHT]:
            print('Pressing Right')
            if not self.collide_RIGHT:
                self.acc.x = PLAYER_ACC
            self.state = WALKRIGHT

        for event in eventsList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print('Keydown Space')
                    if self.collide_DOWN:
                        self.state = JUMP
                        self.jumping()

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
        elif self.state == DEATH:
            #play animation and sounds
            #return state so scenemgr can play gameover screen
            pass

    def getFrame(self):
        return self.currentFrame

    def setPos(self, collision, x,y):
        self.collision = collision
        self.x = x
        self.y = y
        if collision == True:
            self.pos.x = self.x
            self.pos.y = self.y

    def getPos(self, xOrY):
        if xOrY == 'y':
            return self.rect.centery
        elif xOrY == 'x':
            return self.rect.centerx
        else:
            return self.rect.midbottom

    def setVel(self, collision):
        self.collision = collision
        if collision == True:
            self.vel.y = 0

    def getVel(self, xOrY):
        if xOrY == 'y':
            return self.vel.y
        elif xOrY == 'x':
            return self.vel.x
        else:
            return self.vel

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

    def falling(self,keys):
        pass

    def dying(self,keys):
        pass

