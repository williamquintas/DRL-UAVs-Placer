import csv
import sys
from controllers.simulation import SimulationController, SimulationRendererController
sys.path.append('.')


simulation = SimulationController(host_quantity=1, uav_quantity=1)
renderer = SimulationRendererController(simulation, "Positioning hosts from CSV")


ID = 'D863340'


def filter_longitude_latitude_headers(column):
    return column[0] == 'latitude' or column[0] == 'longitude'


with open(f'./data/{ID}_normalized.csv', 'r', encoding='utf-8') as csv_file:
    data = csv.reader(csv_file)
    headers = next(data, None)

    for index, row in enumerate(data):
        position = {}

        for header, value in tuple(
                filter(filter_longitude_latitude_headers, zip(headers, row))):
            # TODO: get CSV normalized data
            position['x' if header == 'latitude' else 'y'] = float(
                value) / 10.0

        host = simulation.get_hosts()[0]
        host.set_position(position)
        renderer.render()

renderer.close()
