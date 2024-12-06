import pygame
from pygame import Vector2

from rules import bot_speed


def distance_from_vector_to_rectangle(vector: Vector2, rect):
    """
    Calculate the distance from a vector to the nearest edge of a rectangle.

    Parameters:
    vector (tuple): A tuple representing the (x, y) coordinates of the vector.
    rect (pygame.Rect): A pygame Rect object representing the rectangle.

    Returns:
    float: The distance to the nearest edge of the rectangle.
    """
    dist = vector.distance_to((rect.centerx, rect.centery))
    # Extract the vector coordinates
    vx, vy = vector

    # Rectangle edges
    rect_left = rect.left
    rect_right = rect.right
    rect_top = rect.top
    rect_bottom = rect.bottom

    # Calculate distances to the rectangle edges
    if vx < rect_left:
        dx = rect_left - vx  # Left edge
    elif vx > rect_right:
        dx = vx - rect_right  # Right edge
    else:
        dx = 0  # Inside the edges

    if vy < rect_top:
        dy = rect_top - vy  # Top edge
    elif vy > rect_bottom:
        dy = vy - rect_bottom  # Bottom edge
    else:
        dy = 0  # Inside the edges

    # Calculate the distance
    if dx == 0 and dy == 0:
        return 0  # Vector is inside the rectangle

    return (dx ** 2 + dy ** 2) ** 0.5  # Euclidean distance


class Bot(pygame.sprite.Sprite):

    def __init__(self, rad, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.image.load("./sprites/tonk.png")
        self.image = pygame.Surface((rad * 2, rad * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (55, 55, 55, 100), (rad, rad), rad)
        pygame.draw.line(self.image, (0, 0, 0), (rad, rad), (rad,0), 2)
        self.org_image = self.image.copy()

        self.rect = self.image.get_rect(center=(x, y))
        self.rad = rad
        self.direction = pygame.Vector2(1, 0)
        self.speed = self.angle = self.sensor = self.angle_to_goal = 0
        self.pos = pygame.Vector2(self.rect.center)
        self.width, self.height = 0,0

    def set_borders(self, width, height):
        self.width = width
        self.height = height

    def calc_distance(self, obstacles):
        dists = []
        direction = pygame.Vector2(1, 0).rotate(-self.angle)
        for obstacle in obstacles:
            dist = distance_from_vector_to_rectangle(direction, obstacle.rect)
            if dist > 0: dists.append(dist)
        return min(dists)

    # bot can turn left and right
    def handle_events(self):
        try:
            speed, turn = bot_speed(100, self.angle_to_goal)
            angle = turn
            self.speed = speed
            self.move(-self.speed)
            self.angle += angle
            print(self.angle_to_goal)
        except:
            print("ERROR")
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.angle += 3
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            self.move(-self.speed)
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.move(self.speed)
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.angle += -3

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