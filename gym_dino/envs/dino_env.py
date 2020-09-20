import gym
import pygame
from gym import error, spaces, utils
from gym.utils import seeding

from gym_dino.envs.dino_game import DinoGame
from gym_dino.envs.dino_cfg import width, height


class DinoEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.env = DinoGame()
        self.observation_space = spaces.Box(0, 255, [height, width, 3])
        self.action_space = spaces.Discrete(2)

    def step(self, action):
        self.env.step(action)
        observation, reward, done = self.env.get_current_state()

        return observation, reward, done, ""

    def reset(self):
        self.env.draw()
        self.env.reset()
        obs, reward, done = self.env.get_current_state()

        return obs

    def render(self, mode='human'):
        self.env.draw()

    def close(self):
        pygame.quit()
        quit()
