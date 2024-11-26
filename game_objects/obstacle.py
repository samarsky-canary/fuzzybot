import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, w, h)
        self.pos = pygame.Vector2(self.rect.center)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill("black")