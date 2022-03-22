import gym
import gym_envs
from utils.constants import RENDER_GRAPH, NUMBER_OF_EPISODES

env = gym.make('UAV-Placer-v0')


def check_reward_and_repeat_action(first_reward, first_done, action):
    reward = first_reward
    done = first_done
    score = 0

    while (reward == 1 and not done):
        state, reward, done, info = env.step(action)
        score += reward
        if RENDER_GRAPH:
            env.render(episode_number=episode + 1)

    return score


episodes = NUMBER_OF_EPISODES
scores = []

for episode in range(episodes):
    state = env.reset()
    done = False
    score = 0

    while not done:
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        score += reward

        if RENDER_GRAPH:
            env.render(episode_number=episode + 1)

        score += check_reward_and_repeat_action(reward, done, action)

        # TODO: implement function to handle speed trying to improve reward and
        # score

    scores.append(score)
    print(f'Episode: {episode+1} Score: {score}')

print(f'Average score: {sum(scores)/len(scores)}')
