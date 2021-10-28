import utils.location as loc
import utils.constants as const

def build_host():
    host = {}

    position = loc.generate_random_position(const.SPACE_SIZE)
    host['position'] = position

    return host