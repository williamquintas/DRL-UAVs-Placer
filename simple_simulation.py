import controllers.simulation as simulation
import json

from utils.location import update_position

sim = simulation.init_simulation(host_quantity=5, uav_quantity=2)

renderer = simulation.SimulationRenderer(sim)

for i in range(10):
    renderer.update_uavs({
        "uav_0": {
            "position": {
                "x": sim['uavs']['uav_0']['position']['x'] - 0.1,
                "y": sim['uavs']['uav_0']['position']['y'] - 0.1
            }
        }
    })

    for host_index in sim['hosts']:
        host = sim['hosts'][host_index]
        host_position = host['position']

        new_position = {}
        for coordinate_index, value in host_position.items():
            new_position.update({
                coordinate_index: host_position[coordinate_index] - 0.1,
            })
        sim = simulation.update_host_position(sim, {
            f'{host_index}': {
                'position': update_position(host_position, new_position)
            }
        })
    renderer.render(title="Simple simulation")

renderer.close()

print(json.dumps(sim, indent=2))