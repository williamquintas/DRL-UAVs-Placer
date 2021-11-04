import controllers.simulation as simulation
import json

sim = simulation.init_simulation(host_quantity=5, uav_quantity=1)
simulation.plot_graph(sim)

print(json.dumps(sim, indent=2))