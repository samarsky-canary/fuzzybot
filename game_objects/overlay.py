import math

import pygame

BORDER_WIDTH = 5


class Overlay:
    def __init__(self):
        self.dist_to_goal = self.angle = self.dist_to_obst = 0
        self.font = pygame.font.SysFont("Comic Sans MS", 15)
        self.dist = self.angle = self.obsDist = None

    def draw(self, screen, dist, angle, dist_to_obst):
        self.dist_to_goal = dist
        self.angle = angle
        self.dist_to_obst = dist_to_obst
        self.dist = self.font.render("Distance To Goal: {}".format(self.dist_to_goal), True, (0, 0, 0))
        self.angle = self.font.render("Bot Angle (rad): {}".format(f"{self.angled(self.angle):.0f}"), True, (0, 0, 0))
        self.obsDist = self.font.render("Obst Dist (rad): {}".format(self.dist_to_obst), True, (0, 0, 0))
        screen.blit(self.dist, (BORDER_WIDTH + 0, BORDER_WIDTH + 0))
        screen.blit(self.angle, (BORDER_WIDTH + 0, BORDER_WIDTH + 25))
        screen.blit(self.obsDist, (BORDER_WIDTH + 0, BORDER_WIDTH + 50))

    @staticmethod
    def angled(angle):
        vector = pygame.Vector2(1, 0).rotate(-angle)
        # Calculate the angle of the vector
        angle_vector = math.degrees(math.atan2(vector[1], vector[0]))

        # Assuming the rectangle is axis-aligned
        angle_rect = 0

        # Calculate the angle between the vector and the rectangle
        angle_between = angle_vector - angle_rect
        angle_between = angle_between % 360  # Normalize to [0, 360]
        return angle_between