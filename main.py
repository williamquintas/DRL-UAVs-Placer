import gym
import gym_envs
import utils.constants as const

env = gym.make('UAV-Placer-v0')

episodes = const.NUMBER_OF_EPISODES
for episode in range(episodes):
    state = env.reset()
    done = False
    score = 0

    while not done:
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        if const.RENDER_GRAPH:
            env.render(episode_number=episode+1)
        score += reward

    print(f'Episode: {episode+1} Score: {score}')