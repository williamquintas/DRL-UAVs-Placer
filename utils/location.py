import numpy as np
import random

# comment the line below to generate different random numbers
random.seed(1)


def generate_random_position(max_value=10):
    point = {
        'x': round(random.uniform(0, max_value), 1),
        'y': round(random.uniform(0, max_value), 1)
    }
    return point


def calculate_distance(point1, point2):
    x1 = point1['x']
    x2 = point2['x']
    y1 = point1['y']
    y2 = point2['y']
    p1 = np.array((x1, y1))
    p2 = np.array((x2, y2))
    return np.linalg.norm(p1 - p2)


def check_limits(x, y, max, min=0.0):
    return x >= min and y >= min and x <= max and y <= max


def update_position(position_object, new_position):
    if not isinstance(position_object, dict):
        raise TypeError

    for coordinate in position_object.keys():
        position_object[coordinate] = new_position[coordinate]

    return position_object
