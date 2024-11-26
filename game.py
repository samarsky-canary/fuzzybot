import math

import pygame

from game_objects.bot import Bot
from game_objects.overlay import Overlay


class Game:

    def __init__(self, w, h, x, y, speed):
        self.run = True
        self.screen_width = w
        self.screen_height = h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = (252, 255, 255)
        # all_sprites is used to update and draw all sprites together.
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.overlay = Overlay()

        # init bot
        self.bot = Bot(20, x, y, speed)
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



        try:
            # close the game if Escape or X cross clicked
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False
        except:
            print("Event handle errorf")

    def dist_to_goal(self):
        dist = math.hypot(self.bot.rect.center[0] - self.goal.rect.center[0], self.bot.rect.center[1] - self.goal.rect.center[1])
        return round(dist, 2)

    def update(self):
        # Calls `update` methods of all contained sprites.
        self.all_sprites.update()
        for obstacle in self.obstacles:
            collide = self.bot.rect.colliderect(obstacle.rect)
            color = "red" if collide else "black"
            obstacle.image.fill(color)

        collide = self.bot.rect.colliderect(self.goal.rect)
        color = "green" if collide else "gold"
        self.goal.image.fill(color)


    def draw(self):
        self.screen.fill(self.background)
        self.overlay.draw(self.screen, self.dist_to_goal(), self.bot.angle)
        self.all_sprites.draw(self.screen)  # Draw the contained sprites.
        pygame.display.flip()
