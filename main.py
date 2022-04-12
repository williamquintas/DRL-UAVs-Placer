# pylint: disable=unused-import
# pylint: disable=invalid-name
import gym
import gym_envs
from utils.constants import RENDER_GRAPH, NUMBER_OF_EPISODES


def check_reward_and_repeat_action(first_reward, first_done, current_action):
    _reward = first_reward
    _done = first_done
    _score = 0

    while (_reward == 1 and not _done):
        _, _reward, _done, __ = env.step(current_action)
        _score += _reward
        if RENDER_GRAPH:
            env.render(episode_number=episode + 1)

    return _score


if __name__ == '__main__':
    env = gym.make('UAV-Placer-v0')
    scores = []

    for episode in range(NUMBER_OF_EPISODES):
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
        scores.append(score)
        print(f'Episode: {episode+1} Score: {score}')

    print(f'Average score: {sum(scores)/len(scores)}')
