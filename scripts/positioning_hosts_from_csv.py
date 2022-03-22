from itertools import islice
import csv
import controllers.simulation as simulation
import sys
sys.path.append('.')


sim = simulation.init_simulation(host_quantity=1, uav_quantity=1)
renderer = simulation.SimulationRendererController(sim)


ID = 'D863340'


def filter_longitude_latitude_headers(column): return column[0] == 'latitude' \
    or column[0] == 'longitude'


with open(f'./data/{ID}_normalized.csv', 'r') as csv_file:
    data = csv.reader(csv_file)
    headers = next(data, None)

    for index, row in enumerate(data):
        position = {}

        for header, value in tuple(
                filter(filter_longitude_latitude_headers, zip(headers, row))):
            # TODO: get CSV normalized data
            position['x' if header == 'latitude' else 'y'] = float(
                value) / 10.0

        sim = simulation.update_host_position(sim, {
            'host_0': {
                'position': position
            }
        })
        renderer.render(title="Positioning hosts from CSV")

renderer.close()
