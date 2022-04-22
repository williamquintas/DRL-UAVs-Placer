import copy
import random
from gym import Env
from gym.spaces import Discrete, Box

from controllers.simulation import SimulationController, SimulationRendererController
from controllers.uav import UAVController
import utils.location as loc
from utils.constants import BASE_SPEED, NUMBER_OF_SUBSTEPS, PRECISION, SPACE_SIZE

# Possible actions:
#     0: Stay stopped
#     1: Move up
#     2: Move right
#     3: Move down
#     4: Move left
#     5: Increase speed
#     6: Decrease speed
ACTIONS = {
    0: 'stay_stopped',
    1: 'move_up',
    2: 'move_right',
    3: 'move_down',
    4: 'move_left',
    5: 'increase_speed',
    6: 'decrease_speed',
}


class UAVPlacerEnv(Env):
    def __init__(self, number_of_substeps=NUMBER_OF_SUBSTEPS):
        self.action_space = Discrete(len(ACTIONS))
        self.observation_space = Box(
            low=0.0, high=float(SPACE_SIZE), shape=(1, 2))
        self.simulation = SimulationController()
        self.remaining_substeps = number_of_substeps
        self.renderer = SimulationRendererController(self.simulation, "")
        self.speed = BASE_SPEED

        # TODO: implement a way to handle more than single UAV
        uav = self.simulation.get_uavs()[0]
        uav_position = uav.get_position()
        center_of_mass = self.simulation.get_center_of_mass()
        self.state = [
            center_of_mass['x'],
            center_of_mass['y'],
            uav_position['x'],
            uav_position['y']]

    def _get_movement_by_action(self, action):
        if ACTIONS.get(action) == 'move_up':
            return (0.0, self.speed)
        elif ACTIONS.get(action) == 'move_right':
            return (self.speed, 0.0)
        elif ACTIONS.get(action) == 'move_down':
            return (0.0, -self.speed)
        elif ACTIONS.get(action) == 'move_left':
            return (-self.speed, 0.0)

        return (0.0, 0.0)

    def _move_all_uavs(self, movement):
        for uav in self.simulation.get_uavs():
            uav.move_position(*movement)

    def _calculate_uav_distance_to_center_of_mass(self):
        # TODO: implement multiple UAVs scenario
        uav = self.simulation.get_uavs()[0]
        center_of_mass = self.simulation.get_center_of_mass()

        return loc.calculate_distance(uav.get_position(), center_of_mass)

    def _calculate_reward(self, current_distance, previous_distance):
        if current_distance < previous_distance:
            return 1
        elif current_distance >= previous_distance:
            return -1

    def handle_speed_actions(self, action):
        if ACTIONS.get(action) == 'increase_speed':
            MAX_SPEED = 10 * BASE_SPEED
            new_speed = self.speed * random.uniform(1, 5)
            if (self.speed < MAX_SPEED and new_speed < MAX_SPEED):
                self.speed = new_speed
        elif ACTIONS.get(action) == 'decrease_speed':
            MIN_SPEED = BASE_SPEED
            new_speed = self.speed / random.uniform(1, 5)
            if (self.speed > MIN_SPEED and new_speed > MIN_SPEED):
                self.speed = new_speed
        return (0.0, 0.0)

    def handle_action(self, action):
        if ACTIONS.get(action) == 'increase_speed' or ACTIONS.get(
                action) == 'decrease_speed':
            return self.handle_speed_actions(action)
        else:
            return self._get_movement_by_action(action)

    def step(self, action):
        previous_distance = self._calculate_uav_distance_to_center_of_mass()

        movement = self.handle_action(action)
        self._move_all_uavs(movement)
        current_distance = self._calculate_uav_distance_to_center_of_mass()

        self.remaining_substeps -= 1
        reward = self._calculate_reward(current_distance, previous_distance)
        uav_distance_to_center_of_mass = self._calculate_uav_distance_to_center_of_mass()
        if self.remaining_substeps <= 0 or uav_distance_to_center_of_mass <= PRECISION:
            done = True
        else:
            done = False

        uav = self.simulation.get_uavs()[0]
        uav_position = uav.get_position()
        center_of_mass = self.simulation.get_center_of_mass()
        self.state = [
            center_of_mass['x'],
            center_of_mass['y'],
            uav_position['x'],
            uav_position['y']]
        info = {
            'remaining_substeps': self.remaining_substeps,
            'uav_distance_to_center_of_mass': uav_distance_to_center_of_mass,
            'speed': self.speed
        }

        return self.state, reward, done, info

    def render(self, mode, episode_number):
        if mode == 'human':
            self.renderer.set_title(
                "Episode: {} - Remaining steps: {}".format(episode_number, self.remaining_substeps))
            self.renderer.render()

    def reset(self):
        self.simulation = SimulationController()
        self.remaining_substeps = NUMBER_OF_SUBSTEPS
        self.renderer.close()
        self.renderer = SimulationRendererController(self.simulation, "")
        self.speed = BASE_SPEED

        # TODO: implement a way to handle more than single UAV
        uav = self.simulation.get_uavs()[0]
        uav_position = uav.get_position()
        center_of_mass = self.simulation.get_center_of_mass()
        self.state = [
            center_of_mass['x'],
            center_of_mass['y'],
            uav_position['x'],
            uav_position['y']]

        return self.state
