from utils.location import check_limits
from utils.constants import SPACE_SIZE, DATA_COMMUNICATED_LIST_SIZE


class HostController:
    def __init__(self, host_id, position):
        if not isinstance(position, dict):
            raise TypeError(
                "position must be a dict { 'x': float, 'y': float }")

        self._id = host_id
        self._position = position
        self._data_communicated_list = DATA_COMMUNICATED_LIST_SIZE * []

    def get_id(self):
        return self._id

    def get_position(self):
        return self._position

    def get_data_communicated_list(self):
        return self._data_communicated_list

    def set_position(self, position):
        self._position = position

    def append_data_communicated_list(self, rx, tx):
        print(rx, tx)
        if len(self._data_communicated_list) == DATA_COMMUNICATED_LIST_SIZE:
            self._data_communicated_list.pop(0)
        self._data_communicated_list.append(rx+tx)

    def move_position(self, x_step, y_step):
        new_x = self._position['x'] + x_step
        new_y = self._position['y'] + y_step

        if check_limits(new_x, new_y, float(SPACE_SIZE)):
            self._position['x'] = new_x
            self._position['y'] = new_y
