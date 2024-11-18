import math
import random

import pygame

class Game:

    def __init__(self, w, h, x, y):
        self.run = True
        self.screen_width = w
        self.screen_height = h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = (252, 249, 217)
        # all_sprites is used to update and draw all sprites together.
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()

        # init bot
        self.bot = Bot(5, x, y, 3)
        self.bot.set_borders(self.screen.get_width(), self.screen.get_height())
        self.all_sprites.add(self.bot)
        self.goal = None

    def load_obstacles(self, obstacles):
        self.all_sprites.add(obstacles)
        self.obstacles.add(obstacles)

    def load_goal(self, goal):
        self.all_sprites.add(goal)
        self.goals.add(goal)
        self.goal = goal

    def handle_events(self):
        keys = pygame.key.get_pressed()
        self.bot.handle_events()


        # bot moves forward and backward only
        if keys[pygame.K_UP]:
            self.bot.move(-5)
        if keys[pygame.K_DOWN]:
            self.bot.move(5)

        # close the game if Escape or X cross clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False

    def update(self):
        # Calls `update` methods of all contained sprites.
        self.all_sprites.update()
        for obstacle in self.obstacles:
            collide = self.bot.rect.colliderect(obstacle.rect)
            color = "red" if collide else "black"
            obstacle.image.fill(color)

        collide = self.bot.rect.colliderect(self.goal.rect)
        color = "white" if collide else "gold"
        self.goal.image.fill(color)


    def draw(self):
        self.screen.fill(self.background)
        self.all_sprites.draw(self.screen)  # Draw the contained sprites.
        pygame.display.update()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, w, h)
        self.pos = pygame.Vector2(self.rect.center)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill("black")

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 50, 50)
        self.pos = pygame.Vector2(self.rect.center)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill("gold")

class Bot(pygame.sprite.Sprite):

    def __init__(self, rad, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/tonk.png")
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