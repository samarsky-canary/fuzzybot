import math

import pygame

from game_objects.bot import Bot
from game_objects.overlay import Overlay


class Game:

    def __init__(self, w, h, x, y):
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
        self.win = False

        # init bot
        self.bot = Bot(20, x, y)
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
        self.bot.goal = self.goal.rect

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

    def dist_to_obstacle(self):
        pup = self.bot.calc_distance(self.obstacles)
        obstInfo = min([x for xs in pup for x in xs], key=lambda r: r['distance'])

        self.bot.nearest_obstacle = obstInfo['distance']
        return self.bot.nearest_obstacle

    def update(self):
        # Calls `update` methods of all contained sprites.
        self.all_sprites.update()
        collided = False
        for obstacle in self.obstacles:
            collide = self.bot.rect.colliderect(obstacle.rect)
            color = "red" if collide else "black"
            if color == "red": collided = True
            obstacle.image.fill(color)

        self.bot.collided = collided
        collide = self.bot.rect.colliderect(self.goal.rect)
        color = "green" if collide else "gold"
        if color == 'green':
            self.win = True
            self.bot.stop = True
        self.goal.changeColor(color)


    def draw(self):
        self.screen.fill(self.background)
        # Get the angle between the two rectangles
        self.angle_between_bot_n_goal()
        self.dist_to_obstacle()

        self.overlay.draw(self.screen, self.dist_to_goal(), self.bot.angle, self.bot.nearest_obstacle, self.bot.angle_to_goal)
        pygame.draw.line(self.screen, (200, 200, 200), self.bot.rect.center, self.goal.rect.center, 4)
        self.all_sprites.draw(self.screen)  # Draw the contained sprites.
        pygame.display.flip()

    def angle_between_bot_n_goal(self):
        vector = pygame.Vector2(1, 0).rotate(-self.bot.angle)

        # Calculate the center points
        center_a = self.bot.rect.center
        center_b = self.goal.rect.center
        # Calculate differences in x and y coordinates
        delta_x = center_b[0] - center_a[0]
        delta_y = center_b[1] - center_a[1]

        # Calculate the angle in radians
        angle_rad = math.atan2(delta_y, delta_x)

        # Convert radians to degrees (optional)
        angle_deg = math.degrees(angle_rad)
        angle_between = angle_deg % 360
        vector2 = pygame.Vector2(0, 1).rotate(angle_deg)
        angle_to_goal = vector.angle_to(vector2)
        if (angle_to_goal < - 180):
            angle_to_goal = 360 + angle_to_goal
        elif (angle_to_goal > 180):
            angle_to_goal = 360 - angle_to_goal
        self.bot.angle_to_goal = angle_to_goal
        # print(f"Angle in radians: {self.bot.angle_to_goal:.1f}")

