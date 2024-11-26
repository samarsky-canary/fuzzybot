import pygame


class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 50, 50)
        self.pos = pygame.Vector2(self.rect.center)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill("gold")
