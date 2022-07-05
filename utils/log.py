from utils.constants import VERBOSE

FILE_PATH = 'data.csv'

def log(*values: object):
    if VERBOSE:
        print(values)

def write_to_file(row: str):
    with open(FILE_PATH, 'a', encoding='utf-8') as csv_file:
        csv_file.write(row)