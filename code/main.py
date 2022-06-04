import sys
import pygame
from game_data import level_0
from level import Level
from settings import*

# Pygame Setup
pygame.init() # Initialises pygame
screen = pygame.display.set_mode((screen_width, screen_height)) # Sets screen dimensions
clock = pygame.time.Clock() # Frame rate measuremen
level = Level(level_0, screen) # level takes arguments level_0 and the screen

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # When the player quits
            pygame.quit() # Quit game
            sys.exit()

    screen.fill('black')
    level.run() # Run level variable which encompasses two arguments

    pygame.display.update() # Displays content of code
    clock.tick(60) # Frame rate
