from random import Random, random
import threading, random

WAIT_SECONDS = 1

def should_get_file():
    return random.random() >= 0.9

def get_file():
    if should_get_file():
        file_size = random.choice([2, 4, 8, 16, 32, 64, 128, 256, 512, 1024])
        #TODO: implement get_file logic

    threading.Timer(WAIT_SECONDS, get_file).start()
    
get_file()