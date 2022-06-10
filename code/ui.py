import pygame

class UI:
    def __init__(self, surface):

        #Setup
        self.display_surface = surface

        #Health
        self.health_bar = pygame.image.load('../graphics/ui/health_bar.png').convert_alpha()
        self.health_bar_topleft = (12, 10)
        self.bar_max_width = 60
        self.bar_height = 4

        #Coins
        self.coin = pygame.image.load('../graphics/ui/coin.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft = (50, 30))
        self.font = pygame.font.Font('../graphics/ui/MinimalPixel v2.ttf', 15)


    def show_health(self, current, full):
        self.display_surface.blit(self.health_bar,(10, 7))
        current_health_ratio = current / full
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect(self.health_bar_topleft, (current_bar_width, self.bar_height))
        pygame.draw.rect(self.display_surface, 'red', health_bar_rect)

    def show_coins(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surf = self.font.render(str(amount), False, 'white')
        coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf, coin_amount_rect)

