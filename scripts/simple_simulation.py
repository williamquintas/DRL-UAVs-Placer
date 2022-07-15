import sys
sys.path.append('.')
from controllers.simulation import SimulationController, SimulationRendererController

simulation = SimulationController(host_quantity=5, uav_quantity=2)
renderer = SimulationRendererController(simulation, title="Simple simulation")

for i in range(10):
    for uav in simulation.get_uavs():
        uav.move_position(0.1, 0.1)

    for host in simulation.get_hosts():
        host.move_position(-0.1, -0.1)

    renderer.render()

renderer.close()

print(simulation.to_json())
