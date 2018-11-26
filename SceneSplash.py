#
# This the Splash Scene
#

import pygame
from pygame.locals import *
import pygwidgets
import SceneManager
from Constants import *

class SceneSplash(SceneManager.Scene):
    def __init__(self, window, sceneKey):
        # Save window and sceneKey in instance variables
        self.window = window
        self.sceneKey = sceneKey

        pygame.mixer.music.load(MUSIC_SPLASH)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1)

        self.backgroundImage = pygwidgets.Image(self.window, (0, 0), BG_SPLASH)
        self.logo = pygwidgets.Image(self.window, (WINDOW_WIDTH/2 - 250, SPLASH_WINDOW_HEIGHT/2 - 200), LOGO)
        self.startButton = pygwidgets.TextButton(self.window, (WINDOW_WIDTH/2 -50, SPLASH_WINDOW_HEIGHT/2 - 50), 'Start', \
                                                 upColor=DUSTYPURPLE, downColor=DARKVIOLET, textColor=WHITE, fontName = FONT_NAME, enterToActivate=True)
        self.quitButton = pygwidgets.TextButton(self.window, (WINDOW_WIDTH/2 -50, SPLASH_WINDOW_HEIGHT/2 + 50), 'Quit', \
                                                upColor=DUSTYPURPLE, downColor=DARKVIOLET, textColor=WHITE, fontName = FONT_NAME, )
        self.controlsButton = pygwidgets.TextButton(self.window, (WINDOW_WIDTH/2 -50, SPLASH_WINDOW_HEIGHT/2), 'Controls', \
                                                    upColor=DUSTYPURPLE, downColor=DARKVIOLET, textColor=WHITE, fontName = FONT_NAME,)

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.startButton.handleEvent(event):
                self.goToScene(SCENE_PLAY)

            elif self.quitButton.handleEvent(event):
                self.quit()

            elif self.controlsButton.handleEvent(event):
                self.goToScene(SCENE_CONTROLS)

    def update(self):
        self.logo.scale(60, True)

    def draw(self):
        self.backgroundImage.draw()
        self.logo.draw()
        self.startButton.draw()
        self.quitButton.draw()
        self.controlsButton.draw()
        pygame.display.flip()


    def leave(self):
        self.window.fill(BGCOLOR)
        pygame.display.flip()

