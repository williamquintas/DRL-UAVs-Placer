import controllers.host as host
import controllers.uav as uav

import matplotlib.pyplot as plt
import utils.location as loc
from utils.constants import SPACE_SIZE 

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


def init_simulation(host_quantity=2, uav_quantity=1):
    simulation = {}
    hosts_dict = {}
    uavs_dict = {}

    for host_index in range(host_quantity):
        hosts_dict.update({
            f'host_{host_index}': host.build_host()
        })

    for uav_index in range(uav_quantity):
        uavs_dict.update({
            f'uav_{uav_index}': uav.build_uav()
        })

    simulation['hosts'] = hosts_dict
    simulation['uavs'] = uavs_dict
    simulation['center_of_mass'] = calculate_center_of_mass(hosts_dict)

    return simulation

def plot(simulation):
    x = list()
    y = list()
    labels = list()
    colors = list()

    # Plots hosts
    hosts_dict = simulation['hosts']
    for host_index in hosts_dict:
        host = hosts_dict[host_index]
        position = host['position']
        x.append(position['x'])
        y.append(position['y'])
        labels.append(host_index)
        colors.append('black')

    # Plots center of mass
    center_of_mass = simulation['center_of_mass']
    plt.scatter(center_of_mass['x'], center_of_mass['y'], color=['red'])
    plt.annotate('center_of_mass', (center_of_mass['x'], center_of_mass['y']))

    # Plots UAVs - TODO: plot UAVs moving
    uavs_dict = simulation['uavs']
    for uav_index in uavs_dict:
        uav = uavs_dict[uav_index]
        position = uav['position']
        x.append(position['x'])
        y.append(position['y'])
        labels.append(uav_index)
        colors.append('blue')

    plt.scatter(x, y, color=colors)
    for i, txt in enumerate(labels):
        plt.annotate(txt, (x[i], y[i]))

    plt.axis([0, SPACE_SIZE, 0, SPACE_SIZE])
    plt.title('Simulation')
    plt.xlabel('X')
    plt.ylabel('Y')

    plt.show()
    plt.clf()