import math
from copy import deepcopy

import numpy as np
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

    MAX_DISTANCE = 10000000

    def __init__(self, rad, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.image.load("./sprites/tonk.png")
        self.image = pygame.Surface((rad * 2, rad * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (55, 55, 55, 100), (rad, rad), rad)
        pygame.draw.line(self.image, (0, 0, 0), (rad, rad), (rad,0), 2)
        self.org_image = self.image.copy()
        self.stop = False

        self.rect = self.image.get_rect(center=(x, y))
        self.rad = rad
        self.direction = pygame.Vector2(1, 0)
        self.speed = self.angle = self.sensor = self.angle_to_goal = self.nearest_obstacle = 0
        self.pos = pygame.Vector2(self.rect.center)
        self.width, self.height = 0,0
        self.goal = None
        self.collided = False
        self.frame = 0

    def set_borders(self, width, height):
        self.width = width
        self.height = height

    def calc_distance(self, obstacles):
        if self.goal is None: return
        dists = [[]]
        halfSq = 20
        idx = 0
        angle = Vector2(1, 0).rotate(-self.angle).rotate(-90)
        leftBorder = self.direction + pygame.Vector2(-angle[1], angle[0])
        rightBorder = self.direction + pygame.Vector2(angle[1], -angle[0])
        pos = deepcopy(self.pos)
        pos.x += halfSq
        pos.y += halfSq
        dirLine = pos + angle * max(self.width, self.height)

        for obs in obstacles:
            obstacle = obs.rect
            dists.append([])

            for line in self._create_lines(
                    [obstacle.x + halfSq, obstacle.y + halfSq], obstacle.width,
                    obstacle.height):

                inter_point = self._line_intersection(pos, dirLine, line[0], line[1])
                if (inter_point is None or not self._point_in_line(inter_point, pos, dirLine) or not self._point_in_line(
                            inter_point, line[0], line[1])):
                    dists[idx].append({'border': None, 'distance': self.MAX_DISTANCE, 'angle': 90})
                else:
                    dist1 = self._dist(pos, line[0])
                    dist2 = self._dist(pos, line[1])

                    leftDist = self._dist(leftBorder, inter_point)
                    rightDist = self._dist(rightBorder, inter_point)
                    if leftDist < rightDist:
                        zn = -1
                    else:
                        zn = 1

                    if dist1 < dist2:
                        angle = self.angle_calc(self._vector_by_points(inter_point, pos),
                                           self._vector_by_points(inter_point, line[1]))
                    else:
                        angle = self.angle_calc(self._vector_by_points(inter_point, pos),
                                           self._vector_by_points(inter_point, line[0]))
                    dists[idx].append(
                        {'border': inter_point, 'distance': self._dist(pos, inter_point), 'angle': angle * zn})
            idx += 1
            #
            # dist = distance_from_vector_to_rectangle(direction, obstacle.rect)
            # if dist > 0: dists.append(dist)
        return dists


    def _point_in_line(self, point: tuple[int, int], lineA: tuple[int, int], lineB: tuple[int, int]):
        return ((self._dist(point, lineA) + self._dist(point, lineB)) - self._dist(lineA, lineB)) < 10

    def _dist(self, p1: tuple[int, int], p2: tuple[int, int]):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    def _vector_by_points(self, a: tuple[int, int], b: tuple[int, int]):
        return pygame.Vector2([b[0] - a[0], b[1] - a[1]])

    def dotproduct(self, v1, v2):
        return sum((a*b) for a, b in zip(v1, v2))

    def length(self, v):
        return math.sqrt(self.dotproduct(v, v))

    def angle_calc(self, v1, v2):
        cos = self.dotproduct(v2, v1) / (self.length(v2) * self.length(v1))
        angle = math.acos(cos)

        angleV = Vector2(1, 0).rotate(-self.angle)


        leftBorder = self.direction + pygame.Vector2(-angleV[1], angleV[0])
        rightBorder = self.direction + pygame.Vector2(angleV[1], -angleV[0])
        leftDist = self._dist(leftBorder, (self.goal.x, self.goal.y))
        rightDist = self._dist(rightBorder, (self.goal.x, self.goal.y))
        if leftDist < rightDist: zn = 1
        else: zn = -1

        return math.degrees(angle) * zn

    def _create_lines(self, leftTop, width, height):
        return [ ([leftTop[0], leftTop[1]], [leftTop[0] + width, leftTop[1]]),
            ([leftTop[0], leftTop[1]], [leftTop[0], leftTop[1] + height]),
            ([leftTop[0], leftTop[1] + height], [leftTop[0] + width, leftTop[1] + height]),
            ([leftTop[0] + width, leftTop[1]], [leftTop[0] + width, leftTop[1] + height]) ]

    def _line_intersection(self, A: tuple[int, int], B: tuple[int, int], C: tuple[int, int], D: tuple[int, int]):
        s = np.vstack([A,B,C,D])        # s for stacked
        h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
        l1 = np.cross(h[0], h[1])           # get first line
        l2 = np.cross(h[2], h[3])           # get second line
        x, y, z = np.cross(l1, l2)          # point of intersection
        if z == 0:                          # lines are parallel
            return None
        return (x/z, y/z)

    # bot can turn left and right
    def handle_events(self):
        if self.stop: return
        self.frame += 1
        try:
            speed, turn = bot_speed(self.nearest_obstacle, self.angle_to_goal)
            angle = turn
            self.speed = speed
            if self.nearest_obstacle < 20 and self.collided == False:
                self.move(7)
                self.angle += 30
            elif self.nearest_obstacle < 20 and self.collided == True and self.frame > 15:
                self.angle += 30
                self.move(-5)

            if (self.frame > 15): self.frame = 0
            self.move(-self.speed)
            self.angle += angle

        except:
            print("exception")
            self.angle += 30
            self.move(1)
        self.debugger()

        # rotate image based on radian angle
        self.direction = pygame.Vector2(self.pos).rotate(-self.angle)
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

    def debugger(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.angle += 5
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            self.move(-2)
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.move(2)
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.angle += -5


class Line:
    @classmethod
    def from_angle(cls, angle, point, distance):
        r = math.radians(angle)
        end = math.sin(r) * distance + point[0], math.cos(r) * distance + point[1]
        return cls(point, end)

    def __init__(self, start, end):
        self.start = pygame.Vector2(start)
        self.end = pygame.Vector2(end)

    # Line intersect
    def intersect(self, line):
        da = self.end - self.start
        db = line.end - line.start
        dd = self.start - line.start
        dw = pygame.Vector2(-da.y, da.x)
        denom = dw.dot(db)
        num = dw.dot(dd)
        if denom != 0:
            return (num / denom) * db + line.start

    def __repr__(self):
        return str(vars(self))

a = Line((10, 10), (60, 60))
b = Line((20, 60), (60, 20))
print(a.intersect(b))

c = Line.from_angle(90, (0, 15), 1000)
print(c)
print(a.intersect(c))