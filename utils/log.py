from utils.constants import VERBOSE


def log(*values: object):
    if VERBOSE:
        print(values) 