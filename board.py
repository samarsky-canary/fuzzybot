import json
import sys
import random

import pygame

from game_objects.goal import Goal
from game_objects.obstacle import Obstacle
from game import Game

SCREEN_WIDTH = 1060
SCREEN_HEIGHT = 798
BORDER_WIDTH = 5

def load_obstacles(game: Game, json):
    obstacles = [
        Obstacle(0, 0, SCREEN_WIDTH, BORDER_WIDTH),
        Obstacle(SCREEN_WIDTH - BORDER_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
        Obstacle(0, 0, BORDER_WIDTH, SCREEN_HEIGHT),
        Obstacle(0, SCREEN_HEIGHT - BORDER_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT),
    ]
    for i in json['obstacles']:
        obs = Obstacle(i['x'], i['y'], i['w'], i['h'])
        obstacles.append(obs)

    game.load_obstacles(obstacles)
def load_goal(game: Game, data):
    x = data['goal']['x']
    y = data['goal']['y']
    game.load_goal(Goal(x, y))

def main():
    pygame.init()
    pygame.display.set_caption("Tonk goin home")
    clock = pygame.time.Clock()

    px = py = 0
    with open('config.json') as f:
        data = json.load(f)

    px = data['player']['x']
    py = data['player']['y']
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, px, py)
    load_obstacles(game, data)
    load_goal(game, data)

    while game.run:
        game.handle_events()
        game.update()
        game.draw()
        clock.tick(60)


if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()