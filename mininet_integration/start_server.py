import os

from utils.constants import FILES_SIZES

def create_files():
    for file_size in FILES_SIZES:
        os.system("truncate -s {file_size}K {file_size}K-file.txt".format(file_size=file_size))

def serve():
    PORT = 80
    os.system("python3 -m http.server {}".format(PORT))

if __name__ == '__main__':
    create_files()
    serve()