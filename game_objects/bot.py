import pygame


class Bot(pygame.sprite.Sprite):

    def __init__(self, rad, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./sprites/tonk.png")
        self.org_image = self.image.copy()

        self.rect = self.image.get_rect(center=(x, y))
        self.rad = rad
        self.angle = 0
        self.direction = pygame.Vector2(1, 0)
        self.speed = speed
        self.pos = pygame.Vector2(self.rect.center)
        self.width, self.height = 0,0

    def set_borders(self, width, height):
        self.width = width
        self.height = height

    # bot can turn left and right
    def handle_events(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.angle += 3
        if pressed[pygame.K_RIGHT]:
            self.angle -= 3
        if abs(self.angle) == 360 : self.angle = 0

    # rotate image based on radian angle
        self.direction = pygame.Vector2(1, 0).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, velocity):
        direction = pygame.Vector2(0, velocity).rotate(-self.angle)
        pos = self.pos
        pos += direction
        x = round(self.pos[0])
        y = round(self.pos[1])

        border = False
        if x > self.width: x = self.width; border = True
        if x < 0: x = 0; border = True
        if y > self.height: y = self.height; border = True
        if y < 0: y = 0; border = True

        if border is True: self.pos = (x, y)
        else: self.pos = pos
        self.rect.center = round(self.pos[0]), round(self.pos[1])