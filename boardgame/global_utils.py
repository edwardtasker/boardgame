import random
import math
from typing import Tuple
import pygame

def get_random_colour(min_=150, max_=255) -> Tuple[int, ...]:
    """Returns a random RGB colour with each component between min_ and max_"""
    return tuple(random.choices(list(range(min_, max_)), k=3))


# def get_equilateral_triangle_coords(centre, radius):
#     """Returns a list of vertices for an equilateral triangle given its center and side length."""

#     centre_x, centre_y = centre[0], centre[1]
#     half_side = 2 * radius * math.cos(math.pi / 6)
#     #   half_side = side_length / 2
    
#     angle = math.pi / 3  # 60 degrees in radians
#     height = half_side * math.sqrt(3)

#     # Calculate vertices
#     p1 = (centre_x, centre_y - height / 3)  # Top vertex
#     p2 = (centre_x + half_side * math.cos(angle), centre_y + height / 3)
#     p3 = (centre_x - half_side * math.cos(angle), centre_y + height / 3)

#     return (p1, p2, p3)

def get_equilateral_triangle_coords(centre, area):
    """Calculates the vertices of an equilateral triangle given its center and area."""
    
    centre_x, centre_y = centre[0], centre[1]
    # Calculate side length
    side_length = math.sqrt(4 * area / math.sqrt(3))

    # Calculate radius of circumcircle
    radius = side_length / (math.sqrt(3))

    # Calculate angles for vertices
    angle_step = 2 * math.pi / 3

    # Calculate vertex positions
    vertices = []
    for i in range(3):
        angle = math.pi / 6 + i * angle_step
        x = centre_x + radius * math.cos(angle)
        y = centre_y + radius * math.sin(angle)
        vertices.append((x, y))

    return vertices


def get_square_coords(centre, area):
    """Returns a list of vertices for an square given its center and side length."""
    centre_x, centre_y = centre[0], centre[1]

    side_length = math.sqrt(area)
    half_side = side_length / 2
    side_length = 2*half_side

    return (centre_x - half_side, centre_y - half_side, side_length, side_length)


def get_hexagon_coords(centre, radius):
    """Calculates the vertices of a hexagon given its center and radius."""

    centre_x, centre_y = centre[0], centre[1]
    vertices = []
    angle_step = 2 * math.pi / 6  # 60 degrees in radians

    for i in range(6):
        angle = i * angle_step
        x = centre_x + radius * math.cos(angle)
        y = centre_y + radius * math.sin(angle)
        vertices.append((x, y))

    return vertices

def create_dice_image(size, color, dot_color, value):
    """Creates a dice image with the specified size, color, and dot color."""
    dice_image = pygame.Surface((size, size))
    dice_image.fill(color)

    dot_radius = size // 10

    # Define dot positions
    dot_positions = [
        (size // 2, size // 2),  # Center
        (size // 4, size // 4),
        (size * 3 // 4, size // 4),
        (size // 4, size * 3 // 4),
        (size * 3 // 4, size * 3 // 4),
        (size // 4, size // 2),
        (size * 3 // 4, size // 2),
        (size * 3 // 4, size // 2)
    ]

    # Determine the dots for each dice value
    dot_patterns = [
        [],
        [0],
        [1, 4],
        [0, 2, 3],
        [1, 2, 3, 4],
        [0, 1, 2, 3, 4],
        [1, 2, 3, 4, 5, 6]
    ]

    # Draw dots based on dice value
    for i in range(value):
        pygame.draw.circle(dice_image, dot_color, dot_positions[dot_patterns[value][i]], dot_radius)  # Replace with desired dice value

    return dice_image
