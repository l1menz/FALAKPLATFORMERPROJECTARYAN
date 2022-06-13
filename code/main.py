import pygame, sys, time   # Import pygame
import timer
import datetime
from settings import *
from level import Level  # Importing from level file
from overworld import Overworld
from ui import UI

class Game:
    def __init__(self):

        # Game Atrributes
        self.max_level = 3
        self.max_health = 10
        self.current_health = 10
        self.coins = 0

        #Audio
        self.level_bg_music = pygame.mixer.Sound('../audio/war-is-coming-103662.mp3')
        self.level_bg_music.set_volume(0.2)
        self.overworld_bg_music = pygame.mixer.Sound('../audio/kingdom-of-fantasy-version-60s-10817.mp3')
        self.overworld_bg_music.set_volume(0.2)

        #Overworld
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops = -1 )

        #Ui
        self.ui = UI(screen)


    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops = -1)


    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops = -1)
        self.level_bg_music.stop()

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
            self.level_bg_music.stop()
            self.overworld_bg_music.play(loops = -1)


    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()


pygame.init()  # Initialises pygame
pygame.font.init()
screen_width = 1280 # Width of player screen
screen_height = 720 # Height of player screen
screen = pygame.display.set_mode((screen_width, screen_height))  # Game screen
clock = pygame.time.Clock()  # Sets frame limit
game = Game()
font = pygame.font.Font('../graphics/ui/MinimalPixel v2.ttf', 20)
FPS = 60
timer = 0
while True:  # While game is running
    for event in pygame.event.get(): # When pygame is running
        if event.type == pygame.QUIT:  # When user quits
            pygame.quit()
            sys.exit() # Quit game

    screen.fill('grey') # Fills screen black

    game.run()

    clock.tick(FPS)
    timer += 1 / FPS
    elapsed_time = datetime.timedelta(seconds=round(timer))
    timer_text = font.render("Time: " + str(elapsed_time), False, (255, 255, 255))
    screen.blit(timer_text, (100, 100))

   # story_text = font.render("There was once a time of peace for the Falaks. It was taken away by monsters. "
                             #"Exterminate them all!" , False, (255, 255, 255))
    #screen.blit(story_text, (200, 200))





    pygame.display.update()  # Runs what the code displays per frame
