import gym
from PIL import Image
from gym_dino.envs.dino_cfg import width, height

env = gym.make('gym_dino:dino-v0')

for _ in range(20):
    observation = env.reset()
    for t in range(1000):
        env.render()
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        img = Image.frombytes('RGB', (width, height), observation)
        if done:
            print("Episode finished after {} timesteps. Ep. reward: {}".format(t + 1, reward))
            break
env.close()
