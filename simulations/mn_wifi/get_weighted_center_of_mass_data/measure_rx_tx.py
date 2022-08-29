import os, sys, threading
from subprocess import Popen, PIPE

WAIT_SECONDS = 1
SERVER_ADDRESS = "10.0.0.3"
PATH = os.path.dirname(os.path.abspath(__file__))


def build_command(interface: str, grep: str, field_position: int) -> str:
    return 'ifconfig {} | grep "{}" | cut -d":" -f{} | cut -d" " -f1'.format(interface, grep, field_position)


def read_rx(interface: str) -> int:
    command = build_command(interface, "RX bytes", 2)
    rx = Popen(command, shell=True, stdout=PIPE).stdout.read()
    return int(rx)


def read_tx(interface: str) -> int:
    command = build_command(interface, "TX bytes", 3)
    tx = Popen(command, shell=True, stdout=PIPE).stdout.read()
    return int(tx)


def measure_rx_tx():
    vehicle = sys.argv[1]
    interface = "{}-wlan0".format(vehicle)

    rx, tx = (read_rx(interface), read_tx(interface))
    with open('{}_rx_tx.dat'.format(vehicle), 'a', encoding='utf-8') as file:
        file.write('{},{}\n'.format(rx, tx))

    threading.Timer(WAIT_SECONDS, measure_rx_tx).start()


if __name__ == '__main__':
    measure_rx_tx()