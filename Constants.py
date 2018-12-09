#CONSTANTS
# GAME OPTIONS/SETTINGS
import pygame

#GAME
TITLE = "Goblin"
WINDOW_WIDTH = 540
WINDOW_HEIGHT = 600
OFFSET = -400
#640
SPLASH_WINDOW_WIDTH = 540
SPLASH_WINDOW_HEIGHT = 540
GAME_HEIGHT = 500
DIALOG_BOX_OFFSET = 35
DIALOG_BOX_WIDTH = WINDOW_WIDTH - (2 * DIALOG_BOX_OFFSET)
FPS = 60
VEC = pygame.math.Vector2
FONT_NAME = 'Courier New'

GAME_OVER_DATA = 'game over data'

#SCENE KEYS
SCENE_SPLASH = 'scene splash'
SCENE_PLAY = 'scene play'
SCENE_GAME_OVER = 'scene game over'
SCENE_CONTROLS = 'scene controls'

#LOAD
LOGO = 'images/logo_goblin.png'
BG_SPLASH = 'images/background_splash.png'
SPRITESHEET = 'images/spritesheet.png'
SPRITESHEET_PLAYER = 'images/spritesheet_player.png'
SPRITESHEET_GOBLINS = 'images/spritesheet_goblins.png'
IMAGE_LEVEL_1 = 'images/Level1Map.png'
ATMOSPHERE = 'images/atmos_overlay.png'
GLOW = 'images/glow_overlay.png'
IMAGE_COLLISION_MAP = 'images/ColMap.png'
MUSIC_SPLASH = 'sounds/ForgottenVictory.ogg'
MUSIC_GOBLINS = 'sounds/PPM-Emotional-Introspection.mp3'
MUSIC_VILLAGERS = 'sounds/Town-Square.mp3'
MUSIC_HERO = 'sounds/Young-Heroes.mp3'

#PLATER PHYSICS
PLAYER_ACC = 0.3
PLAYER_FRICTION = -0.13
PLAYER_GRAVITY = 0.45
PLAYER_JUMP = 8.5

#PLAYER STATES
IDLING ='idling'
WALKING_LEFT = 'walkleft'
WALKING_RIGHT = 'walkright'
JUMPING = 'jumping'
DYING = 'dying'
FALLING = 'falling'
LEFT = 'left'
RIGHT = 'right'


#COLORS
CONTROL_FONT_COLOR = (255, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0,0, 255)
YELLOW = (255, 255, 0)
TEAL = (0, 255, 200)
PURPLE = (130, 0, 255)
LIGHTBLUE = (153,204,255)
LIGHTPURPLE = (204,204,255)
DARKPURPLE = (25,0,51)
DARKVIOLET = (51,0,51)
DARKGREEN = (47,79,79)
DUSTYPURPLE = (72,61,139)
BGCOLOR = (93,71,139)
HIT = (0, 0, 0, 255)
