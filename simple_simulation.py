import controllers.simulation as simulation
import json

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
    renderer.render(title="Simple simulation")

renderer.close()

print(json.dumps(sim, indent=2))