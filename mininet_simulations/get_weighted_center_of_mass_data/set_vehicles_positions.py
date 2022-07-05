#!/usr/bin/python
import csv, socket, sys, time
sys.path.append('..')

from utils.constants import SIMULATION_SOCKET_PORT, MININET_SOCKET_PORT
from utils.log import log


def build_client(port: int) -> socket:
    host = '127.0.0.1'
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    return client


def send_message(port: int, message: str) -> None:
    client = build_client(port)
    client.send(str(message).encode('utf-8'))
    client.close()
    time.sleep(0.1)


def send_command_to_mininet_socket(message: str) -> None:
    port = MININET_SOCKET_PORT
    send_message(port, message)


def send_command_to_simulation(message: str) -> None:
    port = SIMULATION_SOCKET_PORT
    send_message(port, message)


def filter_row_fields(column: dict) -> bool:
    return column[0] == 'latitude' or \
        column[0] == 'longitude' or \
        column[0] == 'date' or \
        column[0] == 'time'


def read_data_from_csv(vehicle_name: str, coordinates_list: str) -> list:
    file_path = '../data/{}.csv'.format(vehicle_name)

    with open(file_path, 'r', encoding='utf-8') as csv_file:
        data = csv.reader(csv_file)
        headers = next(data)

        updated_coordinates_list = coordinates_list
        for row in list(data):
            coordinate = {}
            for header, value in tuple(filter(filter_row_fields, zip(headers, row))):
                coordinate[header] = value
            coordinate['datetime'] = coordinate['date'] + coordinate['time']
            coordinate['vehicle'] = vehicle_name
            updated_coordinates_list.append(coordinate)

        return updated_coordinates_list


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        log("No vehicles passed in arguments. \n")
        sys.exit()
    else:
        data_list = []
        for n in range(1, len(sys.argv)):
            log("*** Getting {}'s data\n".format(sys.argv[n]))
            vehicle = sys.argv[n]
            data_list = read_data_from_csv(vehicle, data_list)
        data_list.sort(key=lambda coordinate: coordinate['datetime'])

        log("\n*** Sending commands for mininet and simulation\n")
        for coordinate in data_list:
            command = "set.{}.setPosition(\"{},{},0.0\")"\
                .format(coordinate['vehicle'],
                        str(coordinate['longitude']),
                        str(coordinate['latitude'])
                        )
            send_command_to_mininet_socket(command)
            command = "{} set_position {} {} {}" \
                .format(coordinate['vehicle'],
                        str(coordinate['longitude']),
                        str(coordinate['latitude']),
                        "T".join([coordinate['date'], coordinate['time']])
                        )
            send_command_to_simulation(command)
        print("***** Finished sending coordinates! *****")
