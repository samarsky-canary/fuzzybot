import pygame


class Overlay:
    def __init__(self):
        self.dist_to_goal = self.angle = 0
        self.font = pygame.font.SysFont("Comic Sans MS", 15)
        self.dist = self.angle = None

    def draw(self, screen, dist, angle):
        self.dist_to_goal = dist
        self.angle = angle
        self.dist = self.font.render("Distance To Goal: {}".format(self.dist_to_goal), True, (0, 0, 0))
        self.angle = self.font.render("Bot Angle (rad): {}".format(self.angle), True, (0, 0, 0))
        screen.blit(self.dist, (0, 0))
        screen.blit(self.angle, (0, 25))