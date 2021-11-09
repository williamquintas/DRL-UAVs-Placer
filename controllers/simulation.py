import controllers.host as host
import controllers.uav as uav

import matplotlib.pyplot as plt
from utils.constants import SPACE_SIZE

def init_simulation(host_quantity=2, uav_quantity=1, **kw_args):
    simulation = {}
    hosts_dict = {}
    uavs_dict = {}

    if 'hosts' in kw_args:
        simulation['hosts'] = kw_args['hosts']
    else:
        for host_index in range(host_quantity):
            hosts_dict.update({
                f'host_{host_index}': host.build_host()
            })
        simulation['hosts'] = hosts_dict

    for uav_index in range(uav_quantity):
        uavs_dict.update({
            f'uav_{uav_index}': uav.build_uav()
        })

    simulation['uavs'] = uavs_dict
    simulation['center_of_mass'] = calculate_center_of_mass(simulation['hosts'])

    return simulation


def calculate_center_of_mass(hosts_dict):
    x_sum = 0.0
    y_sum = 0.0

    for host_index in hosts_dict:
        host = hosts_dict[host_index]
        position = host['position']
        x_sum += position['x']
        y_sum += position['y']

    center_of_mass = {
        'x': round(x_sum/len(hosts_dict), 2),
        'y': round(y_sum/len(hosts_dict), 2)
    }

    return center_of_mass

class SimulationRenderer():
    def __init__(self, simulation):
        self._simulation = simulation
        self._fig = plt.figure()
        self._ax = plt.subplot(1,1,1)
        self._reset_ax()

    def _clear_lists(self):
        self._x = list()
        self._y = list()
        self._labels = list()
        self._colors = list()

    def _reset_ax(self, title=1):
        self._clear_lists()
        self._ax.clear()
        self._ax.axis([0, SPACE_SIZE, 0, SPACE_SIZE])
        self._ax.set_title(f'Simulation - {title}')
        self._ax.set_xlabel('X')
        self._ax.set_ylabel('Y')

    def _build_hosts_rendering(self):
        for host_index in self._simulation['hosts']:
            host = self._simulation['hosts'][host_index]
            position = host['position']
            self._x.append(position['x'])
            self._y.append(position['y'])
            self._labels.append(host_index)
            self._colors.append('black')

    def _build_center_of_mass_rendering(self):
        center_of_mass = self._simulation['center_of_mass']
        self._x.append(center_of_mass['x'])
        self._y.append(center_of_mass['y'])
        self._labels.append('center_of_mass')
        self._colors.append('red')

    def _build_uavs_rendering(self):
        for uav_index in self._simulation['uavs']:
            uav = self._simulation['uavs'][uav_index]
            position = uav['position']
            self._x.append(position['x'])
            self._y.append(position['y'])
            self._labels.append(uav_index)
            self._colors.append('blue')

    def _build_rendering(self, title):
        self._reset_ax(title)
        self._build_hosts_rendering()
        self._build_center_of_mass_rendering()
        self._build_uavs_rendering()

    def update_uavs(self, uavs):
        self._simulation['uavs'] = uavs

    def render(self, title):
        self._build_rendering(title)

        self._ax.scatter(self._x, self._y, color=self._colors)
        for i, txt in enumerate(self._labels):
            self._ax.annotate(txt, (self._x[i], self._y[i]))

        plt.draw()
        plt.pause(4e-11)

    def close(self):
        plt.close(self._fig)
