#  1/18    by Irv Kalb
#
#  Added dialogs
#  Split program into scenes, uses Scene Manager
#  Added 'Goodies' (and Goodie Manager)
#  Changed the scoring mechanism and display.
#  Saves high scores to file.
#  Re-wrote to be object oriented, built Baddie Manager
#
#  Original version by Al Swiegart from his book "Invent With Python"
#    (concept, graphics, and sounds used by permission from Al Swiegart)

import pygame
from pygame.locals import *
import random
import sys
import pygwidgets
import SceneManager
from Constants import *
from Player import *
from Villagers import *
from Goblins import *


class ScenePlay(SceneManager.Scene):

    def __init__(self, window, sceneKey):
        # Save window and sceneKey in instance variables
        self.window = window
        self.sceneKey = sceneKey
        self.playBackground = pygwidgets.Image(self.window, (0, -320), IMAGE_LEVEL_1)

        #instantiate objects
        self.oVillagerMgr = VillagerMgr(self.window)
        self.oGoblinMgr = GoblinMgr(self.window)
        self.oPlayer = Player(self.window)

        self.deathCount = 0
        self.backgroundMusic = True

        #instantiate collision platforms
        self.collision_map = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.collision_map.blit(pygame.image.load(IMAGE_COLLISION_MAP), (0,-320))
        self.ground = pygame.draw.line(self.collision_map,BLACK,(0,WINDOW_HEIGHT), (WINDOW_WIDTH,WINDOW_HEIGHT))

        self.collision = False
        self.HIT = BLACK
        self.posX = self.oPlayer.getPos('x')
        self.posY = self.oPlayer.getPos('y')
        self.velY = self.oPlayer.getVel('y')
        self.pos = self.oPlayer.getPos('z')



    def enter(self, data):  # no data passed in
        pygame.mixer.music.stop()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.mixer.music.load(MUSIC_GOBLINS)
        pygame.display.update()
        self.dingSound = pygame.mixer.Sound('sounds/ding.wav')
        self.gameOverSound = pygame.mixer.Sound('sounds/lose sound 1_0.wav')
        self.reset()

    # Start a new game
    def reset(self):
        self.deathCount = 0

        # Tell the managers to reset themselves
        self.oPlayer.reset()
        self.oVillagerMgr.reset()
        self.oGoblinMgr.reset()

        if self.backgroundMusic:
            pygame.mixer.music.play(-1, 0.0)
        self.playing = True


    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:
            pass
        #add keybinding here
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.oPlayer.setPos(keys, self.posX, self.posY)
        if keys[pygame.K_SPACE]:
            self.oPlayer.setFrame(keys)




    def update(self):
        if self.playing:
            playerRect = self.oPlayer.update()  # move the player


            #determine collision based on pixel color from collision map
            self.color = self.collision_map.get_at(self.pos)

            for check_pixel in range(self.posY, self.posY + int(self.velY)):
                color = self.collision_map.get_at((self.posX, check_pixel))
                if color == self.HIT:
                    self.collision = True
                    print("Colliding with pixel at (", self.posX, ',', check_pixel, ')')
                    self.oPlayer.setPos(self.collision, self.posX, check_pixel)
                    break

            # Tell the Baddie mgr to move all the baddies
            # It returns the number of baddies that fell off the bottom
            nDeaths = self.oVillagerMgr.update()
            self.deathCount = self.deathCount + nDeaths
    
            # Tell the Goodie mgr to move any goodies
            self.oGoblinMgr.update()

            # Check if the player has hit any of the goodies
            #print('In ScenePlay, self.oPlayer', self.oPlayer)
            if self.oGoblinMgr.hasPlayerHitGoblin(self.oPlayer):
                pass
                #update Player about collision so it can interact

            # Check if the player has hit any of the baddies
            if self.oVillagerMgr.hasPlayerHitVillager(playerRect):
                pass
                #update Player about collision so it can attack
    
    def draw(self):
        # Draw everything
        self.window.fill(BLACK)
        self.playBackground.draw()
    
        # Tell the managers to draw all the baddies & goodies
        self.oVillagerMgr.draw()
        self.oGoblinMgr.draw()
    
        # Draw the player
        self.oPlayer.draw()

        if not self.playing:
            self.gameOverImage.draw()


    def leave(self):
        pygame.mixer.music.stop()
