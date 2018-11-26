### PLAYER
import pygame
from Constants import *

class Player():
    def __init__(self, window):
        self.window = window
        self.image = pygame.image.load('images/goblin_R1.png')
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH /2, WINDOW_HEIGHT/ 2)  # set player to center of screen
        self.height = self.rect.height
        self.halfHeight = self.height / 2
        self.width = self.rect.width
        self.halfWidth = self.width / 2

        self.maxX = WINDOW_WIDTH - self.rect.width
        self.maxY = GAME_HEIGHT - self.rect.height

        self.currentFrame = 0  # up to number of frames in an animation
        self.state = STAND

        #VEC(X,Y)
        self.pos = VEC(WINDOW_WIDTH/2, WINDOW_HEIGHT + 10)
        self.vel = VEC(0,0)
        self.acc = VEC(0,0)
        self.x = self.pos.x
        self.y = self.pos.y

    def update(self):
        self.acc = VEC(0, PLAYER_GRAVITY)  # calculate acceleration

       # motion
        self.acc.x += self.vel.x * PLAYER_FRICTION  # apply friction
        self.vel += self.acc  # calculate velocity
        self.pos += self.vel + (0.5 * self.acc)  # calculate position

        #do not pass sides of screen
        if self.pos.x > WINDOW_WIDTH:
            self.pos.x = WINDOW_WIDTH
        if self.pos.x < 0:
            self.pos.x = 0

        theRect = pygame.Rect(self.pos.x, self.pos.y, self.height, self.width)
        return self.rect

    def draw(self):
        self.window.blit(self.image, (self.pos.x, self.pos.y))

    def setFrame(self, key_input):
        if self.state == STAND:
            self.standing(keys)
        elif self.state == WALK:
            self.walking(keys)
        elif self.state == JUMP:
            self.jumping(keys)
        elif self.state == FALL:
            self.falling(keys)
        elif self.state == DEATH:
            self.dying(keys)

    def getFrame(self):
        return self.currentFrame

    def setPos(self, collision, x,y):
        self.collision = collision
        if collision == True:
            self.pos = (x,y)

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
            self.vel.y = VEC(0, 0)

    def getVel(self, xOrY):
        if xOrY == 'y':
            return self.vel.y
        elif xOrY == 'x':
            return self.vel.x
        else:
            return self.vel

    def standing(self, keys):
        self.interact = False
        self.frame_index = 0
        self.vel = VEC(0,0)
        self.acc = VEC(0,0)

        if keys[pygame.K_LEFT]:
            self.walking(keys)
        if keys[pygame.K_RIGHT]:
            self.walking(keys)
        if collision:
            if keys[pygame.K_RETURN]:
                self.interact = True

    def walking(self,keys):
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC

    def jumping(self,keys):
        if not collide:
            if keys[pygame.K_SPACE]:
                self.vel.y = -PLAYER_JUMP
    def falling(self,keys):
        pass

    def dying(self,keys):
        pass

