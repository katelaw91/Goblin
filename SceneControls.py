#
# This the Splash Scene
#

import pygame
from pygame.locals import *
import pygwidgets
import SceneManager
from Constants import *

class SceneControls(SceneManager.Scene):
    def __init__(self, window, sceneKey):
        # Save window and sceneKey in instance variables
        self.window = window
        self.sceneKey = sceneKey

        self.backgroundImage = pygwidgets.Image(self.window, (0, 0), BG_SPLASH)
        self.backButton = pygwidgets.TextButton(self.window, (WINDOW_WIDTH/2 - 50, SPLASH_WINDOW_HEIGHT/2 - 150), 'Back', \
                                                upColor=DUSTYPURPLE, downColor=DARKVIOLET, textColor=WHITE,fontName=FONT_NAME, enterToActivate=True)

        self.moveKeys = pygwidgets.DisplayText(self.window, (WINDOW_WIDTH/2 - 70, SPLASH_WINDOW_HEIGHT/2 - 50), 'Move: Arrow Keys', \
                                fontSize=16, fontName = FONT_NAME,textColor=CONTROL_FONT_COLOR, justified='left')

        self.jumpKeys = pygwidgets.DisplayText(self.window, (WINDOW_WIDTH/2 - 70, SPLASH_WINDOW_HEIGHT/2), 'Jump: Spacebar', \
                                fontSize=16, fontName = FONT_NAME,textColor=CONTROL_FONT_COLOR, justified='left')

        self.interactKeys = pygwidgets.DisplayText(self.window, (WINDOW_WIDTH/2 - 70, SPLASH_WINDOW_HEIGHT/2 + 50), 'Interact: Enter', \
                                fontSize=16, fontName = FONT_NAME,textColor=CONTROL_FONT_COLOR, justified='left')

        self.attackKeys = pygwidgets.DisplayText(self.window, (WINDOW_WIDTH/2 - 70, SPLASH_WINDOW_HEIGHT /2 + 100), 'Attack: Mouse Left', \
                                                 fontName=FONT_NAME,fontSize=16, textColor=CONTROL_FONT_COLOR, justified='left')

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.backButton.handleEvent(event):
                self.goToScene(SCENE_SPLASH)

    def draw(self):

        pygame.display.flip()
        self.backgroundImage.draw()
        self.backButton.draw()
        self.moveKeys.draw()
        self.jumpKeys.draw()
        self.interactKeys.draw()
        self.attackKeys.draw()

    def leave(self):
        self.window.fill(BGCOLOR)
        pygame.display.flip()
