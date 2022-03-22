from gym.envs.registration import register

register(
    id='UAV-Placer-v0',
    entry_point='gym_envs.envs:UAVPlacerEnv',
    max_episode_steps=2000,
)
