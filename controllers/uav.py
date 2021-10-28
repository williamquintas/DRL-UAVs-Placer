import utils.location as loc
import utils.constants as const

def build_uav():
    uav = {}

    position = loc.generate_random_position(const.SPACE_SIZE)
    uav['position'] = position

    return uav