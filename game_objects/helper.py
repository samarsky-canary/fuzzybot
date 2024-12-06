import pygame
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 20
RECT_SIZE = (50, 100)

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Distance from View Vector to Rect")

# Player properties
player_pos = np.array([440, 300])  # Player starting position
view_vector = np.array([0, -1])  # Direction the player is facing (upwards)
player_color = (0, 255, 0)

# Rectangle properties
rect_pos = np.array([400, 100])  # Rectangle starting position (top-left corner)
rect_color = (255, 0, 0)

# Function to calculate the closest point on the rectangle to the player
def closest_point_on_rect(rect_pos, rect_size, point):
    # Rectangle boundaries
    rect_left = rect_pos[0]
    rect_right = rect_pos[0] + rect_size[0]
    rect_top = rect_pos[1]
    rect_bottom = rect_pos[1] + rect_size[1]

    # Clamp the point to the rectangle's closest edge
    closest_x = max(rect_left, min(point[0], rect_right))
    closest_y = max(rect_top, min(point[1], rect_bottom))

    return np.array([closest_x, closest_y])

# Function to calculate the distance
def distance(point1, point2):
    return np.linalg.norm(point1 - point2)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw player
    pygame.draw.rect(screen, player_color, (player_pos[0]-PLAYER_SIZE//2, player_pos[1]-PLAYER_SIZE//2, PLAYER_SIZE, PLAYER_SIZE))

    # Draw rectangle
    pygame.draw.rect(screen, rect_color, (rect_pos[0], rect_pos[1], RECT_SIZE[0], RECT_SIZE[1]))

    # Calculate the end point of the view vector (for visualization)
    view_end_point = player_pos + view_vector * 100  # Extend the view vector (100 units)

    # Draw the view vector
    pygame.draw.line(screen, (255, 255, 0), player_pos, view_end_point, 3)

    # Calculate the closest point on the rectangle to the player's position
    closest_point = closest_point_on_rect(rect_pos, RECT_SIZE, player_pos)

    # Calculate the distance
    dist_to_rect = distance(player_pos, closest_point)

    # For drawing, let's mark the closest point on the rectangle
    pygame.draw.circle(screen, (0, 0, 255), (int(closest_point[0]), int(closest_point[1])), 5)

    # Print distance to console
    print("Distance from player to rectangle:", dist_to_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()