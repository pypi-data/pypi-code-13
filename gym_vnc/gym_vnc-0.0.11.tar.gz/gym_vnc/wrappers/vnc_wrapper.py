import gym
from gym import spaces

class VNCWrapper(gym.Wrapper):
    def _configure(self, **kwargs):
        self.env.configure(**kwargs)

        # These are dynamically set
        self.metadata = self.env.metadata
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space
        self.safe_action_space = self.env.safe_action_space
        self.n = self.env.n

        # TODO: it'd be nice for all wrappers to live below
        # Vectorized, but it's not easy to do this.
        self.vectorized = self.metadata['semantics.vectorized']

    def tuple(self, space):
        if self.vectorized:
            return spaces.Tuple([space] * self.n)
        else:
            return space

    def detuple(self, space):
        if self.vectorized:
            return space.spaces[0]
        else:
            return space
