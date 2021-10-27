from controllers.uav import build_uav
import matplotlib.pyplot as plt

def calculate_mass_center(uavs_dict):
    x_sum = 0.0
    y_sum = 0.0

    for uav_index in uavs_dict:
        uav = uavs_dict[uav_index]
        position = uav['position']
        x_sum += position['x']
        y_sum += position['y']

    mass_center = {
        'x': round(x_sum/len(uavs_dict), 2),
        'y': round(y_sum/len(uavs_dict), 2)
    }

    return mass_center


def init_simulation(uav_quantity=2):
    simulation = {}
    uavs_dict = {}

    for uav_index in range(uav_quantity):
        uavs_dict.update({
            f'uav_{uav_index}': build_uav()
        })

    simulation['uavs'] = uavs_dict
    simulation['mass_center'] = calculate_mass_center(uavs_dict)

    return simulation

def plot(simulation):
    x = list()
    y = list()
    labels = list()

    uavs_dict = simulation['uavs']
    for uav_index in uavs_dict:
        uav = uavs_dict[uav_index]
        position = uav['position']
        x.append(position['x'])
        y.append(position['y'])
        labels.append(uav_index)

    plt.scatter(x, y)
    for i, txt in enumerate(labels):
        plt.annotate(txt, (x[i], y[i]))

    mass_center = simulation['mass_center']
    plt.scatter(mass_center['x'], mass_center['y'], color=['red'])
    plt.annotate('mass_center', (mass_center['x'], mass_center['y']))

    plt.title('Simulation')
    plt.xlabel('X')
    plt.xlim(0,10)
    plt.ylabel('Y')
    plt.ylim(0,10)
    plt.show()