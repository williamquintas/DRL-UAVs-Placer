from utils.location import check_limits
from utils.constants import SPACE_SIZE, DATA_COMMUNICATED_LIST_SIZE

def removes_unwanted_characters(data_list_str: str) -> str:
    return data_list_str.replace('[', '').replace(']', '')

def cast_str_tuples_to_int(rx_tx_list: list) -> list:
    split_rx_tx_str = lambda item: tuple(item.split(','))
    rx_tx_tuples_list = list(map(split_rx_tx_str, rx_tx_list))

    cast_tuple_elements_to_int = lambda t: tuple(map(int, t))
    return list(map(cast_tuple_elements_to_int, rx_tx_tuples_list))

def get_rx_tx_pairs_from_str(data_list_str: str) -> list:
    data_list_str = removes_unwanted_characters(data_list_str)
    elements_list = data_list_str.split('),(')

    removes_parenthesis = lambda item: item.replace('(', '').replace(')', '')
    elements_without_parenthesis = list(map(removes_parenthesis, elements_list))

    return cast_str_tuples_to_int(elements_without_parenthesis)

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

    def get_avg_data_communicated_per_second(self):
        data_communicated_sum = 0.0

        for data_communicated in self._data_communicated_list:
            data_communicated_sum += (data_communicated[0] + data_communicated[1])

        return data_communicated_sum / DATA_COMMUNICATED_LIST_SIZE

    def set_position(self, position):
        self._position = position

    def set_data_communicated_list(self, data_list: list):
        self._data_communicated_list = get_rx_tx_pairs_from_str(''.join(data_list))

    def move_position(self, x_step, y_step):
        new_x = self._position['x'] + x_step
        new_y = self._position['y'] + y_step

        if check_limits(new_x, new_y, float(SPACE_SIZE)):
            self._position['x'] = new_x
            self._position['y'] = new_y
