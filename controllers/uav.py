from utils.location import check_limits
from utils.constants import SPACE_SIZE


class UAVController:
    def __init__(self, uav_id, position):
        if not isinstance(position, dict):
            raise TypeError(
                "position must be a dict { 'x': float, 'y': float }")

        self._id = uav_id
        self._position = position

    def get_id(self):
        return self._id

    def get_position(self):
        return self._position

    def set_position(self, position):
        self._position = position

    def move_position(self, x_step, y_step):
        new_x = self._position['x'] + x_step
        new_y = self._position['y'] + y_step

        if check_limits(new_x, new_y, float(SPACE_SIZE)):
            self._position['x'] = new_x
            self._position['y'] = new_y
