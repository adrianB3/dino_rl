import gym
from gym import error, spaces, utils
from gym.utils import seeding

from gym_dino.envs.dino_game import DinoGame


class DinoEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.env = DinoGame()
        self.observation_space = spaces.tuple
        self.action_space = spaces.Discrete(3)

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode='human'):
        pass

    def close(self):
        pass
