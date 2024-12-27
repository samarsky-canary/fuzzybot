import pygame


class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 30,30)
        self.pos = pygame.Vector2(self.rect.center)
        # self.image = pygame.Surface((self.rect.width, self.rect.height))
        # self.image.fill("gold")

        self.color = pygame.Color('gold')

        self.image = pygame.Surface((30 * 2, 30 * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, self.image.get_rect().center, 30)
        # pygame.draw.line(self.image, (0, 0, 0), (5, 5), (5,0), 2)

    def changeColor(self, color):
        self.color = color
        pygame.draw.circle(self.image, self.color, (30, 30), 30)
