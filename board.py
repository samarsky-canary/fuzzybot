import sys
import random

import pygame

from game_objects.goal import Goal
from game_objects.obstacle import Obstacle
from game import Game

SCREEN_WIDTH = 1060
SCREEN_HEIGHT = 798
BORDER_WIDTH = 5

def load_obstacles(game: Game):
    obstacles = [
        Obstacle(0, 0, SCREEN_WIDTH, BORDER_WIDTH),
        Obstacle(SCREEN_WIDTH - BORDER_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
        Obstacle(0, 0, BORDER_WIDTH, SCREEN_HEIGHT),
        Obstacle(0, SCREEN_HEIGHT - BORDER_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT),
        Obstacle(760, 0, 90, 200),
        Obstacle(200, 600, 330, 10),
    ]
    game.load_obstacles(obstacles)
def load_goal(game: Game):
    x = random.randrange(0, game.screen_width)
    y = random.randrange(0, game.screen_height)
    game.load_goal(Goal(x, y))

def main():
    pygame.init()
    pygame.display.set_caption("Tonk goin home")
    clock = pygame.time.Clock()

    x = random.randrange(0, SCREEN_WIDTH)
    y = random.randrange(0, SCREEN_HEIGHT)
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, x, y, 5)
    load_obstacles(game)
    load_goal(game)

    while game.run:
        game.handle_events()
        game.update()
        game.draw()
        clock.tick(60)


if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()