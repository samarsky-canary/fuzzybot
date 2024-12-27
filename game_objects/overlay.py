import math

import pygame

BORDER_WIDTH = 5


class Overlay:
    def __init__(self):
        self.font = pygame.font.SysFont("Comic Sans MS", 15)
        self.dist = self.angle = self.obsDist = self.angle_goal = None

    def draw(self, screen, dist, angle, dist_to_obst, angle_to_goal):
        self.dist = self.font.render("Distance To Goal: {}".format(dist), True, (0, 0, 0))
        self.angle = self.font.render("Bot Angle (rad): {}".format(f"{self.angled(angle):.0f}"), True, (0, 0, 0))
        self.obsDist = self.font.render("Obst Dist (rad): {}".format(f"{dist_to_obst:.1f}"), True, (0, 0, 0))
        self.angle_goal = self.font.render("Angle to Goal (rad): {}".format(f"{angle_to_goal:.1f}"), True, (0, 0, 0))
        screen.blit(self.dist, (BORDER_WIDTH + 0, BORDER_WIDTH + 0))
        screen.blit(self.angle, (BORDER_WIDTH + 0, BORDER_WIDTH + 25))
        screen.blit(self.obsDist, (BORDER_WIDTH + 0, BORDER_WIDTH + 50))
        screen.blit(self.angle_goal, (BORDER_WIDTH + 0, BORDER_WIDTH + 75))

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