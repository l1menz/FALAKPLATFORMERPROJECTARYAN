import pygame, sys  # Import pygame
from settings import * # Importing from settings file
from level import Level  # Importing from level file
from game_data import level_0
from tiles import Tile

pygame.init()  # Initialises pygame
width = 1280 # Width of player screen
height = 720 # Height of player screen
screen = pygame.display.set_mode((width, height))  # Game screen
clock = pygame.time.Clock()  # Sets frame limit
level = Level(level_0, screen) # Loads level 0, functions passes a different function everytime i.e level_0, level_1 etc

while True:  # While game is running
    for event in pygame.event.get(): # When pygame is running
        if event.type == pygame.QUIT:  # When user quits
            pygame.quit()
            sys.exit() # Quit game

    screen.fill('black') # Fills screen black
    level.run # Runs level

    pygame.display.update()  # Runs what the code displays per frame
    clock.tick(60)  # Frame the game runs at
