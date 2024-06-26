import pygame
from pygame.sprite import Sprite


class Gun(Sprite):

    def __init__(self, screen):
        """инициализация пушки"""
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load('images/gun.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom - 20
        self.mright = False
        self.mleft = False

    def output(self):
        """рисование пушки"""
        self.screen.blit(self.image, self.rect)



    def update_gun(self):
        """обновление позиции пушки"""
        if self.mright and self.rect.right < self.screen_rect.right:
            self.center += 1.05
        if self.mleft and self.rect.left > 0:
            self.center -= 1.05

        self.rect.centerx = self.center

    def create_gun(self):
        """размещение пушки по центру внизу экрана"""
        self.center = self.screen_rect.centerx
