import sys
sys.path.append('/Users/william/Documents/drl-uavs-placer')

import gym, gym_envs

env = gym.make('UAV-Placer-v0', render_mode="human")

obs = env.reset()

n_steps = 1
for step in range(n_steps):
  print("Step {}".format(step + 1))
  action = env.action_space.sample()
  print("Action {}".format(action))

  obs, reward, done, info = env.step(action)
  env.render()

  while True:
    pass

  print('obs=', obs, 'reward=', reward, 'done=', done, 'info=', info)

  if done:
    print("Goal reached!", "reward=", reward)
    break
