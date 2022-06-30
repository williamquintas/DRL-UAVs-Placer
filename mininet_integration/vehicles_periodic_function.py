import os, random, sys, threading
from utils.constants import FILES_SIZES
from subprocess import Popen, PIPE

WAIT_SECONDS = 1
SERVER_ADDRESS = "10.0.0.3"
PATH = os.path.dirname(os.path.abspath(__file__))

def should_get_file():
    return random.random() >= 0.9


def get_file():
    if should_get_file():
        file_size = random.choice(FILES_SIZES)
        filename = "{}K-file.txt".format(file_size)

        print("Downloading {}K-file.txt".format(filename))
        os.system("wget -O {path}/downloaded_files/{filename} {address}/{filename} &".format(path=PATH, address=SERVER_ADDRESS, filename=filename))

    else:
        print("Not getting files this time.")

    threading.Timer(WAIT_SECONDS, get_file).start()


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
    interface = "{}-wlan0".format(sys.argv[1])
    print(interface, read_rx(interface), read_tx(interface))
    threading.Timer(WAIT_SECONDS, measure_rx_tx).start()


if __name__ == '__main__':
    get_file()
    measure_rx_tx()