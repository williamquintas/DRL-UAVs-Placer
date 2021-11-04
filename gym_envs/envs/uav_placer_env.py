import copy
from gym import Env
from gym.spaces import Discrete, Box

import controllers.simulation as simulation
import controllers.uav as uav
import utils.location as loc
from utils.constants import NUMBER_OF_SUBSTEPS, SPACE_SIZE

# Possible actions:
#     0: Stay stopped
#     1: Move up
#     2: Move right
#     3: Move down
#     4: Move left
ACTIONS = {
    0: 'stay_stopped',
    1: 'move_up',
    2: 'move_right',
    3: 'move_down',
    4: 'move_left'
}

class UAVPlacerEnv(Env):
    def __init__(self, number_of_substeps=NUMBER_OF_SUBSTEPS):
        self.action_space = Discrete(5)
        self.observation_space = Box(low=0.0, high=float(SPACE_SIZE), shape=(1,2))
        sim = simulation.init_simulation()
        self.state = sim
        self.remaining_substeps = number_of_substeps


    def _get_movement_by_action(self, action):
        if ACTIONS.get(action) == 'move_up':
            return (0.0, 0.5)
        elif ACTIONS.get(action) == 'move_right':
            return (0.5, 0.0)
        elif ACTIONS.get(action) == 'move_down':
            return (0.0, -0.5)
        elif ACTIONS.get(action) == 'move_left':
            return (-0.5, 0.0)

        return (0.0, 0.0)


    def _move_all_uavs(self, uavs, movement):
        for uav_index in uavs:
            uavs[uav_index] = uav.move(uavs[uav_index], *movement)
        return uavs


    def _calculate_uav_distance_to_center_of_mass(self, state):
        uavs = state['uavs']
        center_of_mass = state['center_of_mass']
        # TODO: implement multiple UAVs scenario
        uav_index = 'uav_0'
        current_uav = uavs[uav_index]
        return loc.calculate_distance(current_uav['position'], center_of_mass)


    def _calculate_reward(self, current_state, previous_state):
        previous_distance = self._calculate_uav_distance_to_center_of_mass(previous_state)
        current_distance = self._calculate_uav_distance_to_center_of_mass(current_state)

        if current_distance < previous_distance:
            return 1
        elif current_distance >= previous_distance:
            return -1


    def step(self, action):
        current_state = copy.deepcopy(self.state)
        movement = self._get_movement_by_action(action)

        uavs = current_state['uavs']
        current_state['uavs'] = self._move_all_uavs(uavs, movement)

        self.remaining_substeps -= 1

        reward = self._calculate_reward(current_state, self.state)

        # TODO: check if reached limits
        uav_distance_to_center_of_mass = self._calculate_uav_distance_to_center_of_mass(current_state)
        if self.remaining_substeps <= 0 or uav_distance_to_center_of_mass == 0:
            done = True
        else:
            done = False

        self.state = current_state
        info = {
            'remaining_substeps': self.remaining_substeps,
            'uav_distance_to_center_of_mass': uav_distance_to_center_of_mass
        }

        return self.state, reward, done, info


    # TODO: implement rendering
    def render(self, mode):
        pass


    def reset(self):
        sim = simulation.init_simulation(hosts=self.state['hosts'])
        self.state = sim
        self.remaining_substeps = NUMBER_OF_SUBSTEPS
        return self.state