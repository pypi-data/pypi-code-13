import gym

class VNCWrapper(gym.Wrapper):
    def _configure(self, **kwargs):
        self.env.configure(**kwargs)

        # These are dynamically set
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space
        self.safe_action_space = self.env.safe_action_space
        self.n = self.env.n
