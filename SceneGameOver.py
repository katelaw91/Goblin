#
# This the Game Over Scene
#

import pygame
import sys
from pygame.locals import *
import pygwidgets
import SceneManager
from Constants import *
import json  # Write and read the data file in JSON format

class SceneGameOver(SceneManager.Scene):
    DATA_FILE_PATH = 'GameOver.txt'
    
    def __init__(self, window, sceneKey):
        # Save window and sceneKey in instance variables
        self.window = window
        self.sceneKey = sceneKey

        # Set background
        self.backgroundImage = pygwidgets.Image(self.window, (0, 0), "images/GameOverBackground.jpg")

        # Read/load game data
        if not SceneManager.fileExists(SceneGameOver.DATA_FILE_PATH):
            pass
        else:
            data = SceneManager.readFile(SceneGameOver.DATA_FILE_PATH)
            # read in all the data in json format, converts to a list of lists
            self.scoresList = json.loads(data)


        self.deathCount = pygwidgets.DisplayText(self.window, (25, 84), 'Deaths: ', \
                                fontSize=48, textColor=DARKVIOLET, width=175, justified='right')
        # + str(nameScoreList[1]),\
        self.deathMessage = pygwidgets.DisplayText(self.window, (260, 84), 'YOU DIED', \
                                fontSize=48, textColor=DARKVIOLET, width=300, justified='left')

        self.quitButton = pygwidgets.TextButton(self.window, (30, 650), 'Quit')
        self.startNewGameButton = pygwidgets.TextButton(self.window, (450, 650), 'Try Again')


    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:
            if self.startNewGameButton.handleEvent(event):
                self.goToScene(SCENE_PLAY)

            elif self.quitButton.handleEvent(event):
                self.quit()



    def draw(self):
        self.backgroundImage.draw()
        self.deathCount.draw()
        self.deathMessage.draw()
        self.quitButton.draw()
        self.startNewGameButton.draw()


    def respond(self, infoRequested):
        if infoRequested == GAME_OVER_DATA:
            # This is a request to get a dictionary made up of
            # the highest score so far, and the lowest high score of all scores in the list
            highestOnList = self.scoresList[0]
            lowestOnList = self.scoresList[-1]
            highestScore = highestOnList[1]
            lowestScore = lowestOnList[1]

            return {'highest':highestScore, 'lowest':lowestScore}

    def leave(self):
        pygame.mixer.music.stop()
        self.window.fill(BGCOLOR)
        pygame.display.flip()