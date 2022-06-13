import pygame, sys, time   # Import pygame
import timer
import datetime
from settings import *
from level import Level  # Importing from level file
from overworld import Overworld
from ui import UI

class Game: # Game Class with all parameters
    def __init__(self): # Reference to class

        # Game Atrributes
        self.max_level = 0 # Sets Max Level to 0
        self.max_health = 10 # Sets max health to 10
        self.current_health = 10 # Defines current health
        self.coins = 0 # Sets coins to 0

        #Audio
        self.level_bg_music = pygame.mixer.Sound('../audio/war-is-coming-103662.mp3') # Plays bg music
        self.level_bg_music.set_volume(0.2) # Sets volume
        self.overworld_bg_music = pygame.mixer.Sound('../audio/kingdom-of-fantasy-version-60s-10817.mp3') # Plays level selection bg music
        self.overworld_bg_music.set_volume(0.2) # Sets volume

        #Overworld
        self.overworld = Overworld(0, self.max_level, screen, self.create_level) # Defines overworld with set arguments
        self.status = 'overworld' # Sets status to overworld
        self.overworld_bg_music.play(loops = -1 ) # Loops music

        #Ui
        self.ui = UI(screen) # sets UI with UI class parameters


    def create_level(self, current_level): # Function used to create the level
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health) # Defines level with arguments from Level Class
        self.status = 'level' # Sets status to level
        self.overworld_bg_music.stop() # Stops playing overworld music
        self.level_bg_music.play(loops = -1) # Starts playing level music


    def create_overworld(self, current_level, new_max_level): # Function to create overworld
        if new_max_level > self.max_level: # If in overworld the player beats a level
            self.max_level = new_max_level # The current max level becomes the new max level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level) # Defines overworld with Overworld class arguments
        self.status = 'overworld' # Sets status to overworld
        self.overworld_bg_music.play(loops = -1) # Loops music and plays bg music
        self.level_bg_music.stop() # Level music stops

    def change_coins(self, amount): # Function to change coin amount
        self.coins += amount # Takes argument amount and increases subject to amount

    def change_health(self, amount): # Function to change health
        self.current_health += amount # Takes arugment amount and is subject to change depending on variable amount

    def check_game_over(self): # Functions checks if game is over
        if self.current_health <= 0: # If player health is less than or equal to 0
            self.current_health = 10 # Resets Health
            self.coins = 0 # Resets coins
            self.max_level = 0 # Levels back to 1
            self.overworld = Overworld(0, self.max_level, screen, self.create_level) # Sets overworld class with default arguments
            self.status = 'overworld' # Status changes to overworld
            self.level_bg_music.stop() # Level music stops
            self.overworld_bg_music.play(loops = -1) # Overworld music starts


    def run(self): # Displays all elements
        if self.status == 'overworld': # If status set is overworld
            self.overworld.run() # Overworld intitiates
        else: # If it's not level selection/overworld
            self.level.run() # The level runs
            self.ui.show_health(self.current_health, self.max_health) # UI displays the health
            self.ui.show_coins(self.coins) # UI displays the coins amount
            self.check_game_over() # Constantly checking if player has below 0 health


pygame.init()  # Initialises pygame
pygame.font.init() # Initialises font
screen_width = 1280 # Width of player screen
screen_height = 720 # Height of player screen
screen = pygame.display.set_mode((screen_width, screen_height))  # Game screen
clock = pygame.time.Clock()  # Sets frame limit
game = Game()
font = pygame.font.Font('../graphics/ui/MinimalPixel v2.ttf', 20) # Calls font
FPS = 60 # Frames per second
timer = 0 # Defines timer
while True:  # While game is running
    for event in pygame.event.get(): # When pygame is running
        if event.type == pygame.QUIT:  # When user quits
            pygame.quit()
            sys.exit() # Quit game

    screen.fill('grey') # Fills screen grey

    game.run() # Runs game

    clock.tick(FPS) #
    timer += 1 / FPS # Defines and adds time
    elapsed_time = datetime.timedelta(seconds=round(timer)) # Elapsed time counts per frame
    timer_text = font.render("Time: " + str(elapsed_time), False, (255, 255, 255)) # Defines and renders font
    screen.blit(timer_text, (100, 100)) # Displays the time in corner of screen

    story_text = font.render("There was once a time of peace for the Falaks. It was taken away by monsters. "
    "Exterminate them all!" , False, (255, 255, 255)) # Renders font
    screen.blit(story_text, (150, 30)) # Places story text on top of game

    pygame.display.update()  # Runs what the code displays per frame
