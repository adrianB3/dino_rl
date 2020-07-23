from env_interface import EnvironmentBase


class DinoEnv(EnvironmentBase):

    def __init__(self, observation_space, action_space):
        super().__init__(observation_space, action_space)

    def render(self):
        pass

    def step(self, action):
        pass

    def reset(self):
        pass
