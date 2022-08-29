import random
import numpy as np
from geopy.distance import geodesic

# comment the line below to generate different random numbers
random.seed(1)


def generate_random_coordinates():
    point = {
        'x': random.uniform(-180.0, 180.0),
        'y': random.uniform(-90.0, 90.0)
    }
    return point


def calculate_distance(point1, point2):
    p1_as_arr = np.array((point1['x'], point1['y']))
    p2_as_arr = np.array((point2['x'], point2['y']))
    return np.linalg.norm(p1_as_arr - p2_as_arr)


def calculate_geodesic_distance(point1, point2):
    return geodesic((point1['y'],point1['x']), (point2['y'],point2['x'])).kilometers


def calculate_geodesic_movement(point, direction, distance):
    new_point = geodesic(kilometers=distance).destination((point['y'], point['x']), bearing=direction)
    return { 'x': new_point[1], 'y': new_point[0] }


def check_limits(pos_x, pos_y, max_value, min_value=0.0):
    return min_value <= pos_x <= max_value and min_value <= pos_y <= max_value


def update_position(position_object, new_position):
    if not isinstance(position_object, dict):
        raise TypeError

    for coordinate in position_object.keys():
        position_object[coordinate] = new_position[coordinate]

    return position_object
