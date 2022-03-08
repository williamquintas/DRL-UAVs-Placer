#!/usr/bin/python

import csv
import sys
import socket
import time
import os

from mininet.log import info

def client(message):
    host = '127.0.0.1'
    port = 12345  # Make sure it's within the > 1024 $$ <65535 range
    s = socket.socket()
    s.connect((host, port))
    s.send(str(message).encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    info('Received from server: ' + data)
    s.close()

filter_longitude_latitude_headers = lambda column: column[0] == 'latitude' \
                                                or column[0] == 'longitude'

def read_data(file, node):
    with open(file, 'r') as csv_file:
        data = csv.reader(csv_file)

        headers = next(data, None)

        coordinates_list = []
        for index, row in enumerate(data):
            print("Reading {} line".format(index))
            coordinate = {}

            for header, value in tuple(filter(filter_longitude_latitude_headers, zip(headers, row))):
                coordinate[header]= value
                
            coordinates_list.append(coordinate)

        for coordinate in coordinates_list:
            command = "set.{}.setPosition(\"{},{},0.0\")".format(node, str(coordinate['longitude']), str(coordinate['latitude']))
            client(command)
            time.sleep(0.5)
    
if __name__ == '__main__':
    nodes = []
    files = []

    if len(sys.argv) <= 1:
        info("No nodes defined")
        sys.exit()
    else:
        path = os.path.dirname(os.path.abspath(__file__))
        for n in range(1, len(sys.argv)):
            nodes.append(sys.argv[n])
            file_path = '{}/data/{}.csv'.format(path, sys.argv[n])
            files.append(file_path)

    while True:
        i = 0
        for data_file in files:
            read_data(data_file, nodes[i])
            i += 1
