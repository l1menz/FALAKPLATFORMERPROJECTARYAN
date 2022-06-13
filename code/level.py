import pygame # Imports Pygame

from decoration import Sky # Imports class Sky
from enemy import Enemy # Imports class Enemy
from game_data import levels # Imports levels dictionary
from player import Player # Import class Player
from settings import tile_size, screen_width, screen_height # Import settings
from support import import_csv_layout, import_cut_graphics # Import functions from support
from tiles import Tile, StaticTile # Imports classes from tiles


class Level:  # Class that contains all level information
    def __init__(self, current_level, surface, create_overworld, change_coins, change_health): # Class arguments
        # Level base
        self.background = pygame.image.load('../graphics/terrain/background_0.png')
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        #Audio
        self.coin_sound = pygame.mixer.Sound('../audio/effects/coin.wav')
        self.coin_sound.set_volume(0.2)
        self.stomp_sound = pygame.mixer.Sound('../audio/effects/stomp.wav')

        # Defines overworld arguments
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']

        # Player Setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)

        # Terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        #User interface
        self.change_coins = change_coins

        # Coin Setup
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

        # Enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # Constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')

        # Decoration
        self.sky = Sky(9)

        #Time
        current_time = pygame.time.get_ticks()

    def create_tile_group(self, layout, type): # Creates the tile logic in game
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1': # If csv number is -1
                    x = col_index * tile_size
                    y = row_index * tile_size # Creates blank space

                    if type == 'terrain': # If CSV data is type 'terrain'
                        terrain_tile_list = import_cut_graphics('../graphics/terrain/terrain.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface) # Create tile groupset

                    if type == 'coins': # If CSV data type is 'coins'
                        coin_tile_list = import_cut_graphics('../graphics/coins/diamond_1.png')
                        coin_surface = coin_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, coin_surface) # Create coin tile groupset

                    if type == 'enemies': # If CSV data type is 'enemies'
                        sprite = Enemy(tile_size, x, y) # Render sprite and borrow arguments from Class Enemy

                    if type == 'constraints': # If CSV data type is ;constraints'
                        sprite = Tile(tile_size, x, y) # Same logic as enemy

                    sprite_group.add(sprite) # Adds sprites

        return sprite_group # Evaluates sprite group


    def player_setup(self, layout, change_health):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface, change_health)
                    self.player.add(sprite)

                if val == '1':
                    start_surface = pygame.image.load('../graphics/character/character_start_tile.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, start_surface)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites

        for sprite in collidable_sprites():
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right


    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites

        for sprite in collidable_sprites():
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

            if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
                player.on_ground = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 4
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -4
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 4

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level, 0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)
        if collided_coins:
            self.coin_sound.play()
            for coin in collided_coins:
                self.change_coins(1)

    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.stomp_sound.play()
                    self.player.sprite.direction.y = -7
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def timer(self):
        font = pygame.font.Font('../graphics/ui/MinimalPixel v2.ttf', 50)
        current_time = pygame.time.get_ticks()
        time_surf = font.render(current_time, False, (64, 64, 64))
        time_rect = time_surf.get_rect(center=(600, 1000))



    def run(self):  # Runs the level

        # decoration
        self.sky.draw(self.display_surface)

        # Terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # Coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # Enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        # Player Sprites
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()

        self.check_death()
        self.check_win()

        self.check_coin_collisions()
        self.check_enemy_collisions()

        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
