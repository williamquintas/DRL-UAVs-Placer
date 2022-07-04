import os, random, threading
from utils.constants import FILES_SIZES

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
        os.system("wget -q -O {path}/downloaded_files/{filename} {address}/{filename} &".format(path=PATH, address=SERVER_ADDRESS, filename=filename))

    else:
        print("Not getting files this time.")

    threading.Timer(WAIT_SECONDS, get_file).start()


if __name__ == '__main__':
    get_file()