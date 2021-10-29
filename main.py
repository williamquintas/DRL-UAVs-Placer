import gym
import gym_envs
import json

env = gym.make('UAV-Placer-v0')

episodes = 100
for episode in range(episodes):
    state = env.reset()
    done = False
    score = 0

    while not done:
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)

        # TODO: implement rendering
        env.render()
        score += reward

    print(f'Episode: {episode+1} Score: {score}')