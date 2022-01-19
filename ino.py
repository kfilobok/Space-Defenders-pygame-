import pygame

class Ino(pygame.sprite.Sprite):
    """класс одного пришельца"""

    def __init__(self, screen,image0):
        """инициализируем и задаем начальную позицию"""
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load(image0)
        self.rect = self.image.get_rect()
        self.x = float(self.rect.width)
        self.y = float(self.rect.height)

    def draw(self):
        """вывод пришельца на экран"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """перемещение пришельцев"""
        self.y += 0.1
        self.rect.y = self.y