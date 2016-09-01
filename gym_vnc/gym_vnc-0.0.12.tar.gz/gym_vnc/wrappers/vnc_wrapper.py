import gym
from gym import spaces

class VNCWrapper(gym.Wrapper):
    def _configure(self, **kwargs):
        self.env.configure(**kwargs)

        # These are dynamically set
        self.metadata = self.env.metadata
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space

        self.safe_action_space = self.n = None
        if hasattr(self.env, 'safe_action_space'):
            self.safe_action_space = self.env.safe_action_space
        if hasattr(self.env, 'n'):
            self.n = self.env.n

        # TODO: it'd be nice for all wrappers to live below
        # Vectorized, but it's not easy to do this.
        self.vectorized = self.metadata.get('semantics.vectorized', False)

    def vectorized_map(self, func, data):
        if self.vectorized:
            return [func(item) for item in data]
        else:
            return func(data)

    def vectorized_repeat(self, action):
        if self.vectorized:
            return [action] * self.n
        else:
            return action

    def vectorized_tuple(self, space):
        if self.vectorized:
            return spaces.Tuple([space] * self.n)
        else:
            return space

    def vectorized_detuple(self, space):
        if self.vectorized:
            return space.spaces[0]
        else:
            return space
