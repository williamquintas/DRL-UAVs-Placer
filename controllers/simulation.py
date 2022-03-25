import json
import matplotlib.pyplot as plt

from controllers.host import HostController
from controllers.uav import UAVController
from utils.constants import SPACE_SIZE
from utils.location import generate_random_position


class SimulationController:
    def __init__(self, host_quantity=2, uav_quantity=1, **kw_args):
        self._hosts = []
        self._uavs = []
        self._center_of_mass = None

        if 'hosts' in kw_args:
            self._hosts = kw_args['hosts']
        else:
            for host_index in range(host_quantity):
                position = generate_random_position(SPACE_SIZE)
                new_host = HostController(f'host_{host_index}', position)
                self._hosts.append(new_host)

        for uav_index in range(uav_quantity):
            position = generate_random_position(SPACE_SIZE)
            new_uav = UAVController(f'uav_{uav_index}', position)
            self._uavs.append(new_uav)

        self._calculate_center_of_mass()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=2)

    def get_hosts(self):
        return self._hosts

    def get_uavs(self):
        return self._uavs

    def get_center_of_mass(self):
        self._calculate_center_of_mass()
        return self._center_of_mass

    def _calculate_center_of_mass(self):
        x_sum = 0.0
        y_sum = 0.0
        hosts_quantity = len(self._hosts)

        for host in self.get_hosts():
            position = host.get_position()
            x_sum += position['x']
            y_sum += position['y']

        self._center_of_mass = {
            'x': round(x_sum / hosts_quantity, 2),
            'y': round(y_sum / hosts_quantity, 2)
        }


class SimulationRendererController():
    def __init__(self, simulation, title):
        self._simulation = simulation
        self._title = title
        self._data = {
            'x': [],
            'y': [],
            'labels': [],
            'colors': []
        }
        self._fig = plt.figure()
        self._ax = plt.subplot(1, 1, 1)
        self._reset_ax()

    def set_title(self, title):
        self._title = title

    def _clear_lists(self):
        self._data['x'] = []
        self._data['y'] = []
        self._data['labels'] = []
        self._data['colors'] = []

    def _reset_ax(self):
        self._clear_lists()
        self._ax.clear()
        self._ax.axis([0, SPACE_SIZE, 0, SPACE_SIZE])
        self._ax.set_title(f'Simulation - {self._title}')
        self._ax.set_xlabel('X')
        self._ax.set_ylabel('Y')

    def _build_center_of_mass_rendering(self):
        center_of_mass = self._simulation.get_center_of_mass()
        self._data['x'].append(center_of_mass['x'])
        self._data['y'].append(center_of_mass['y'])
        self._data['labels'].append('center_of_mass')
        self._data['colors'].append('red')

    def _build_hosts_rendering(self):
        for host in self._simulation.get_hosts():
            position = host.get_position()
            self._data['x'].append(position['x'])
            self._data['y'].append(position['y'])
            self._data['labels'].append(host.get_id())
            self._data['colors'].append('black')

    def _build_uavs_rendering(self):
        for uav in self._simulation.get_uavs():
            position = uav.get_position()
            self._data['x'].append(position['x'])
            self._data['y'].append(position['y'])
            self._data['labels'].append(uav.get_id())
            self._data['colors'].append('blue')

    def _build_rendering(self):
        self._reset_ax()
        self._build_hosts_rendering()
        self._build_center_of_mass_rendering()
        self._build_uavs_rendering()

    def render(self):
        self._build_rendering()

        self._ax.scatter(self._data['x'], self._data['y'], color=self._data['colors'])
        for i, txt in enumerate(self._data['labels']):
            self._ax.annotate(txt, (self._data['x'][i], self._data['y'][i]))

        plt.draw()
        plt.pause(4e-11)

    def close(self):
        plt.close(self._fig)
