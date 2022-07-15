import random
import numpy as np
from gym import Env
from gym.spaces import Discrete, Box
from controllers.host import HostController

from controllers.simulation import SimulationController
from controllers.uav import UAVController
import utils.location as loc
from utils.constants import BASE_SPEED, PRECISION

# Possible actions:
#     0: Stay stopped
#     1: Move up
#     2: Move right
#     3: Move down
#     4: Move left
ACTIONS = {
    -2: 'stay_stopped',
    -1: 'move_up',
    0: 'move_right',
    1: 'move_down',
    2: 'move_left',
}


class UAVPlacerEnv(Env):
    def __init__(self):
        self.action_space = Discrete(5, start=-2)
        boundaries = np.array(
            [
                180.0,
                90.0,
                180.0,
                90.0
            ],
            dtype=np.float32,
        )
        self.observation_space = Box(low=-boundaries, high=boundaries, dtype=np.float32)
        self.speed = BASE_SPEED

        self._start_simulation()
        uav_position = self.simulation.get_uavs()[0].get_position()
        center_of_mass = self.simulation.get_center_of_mass()

        self.state = np.array(
            [
                uav_position['x'],
                uav_position['y'],
                center_of_mass['x'],
                center_of_mass['y'],
            ],
            dtype=np.float32
        )


    def _start_simulation(self) -> None:
        random_coordinates = loc.generate_random_coordinates()
        host1 = HostController("host_1", random_coordinates)
        host2 = HostController("host_2", {'x': random_coordinates['x']+0.08, 'y': random_coordinates['y']+0.08})

        uav_position = {
            'x': random.uniform(host1.get_position()['x'],host2.get_position()['x']),
            'y': random.uniform(host1.get_position()['y'],host2.get_position()['y'])
        }

        uav = UAVController("uav_1", uav_position)
        self.simulation = SimulationController(hosts=[host1,host2], uavs=[uav])


    def _calculate_uav_distance_to_center_of_mass(self) -> float:
        uav = self.simulation.get_uavs()[0]
        center_of_mass = self.simulation.get_center_of_mass()

        return loc.calculate_geodesic_distance(uav.get_position(), center_of_mass)


    def _calculate_reward(self, current_distance, previous_distance):
        if current_distance < previous_distance:
            return 1
        elif current_distance >= previous_distance:
            return -1


    def _move_uav(self, action):
        uav = self.simulation.get_uavs()[0]
        current_position = uav.get_position()
        if ACTIONS.get(action) == 'move_up':
            direction = 0
        elif ACTIONS.get(action) == 'move_right':
            direction = 90
        elif ACTIONS.get(action) == 'move_down':
            direction = 180
        elif ACTIONS.get(action) == 'move_left':
            direction = -90

        if ACTIONS.get(action) != 'stay_stopped':
            new_position = loc.calculate_geodesic_movement(current_position, direction, BASE_SPEED/60.0)
            uav.set_position(new_position)

    def step(self, action):
        previous_distance = self._calculate_uav_distance_to_center_of_mass()

        # Move UAV
        self._move_uav(action)

        # Calculate distance to center of mass
        current_distance = self._calculate_uav_distance_to_center_of_mass()

        # Calculate reward
        reward = self._calculate_reward(current_distance, previous_distance)

        # Check if is done
        if current_distance <= PRECISION:
            done = True
        else:
            done = False

        uav = self.simulation.get_uavs()[0]
        uav_position = uav.get_position()
        center_of_mass = self.simulation.get_center_of_mass()
        self.state = np.array(
            [
                uav_position['x'],
                uav_position['y'],
                center_of_mass['x'],
                center_of_mass['y'],
            ],
            dtype=np.float32
        )
        info = {
            'current_distance': current_distance,
        }

        return self.state, reward, done, info


    def render(self):
        pass


    def reset(self):
        self._start_simulation()
        uav_position = self.simulation.get_uavs()[0].get_position()
        center_of_mass = self.simulation.get_center_of_mass()

        self.state = np.array(
            [
                uav_position['x'],
                uav_position['y'],
                center_of_mass['x'],
                center_of_mass['y'],
            ],
            dtype=np.float32
        )

        return self.state
