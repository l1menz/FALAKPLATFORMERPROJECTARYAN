import pygame, sys  # Import pygame
from settings import *  # Importing from settings file
from level import Level  # Importing from level file

pygame.init()  # Initialises pygame
WIDTH = 1280
HEIGHT = 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))  # Game screen
clock = pygame.time.Clock()  # Sets frame limit
level = Level(level_map, SCREEN)  # Displays level

while True:  # While game is running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # When user quits
            pygame.quit()
            sys.exit()

    SCREEN.fill('black')
    level.run()

    pygame.display.update()  # Runs what the code displays per frame
    clock.tick(60)  # Frame the game runs at
