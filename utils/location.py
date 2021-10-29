import numpy as np
import random

# comment the line below to generate different random numbers
random.seed(1)

def generate_random_position(max_value=10):
    point = {
        'x': round(random.uniform(0,max_value), 1),
        'y': round(random.uniform(0,max_value), 1)
    }
    return point

def calculate_distance(point1, point2):
    x1 = point1['x']
    x2 = point2['x']
    y1 = point1['y']
    y2 = point2['y']
    return np.linalg.norm([(x1, y1), (x2, y2)])