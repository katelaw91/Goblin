#Spritesheet loading and parsing
import pygame
from Constants import *

class Spritesheet:
    def __init__(self,filename):
        self.spritesheet = pygame.image.load(filename).convert()

        def get_image(self,x,y,width,height):
            #grab an image out of a larger spritesheet
            image = pygame.Surface((width,height))
            image.blit(self.spritesheet, (0,0), (x,y,width,height))
            return image