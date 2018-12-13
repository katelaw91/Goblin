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
        self.playBackground = pygwidgets.Image(self.window, (0, 0), IMAGE_LEVEL_1)
        self.atmosphere = pygwidgets.Image(self.window, (0,0), ATMOSPHERE)
        self.glow = pygwidgets.Image(self.window, (0, 0), GLOW_LEVEL_1)
        self.levelState = GOBLIN_LOWER

        #instantiate objects
        self.oVillagersMgr = VillagersMgr(self.window)
        self.oGoblinMgr = GoblinMgr(self.window)
        self.oPlayer = Player(self.window)

        self.deathCount = 0
        self.backgroundMusic = True


    def enter(self, data):  # no data passed in
        pygame.mixer.music.stop()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.mixer.music.load(MUSIC_GOBLINS)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(AMBIENCE_GOBLIN), -1)
        pygame.mixer.Channel(2).play(pygame.mixer.Sound(AMBIENCE_WATERFALL),-1)
        pygame.mixer.Channel(1).set_volume(0.5)
        pygame.mixer.Channel(2).set_volume(0.5)

        pygame.display.update()
        self.dingSound = pygame.mixer.Sound('sounds/ding.wav')
        self.gameOverSound = pygame.mixer.Sound('sounds/lose sound 1_0.wav')
        self.reset()

    # Start a new game
    def reset(self):
        self.deathCount = 0

        # Tell the managers to reset themselves
        self.oPlayer.reset()
        self.oVillagersMgr.reset()
        self.oGoblinMgr.reset()

        if self.backgroundMusic:
            pygame.mixer.music.play(-1, 0.0)
        self.playing = True


    def handleInputs(self, eventsList, keyPressedList):
        self.oPlayer.handleInputs(eventsList, keyPressedList)
        self.oGoblinMgr.handleInputs(eventsList, keyPressedList)
        self.oVillagersMgr.handleInputs(eventsList, keyPressedList)


    def update(self):
        if self.playing:
            self.playerY = self.oPlayer.update()  # move the player
            self.oVillagersMgr.update()
            self.oGoblinMgr.update()

            self.playerRect = self.oPlayer.getRect()

            # Check if the player collides with npcs
            if self.oGoblinMgr.hasPlayerHitGoblin(self.playerRect):
                pass
            if self.oVillagersMgr.hasPlayerHitVillager(self.playerRect):
                pass


        #PAN CAMERA UP
        if (self.playerY <= 0) and (self.levelState == GOBLIN_LOWER):
            self.oPlayer.panCam('Up')
            self.oGoblinMgr.panCam('Up', self.levelState)
            self.oVillagersMgr.panCam('Up', self.levelState)
            self.playBackground = pygwidgets.Image(self.window, (0, 0), IMAGE_LEVEL_2)
            self.glow = pygwidgets.Image(self.window, (0, 0), GLOW_LEVEL_2)
            self.levelState = GOBLIN_UPPER

        elif (self.playerY <= 0) and (self.levelState == GOBLIN_UPPER):
            self.oPlayer.panCam('Up')
            self.oGoblinMgr.panCam('Up', self.levelState)
            self.oVillagersMgr.panCam('Up', self.levelState)
            self.playBackground = pygwidgets.Image(self.window, (0, 0), IMAGE_LEVEL_3)
            self.glow = pygwidgets.Image(self.window, (0, 0), GLOW_LEVEL_3)
            self.levelState = CITY_LOWER
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(MUSIC_TRANSITION), -1)
            pygame.mixer.music.stop()


        elif (self.playerY <= 0) and (self.levelState == CITY_LOWER):
            self.oPlayer.panCam('Up')
            self.oGoblinMgr.panCam('Up', self.levelState)
            self.oVillagersMgr.panCam('Up', self.levelState)
            self.playBackground = pygwidgets.Image(self.window, (0, 0), IMAGE_LEVEL_4)
            self.glow = pygwidgets.Image(self.window, (0, 0), GLOW_LEVEL_4)
            self.levelState = CITY_UPPER
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(MUSIC_VILLAGERS), -1)


        elif (self.playerY <= 0) and (self.levelState == CITY_UPPER):
            self.oPlayer.panCam('Up')
            self.oGoblinMgr.panCam('Up', self.levelState)
            self.oVillagersMgr.panCam('Up', self.levelState)
            self.playBackground = pygwidgets.Image(self.window, (0, 0), IMAGE_LEVEL_5)
            self.glow = pygwidgets.Image(self.window, (0, 0), GLOW_LEVEL_5)
            self.levelState = LEVEL_END
            print("reached the top of the city")

        #PAN CAMERA DOWN
        if (self.playerY > WINDOW_HEIGHT) and (self.levelState == GOBLIN_UPPER):
            self.oPlayer.panCam('Down')
            self.oGoblinMgr.panCam('Down', self.levelState)
            self.oVillagersMgr.panCam('Down', self.levelState)
            self.playBackground = pygwidgets.Image(self.window, (0, 0), IMAGE_LEVEL_1)
            self.glow = pygwidgets.Image(self.window, (0, 0), GLOW_LEVEL_1)
            self.levelState = GOBLIN_LOWER
        elif (self.playerY > WINDOW_HEIGHT) and (self.levelState == CITY_LOWER):
            self.oPlayer.panCam('Down')
            self.oGoblinMgr.panCam('Down', self.levelState)
            self.oVillagersMgr.panCam('Down', self.levelState)
            self.playBackground = pygwidgets.Image(self.window, (0, 0), IMAGE_LEVEL_2)
            self.glow = pygwidgets.Image(self.window, (0, 0), GLOW_LEVEL_2)
            self.levelState = GOBLIN_UPPER
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(AMBIENCE_GOBLIN), -1)
            pygame.mixer.music.play()


        elif (self.playerY > WINDOW_HEIGHT) and (self.levelState == CITY_UPPER):
            self.oPlayer.panCam('Down')
            self.oGoblinMgr.panCam('Down', self.levelState)
            self.oVillagersMgr.panCam('Down', self.levelState)
            self.playBackground = pygwidgets.Image(self.window, (0, 0), IMAGE_LEVEL_3)
            self.glow = pygwidgets.Image(self.window, (0, 0), GLOW_LEVEL_3)
            self.levelState = CITY_LOWER
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(MUSIC_TRANSITION), -1)

        elif (self.playerY > WINDOW_HEIGHT) and (self.levelState == LEVEL_END):
            self.oPlayer.panCam('Down')
            self.oGoblinMgr.panCam('Down', self.levelState)
            self.oVillagersMgr.panCam('Down', self.levelState)
            self.playBackground = pygwidgets.Image(self.window, (0, 0), IMAGE_LEVEL_4)
            self.glow = pygwidgets.Image(self.window, (0, 0), GLOW_LEVEL_4)
            self.levelState = CITY_UPPER

    
    def draw(self):
        # Draw everything
        self.window.fill(BLACK)
        self.playBackground.draw()
        self.atmosphere.draw()
        self.glow.draw()
    
        # Tell the managers to draw all the baddies & goodies
        self.oVillagersMgr.draw()
        self.oGoblinMgr.draw()
    
        # Draw the player
        self.oPlayer.draw()

        if not self.playing:
            self.gameOverImage.draw()


    def leave(self):
        pygame.mixer.music.stop()
