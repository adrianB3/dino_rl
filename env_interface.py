import abc


class EnvironmentBase(abc.ABC):
    """
    Environment base interface - used for defining a common way to access
    multiple environments. Concrete class must implement the abstract methods.
    """
    def __init__(self, observation_space, action_space):
        self.observation_space = observation_space
        self.observation_space = action_space

    @abc.abstractmethod
    def render(self):
        pass

    @abc.abstractmethod
    def step(self, action):
        """
        Executes an action in the environment
        Input: the action to take
        :return: observation, reward, done, info
        """
        pass

    @abc.abstractmethod
    def reset(self):
        """
        Resets the environment
        :return: observation
        """
        pass

    def close(self):
        pass
