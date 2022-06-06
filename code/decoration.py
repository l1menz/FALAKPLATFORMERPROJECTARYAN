import pygame
from settings import*

class Sky:
    def __init__(self, horizon):
        self.top = pygame.image.load('../graphics/decorations/sky_top.png')
        self.bottom = pygame.image.load('../graphics/decorations/sky_bottom.png')
        self.middle = pygame.image.load('../graphics/decorations/sky_middle.png')

        self.horizon = horizon

        # Strech
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size))
        self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size))

    def draw(self, surface):
        for row in range(vertical_tile_number):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top, (0,y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))

