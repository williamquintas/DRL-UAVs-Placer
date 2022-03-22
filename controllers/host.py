from utils.location import check_limits
from utils.constants import SPACE_SIZE


class HostController:
    def __init__(self, id, position):
        if not isinstance(position, dict):
            raise TypeError(
                "position must be a dict { 'x': float, 'y': float }")
        else:
            self.id = id
            self.position = position

    def get_id(self):
        return self.id

    def get_position(self):
        return self.position

    def move_position(self, x_step, y_step):
        new_x = self.position['x'] + x_step
        new_y = self.position['y'] + y_step

        if check_limits(new_x, new_y, float(SPACE_SIZE)):
            self.position['x'] = new_x
            self.position['y'] = new_y
