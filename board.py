import sys
import random

import pygame

from config import Bot, Game, Obstacle, Goal


def load_obstacles(game: Game):
    obstacles = [
        Obstacle(760, 0, 90, 200),
        Obstacle(200, 600, 330, 10),
    ]
    game.load_obstacles(obstacles)
def load_goal(game: Game):
    x = random.randrange(0, 1060)
    y = random.randrange(0, 798)
    game.load_goal(Goal(x, y))

def main():
    pygame.init()
    pygame.display.set_caption("Tonk goin home")
    clock = pygame.time.Clock()

    x = random.randrange(0, 1060)
    y = random.randrange(0, 798)
    game = Game(1060, 798, x, y)
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