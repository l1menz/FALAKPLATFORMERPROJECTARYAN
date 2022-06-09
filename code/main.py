import pygame, sys  # Import pygame
from settings import *
from level import Level  # Importing from level file
from overworld import Overworld
from ui import UI

class Game:
    def __init__(self):

        # Game Atrributes
        self.max_level = 0
        self.max_health = 10
        self.current_health = 10
        self.coins = 0

        #Overworld
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'

        #Ui
        self.ui = UI(screen)



    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level,self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def change_coins(self, amount):
        self.coins += amount

    def change_health(self, amount):
        self.current_health += amount

    def check_game_over(self):
        if self.current_health <= 0:
            self.current_health = 10
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.current_health,self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()


pygame.init()  # Initialises pygame
screen_width = 1280 # Width of player screen
screen_height = 720 # Height of player screen
screen = pygame.display.set_mode((screen_width, screen_height))  # Game screen
clock = pygame.time.Clock()  # Sets frame limit
game = Game()

while True:  # While game is running
    for event in pygame.event.get(): # When pygame is running
        if event.type == pygame.QUIT:  # When user quits
            pygame.quit()
            sys.exit() # Quit game

    screen.fill('grey') # Fills screen black
    game.run()  # Runs level

    pygame.display.update()  # Runs what the code displays per frame
    clock.tick(60)  # Frame the game runs at
