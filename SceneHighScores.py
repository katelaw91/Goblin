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

def showCustomAnswerDialog(theWindow, theText):
    oDialogBackground = pygwidgets.Image(theWindow, (35, 450), 'images/dialog.png')
    oPromptDisplayText = pygwidgets.DisplayText(theWindow, (0, 480), theText, \
                                width=WINDOW_WIDTH, justified='center', fontSize=36)
    oUserInputText = pygwidgets.InputText(theWindow, (200, 550), '',
                                            fontSize=36, initialFocus=True)
    oNoButton = pygwidgets.CustomButton(theWindow, (65, 595), \
                                        'images/noThanksNormal.png',\
                                        over='images/noThanksOver.png',\
                                        down='images/noThanksDown.png',\
                                        disabled='images/noThanksDisabled.png')
    oYesButton = pygwidgets.CustomButton(theWindow, (330, 595), \
                                        'images/addNormal.png',\
                                        over='images/addOver.png',\
                                        down='images/addDown.png',\
                                        disabled='images/addDisabled.png')
    choiceAsBoolean, userAnswer = SceneManager.customAnswerDialog(theWindow, oDialogBackground, \
                                    oPromptDisplayText, oUserInputText, oYesButton, oNoButton)
    return choiceAsBoolean, userAnswer

class SceneGameOver(SceneManager.Scene):
    DATA_FILE_PATH = 'GameOver.txt'
    
    def __init__(self, window, sceneKey):
        # Save window and sceneKey in instance variables
        self.window = window
        self.sceneKey = sceneKey

        self.backgroundImage = pygwidgets.Image(self.window, (0, 0), "images/GameOverBackground.jpg")

        # The following will create a list of lists
        # Either by building a blank one from scratch, or by reading from a text file
        # The result will look like:
        # [[name, score], [name, score], [name, score] ...]
        # and will always be kept in order of the score (highest to lowest)
        if not SceneManager.fileExists(SceneGameOver.DATA_FILE_PATH):
            self.setEmptyGameOver()
        else:
            data = SceneManager.readFile(SceneGameOver.DATA_FILE_PATH)
            # read in all the data in json format, converts to a list of lists
            self.scoresList = json.loads(data)

        self.scoresField = pygwidgets.DisplayText(self.window, (25, 84), '', \
                                fontSize=48, textColor=BLACK, width=175, justified='right')
        self.namesField = pygwidgets.DisplayText(self.window, (260, 84), '', \
                                fontSize=48, textColor=BLACK, width=300, justified='left')

        self.quitButton = pygwidgets.TextButton(self.window, (30, 650), 'Quit')
        self.resetScoresButton = pygwidgets.TextButton(self.window, (240, 650), 'Reset high scores')
        self.startNewGameButton = pygwidgets.TextButton(self.window, (450, 650), 'Start new game')

        self.showGameOver()


    def setEmptyGameOver(self):
        self.scoresList = [
            ['-----', 0],
            ['-----', 0],
            ['-----', 0],
            ['-----', 0],
            ['-----', 0],
            ['-----', 0],
            ['-----', 0],
            ['-----', 0],
            ['-----', 0],
            ['-----', 0]]

        SceneManager.writeFile(SceneGameOver.DATA_FILE_PATH, json.dumps(self.scoresList))
        self.showGameOver()

    def enter(self, data):
        # This can be called two different ways:
        # 1. If there is no new high score, data will be None
        # 2. Otherwise, data will be the score of the current game
        if data is not None:
            self.draw()
            # We have a new high score sent in from the play scene
            newHighScoreValue = data  # this is the score

                # Show the new high scores table
                self.showGameOver()
                # Write out updated file of high scores
                SceneManager.writeFile(SceneGameOver.DATA_FILE_PATH, json.dumps(self.scoresList))


    def showGameOver(self):
        # Build up strings and show them in text display fields
        scoresText = ''
        namesText = ''
        for nameScoreList in self.scoresList:
            # Each element is a list of [name, score]
            namesText = namesText + nameScoreList[0] + '\n'
            scoresText = scoresText + str(nameScoreList[1]) + '\n'

        self.scoresField.setValue(scoresText)
        self.namesField.setValue(namesText)

    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:
            if self.startNewGameButton.handleEvent(event):
                self.goToScene(SCENE_PLAY)

            elif self.quitButton.handleEvent(event):
                self.quit()

            elif self.resetScoresButton.handleEvent(event):
                confirmed = SceneManager.textYesNoDialog(self.window, (35, 450, DIALOG_BOX_WIDTH, 150), \
                                              "Are you sure you want to RESET the high scores?")
                if confirmed:
                    self.setEmptyGameOver()


    def draw(self):
        self.backgroundImage.draw()
        self.scoresField.draw()
        self.namesField.draw()
        self.quitButton.draw()
        self.resetScoresButton.draw()
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
