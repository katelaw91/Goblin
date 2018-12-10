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
        self.playBackground = pygwidgets.Image(self.window, (0, OFFSET), IMAGE_LEVEL_1)
        self.atmosphere = pygwidgets.Image(self.window, (0,0), ATMOSPHERE)
        self.glow = pygwidgets.Image(self.window, (0, OFFSET), GLOW)
        self.vines = pygwidgets.Image(self.window,(0,OFFSET), VINES)
        #y -320
        self.levelState = GOBLIN_LOWER

        #instantiate objects
        self.oVillagerMgr = VillagerMgr(self.window)
        self.oGoblinMgr = GoblinMgr(self.window)
        self.oPlayer = Player(self.window)

        self.deathCount = 0
        self.backgroundMusic = True


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
        self.oPlayer.handleInputs(eventsList, keyPressedList)
        self.oGoblinMgr.handleInputs(eventsList, keyPressedList)

    def update(self):
        if self.playing:
            self.playerY = self.oPlayer.update()  # move the player
            self.oVillagerMgr.update()
            self.oGoblinMgr.update()

            self.playerRect = self.oPlayer.getRect()


            # Check if the player collides with goblins
            if self.oGoblinMgr.hasPlayerHitGoblin(self.playerRect):
                pass

                #update Player about collision so it can interact

            # Check if the player has hit any of the baddies
            '''if self.oVillagerMgr.hasPlayerHitVillager(playerRect):
                pass
                #update Player about collision so it can attack'''

            #self.collision = self.oGoblinMgr.detectCollision(self.playerRect)


        #PAN CAMERA UP
        if self.playerY <= WINDOW_HEIGHT/6:
            self.oPlayer.panCam('Up')
            self.playBackground = pygwidgets.Image(self.window, (0, OFFSET + 350), IMAGE_LEVEL_1)
            #self.atmosphere = pygwidgets.Image(self.window, (0,0 + 300), ATMOSPHERE)
            self.glow = pygwidgets.Image(self.window, (0, OFFSET + 350), GLOW)
            self.vines = pygwidgets.Image(self.window, (0, OFFSET + 350), VINES)

            self.oGoblinMgr.panCam('Up')
            self.levelState = GOBLIN_UPPER

        #PAN CAMERA DOWN
        if self.playerY > WINDOW_HEIGHT:
            self.oPlayer.panCam('Down')
            self.playBackground = pygwidgets.Image(self.window, (0, OFFSET), IMAGE_LEVEL_1)
            #self.atmosphere = pygwidgets.Image(self.window, (0,0 + 300), ATMOSPHERE)
            self.glow = pygwidgets.Image(self.window, (0, OFFSET), GLOW)
            self.vines = pygwidgets.Image(self.window, (0, OFFSET), VINES)

            self.oGoblinMgr.panCam('Down')
            self.levelState = GOBLIN_LOWER
    
    def draw(self):
        # Draw everything
        self.window.fill(BLACK)
        self.playBackground.draw()
        self.vines.draw()
        self.atmosphere.draw()
        self.glow.draw()
    
        # Tell the managers to draw all the baddies & goodies
        self.oVillagerMgr.draw()
        self.oGoblinMgr.draw()
    
        # Draw the player
        self.oPlayer.draw()

        if not self.playing:
            self.gameOverImage.draw()


    def leave(self):
        pygame.mixer.music.stop()
