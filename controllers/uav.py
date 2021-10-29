import utils.location as loc
import utils.constants as const

def build_uav():
    uav = {}

    position = loc.generate_random_position(const.SPACE_SIZE)
    uav['position'] = position

    return uav

def move(uav, x_step, y_step):
    position = uav['position']
    position['x'] += x_step
    position['y'] += y_step
    return uav