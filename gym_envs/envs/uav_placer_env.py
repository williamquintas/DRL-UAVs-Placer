import random
import numpy as np
from typing import Optional
from gym import Env
from gym.spaces import Discrete, Box
from gym.error import DependencyNotInstalled
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
    metadata = {
        "render_modes": ["human", "rgb_array", "single_rgb_array"],
        "render_fps": 50,
    }

    def __init__(self, render_mode: Optional[str] = None):
        self.action_space = Discrete(5)
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

        self.render_mode = render_mode
        # self.renderer = Renderer(self.render_mode, self._render)
        self.screen_width = 600
        self.screen_height = 400
        self.screen = None
        self.clock = None
        self.isopen = True
        self.state = None


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
        direction = 0
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


    def render(self, mode="human"):
        try:
            import pygame
            from pygame import gfxdraw
        except ImportError:
            raise DependencyNotInstalled(
                "pygame is not installed, run `pip install gym[classic_control]`"
            )

        if self.screen is None:
            pygame.init()
            if mode == "human":
                pygame.display.init()
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height)
                )
                pygame.display.set_caption('UAV Placer Environment')
            else:  # mode in {"rgb_array", "single_rgb_array"}
                self.screen = pygame.Surface((self.screen_width, self.screen_height))
        if self.clock is None:
            self.clock = pygame.time.Clock()

        x_scale = self.screen_width / 180.0
        y_scale = self.screen_width / 90.0
        font = pygame.font.SysFont('arial', 10)

        if self.state is None:
            return None

        uav_radius = 5
        uav_color = (0,0,255)
        uav_x, uav_y = self.state[0], self.state[1]
        uav_draw_x = int(uav_x * x_scale + self.screen_width / 2.0)
        uav_draw_y = int(uav_y * y_scale + self.screen_height / 2.0)

        self.surf = pygame.Surface((self.screen_width, self.screen_height))
        self.surf.fill((255, 255, 255))

        # Draw UAV
        gfxdraw.filled_circle(
            self.surf,
            uav_draw_x,
            uav_draw_y,
            uav_radius,
            uav_color,
        )

        # Draw hosts
        hosts = self.simulation.get_hosts()
        for host in hosts:
            host_size = 5
            host_color = (255,0,255)
            host_position = host.get_position()

            host_x, host_y = host_position['x'], host_position['y']
            host_draw_x = int(host_x * x_scale + self.screen_width / 2.0)
            host_draw_y = int(host_y * y_scale + self.screen_height / 2.0)

            left, right, top, bottom = -host_size / 2, host_size / 2, host_size / 2, -host_size / 2
            host_coords = [(left, bottom), (left, top), (right, top), (right, bottom)]
            host_coords = [(c[0] + host_draw_x, c[1] + host_draw_y) for c in host_coords]
            gfxdraw.filled_polygon(self.surf, host_coords, host_color)

            # text = font.render(f'Host{host.get_id()} lat:{host_y:.3f}, lon:{host_x:.3f}', True, (0,0,0), (255,255,255))
            # self.screen.blit(text, (host_draw_x - 5, self.screen_height - host_draw_y + 10))

        # Update screen
        self.surf = pygame.transform.flip(self.surf, False, True)
        self.screen.blit(self.surf, (0, 0))

        # Display UAV text
        text = font.render(f'UAV lat:{uav_y:.3f}, lon:{uav_x:.3f}', True, (0,0,0), (255,255,255))
        self.screen.blit(text, (uav_draw_x - 5, self.screen_height - uav_draw_y + 10))

        if mode == "human":
            pygame.event.pump()
            self.clock.tick(self.metadata["render_fps"])
            pygame.display.flip()

        elif mode in {"rgb_array", "single_rgb_array"}:
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
            )


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

    def close(self):
        if self.screen is not None:
            import pygame

            pygame.display.quit()
            pygame.quit()