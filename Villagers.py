### VILLAGER
import pygame
import random
from Constants import *

class Villager():
    MIN_SIZE = 10
    MAX_SIZE = 41  # max plus one
    MIN_SPEED = 1
    MAX_SPEED = 9  # max plus one
    IMAGE = pygame.image.load('images/villager.png')

    def __init__(self, window):
        self.window = window

        size = random.randrange(Villager.MIN_SIZE, Villager.MAX_SIZE)
        self.rect = pygame.Rect(random.randrange(0, WINDOW_WIDTH - size),
                            (0 - size), size, size)  # start above the window
        self.speed = random.randrange(Villager.MIN_SPEED, Villager.MAX_SPEED)
        # Set the size of the villager
        self.image = pygame.transform.scale(Villager.IMAGE, (size, size))

    def update(self):   # Move the villager down
        self.rect.top = self.rect.top + self.speed
        if self.rect.top > GAME_HEIGHT:
            return True  # needs to be deleted
        else:
            return False  # stays on window

    def draw(self):
        self.window.blit(self.image, self.rect)

    def collidesWith(self, playerRect):
        if self.rect.colliderect(playerRect):
            return True
        else:
            return False


# VILLAGERMGR
class VillagerMgr():
    ADD_NEW_VILLAGER_RATE = 30  # add a new villager every 8 frames

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self):  # Called when starting a new game
        self.villagersList = []
        self.frameCounter = 0  # add a new villager every ADD_NEW_VILLAGER_RATE frames

    def update(self):
        # If the correct amount of frames have passed,
        # add a new villager
        self.frameCounter = self.frameCounter + 1
        if self.frameCounter == VillagerMgr.ADD_NEW_VILLAGER_RATE:
            # Time to add a new villager (and reset the counter)
            oVillager = Villager(self.window)
            self.villagersList.append(oVillager)
            self.frameCounter = 0

        # Tell each villager to update itself
        # Count how many villagers have fallen off the bottom.
        # Return that count (so score can increase for each one that falls off).
        nVillagersRemoved = 0
        for villager in reversed(self.villagersList):
            deleteMe = villager.update()
            if deleteMe:
                self.villagersList.remove(villager)
                nVillagersRemoved = nVillagersRemoved + 1

        return nVillagersRemoved         


    def draw(self):
        for villager in self.villagersList:
            villager.draw()

    def hasPlayerHitVillager(self, playerRect):
        for villager in self.villagersList:
            if villager.collidesWith(playerRect):
                return True

        return False
