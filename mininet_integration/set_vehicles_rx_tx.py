import socket
import sys
import threading
import time
from utils.constants import DATA_COMMUNICATED_LIST_SIZE, SIMULATION_SOCKET_PORT
from utils.print import log

WAIT_SECONDS = 1

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


def send_command_to_simulation(message: str) -> None:
    port = SIMULATION_SOCKET_PORT
    send_message(port, message)


def read_files() -> None:
    for n in range(1, len(sys.argv)):
        vehicle = sys.argv[n]
        try:
            with open('{}_rx_tx.dat'.format(vehicle), 'r', encoding='utf-8') as file:
                lines = file.readlines() [-DATA_COMMUNICATED_LIST_SIZE:]
                lines = list(map(lambda line: tuple(map(int, line.replace('\n', '').split(','))), lines))
                command = "{} set_rx_tx {}".format(vehicle, str(lines))
                send_command_to_simulation(command)
        except:
            log("{} dat file not found".format(vehicle))

    threading.Timer(WAIT_SECONDS, read_files).start()

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        log("No vehicles passed in arguments. \n")
        sys.exit()
    else:
        time.sleep(1) # Required to wait files to be created
        read_files()