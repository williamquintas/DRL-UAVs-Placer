import controllers.simulation as simulation
import json

sim = simulation.init_simulation()
simulation.plot(sim)

print(json.dumps(sim, indent=2))
