import random

# comment the line below to generate different random numbers
random.seed(1)

def generate_random_position():
    point = {
        'x': round(random.uniform(0,10), 2),
        'y': round(random.uniform(0,10), 2)
    }
    return point

def build_uav():
    uav = {}

    position = generate_random_position()
    uav['position'] = position

    return uav