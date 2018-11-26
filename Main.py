#  Goblin Main program
#
# Instantiates 3 scenes, creates and starts the Scene Manager

# 1 - Import packages
import pygame
import os
from pygame.locals import *
from Constants import *
from SceneSplash import *
from ScenePlay import *
from SceneGameOver import *
from SceneControls import *


# 2 - Define constants
FRAMES_PER_SECOND = 60

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
splashWindow = pygame.display.set_mode((SPLASH_WINDOW_WIDTH, SPLASH_WINDOW_HEIGHT))

# The next line is here just in case you are running from the command line
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 4 - Load assets: image(s), sounds,  etc.
# Create instances of all scenes.  Specify the window and
# a unique scene key (string) for each scene (stored in Constants.py)
oSplashScene = SceneSplash(splashWindow, SCENE_SPLASH)
oGameOverScene = SceneGameOver(window, SCENE_GAME_OVER)
oPlayScene = ScenePlay(window, SCENE_PLAY)
oControlsScene = SceneControls(window, SCENE_CONTROLS)

# 5 - Initialize variables
# Build a dictionary of all scenes
scenesDict = {SCENE_SPLASH:oSplashScene, SCENE_PLAY:oPlayScene, SCENE_GAME_OVER:oGameOverScene, SCENE_CONTROLS:oControlsScene}
# Create the Scene Manager, passing in the scenes dictionary, the starting scene, and the FPS
oSceneMgr = SceneManager.SceneMgr(scenesDict, SCENE_SPLASH, FRAMES_PER_SECOND)

# Tell the scene manager to start running
oSceneMgr.run()
