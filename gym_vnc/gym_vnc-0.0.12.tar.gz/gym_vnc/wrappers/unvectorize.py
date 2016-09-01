from gym_vnc import error
from gym_vnc.wrappers import vnc_wrapper

class Unvectorize(vnc_wrapper.VNCWrapper):
    def _configure(self, vectorized=True, **kwargs):
        super(Unvectorize, self)._configure(**kwargs)
        self.vectorized = vectorized

        # Validate that the user isn't being silly
        if self.unwrapped.n != 1 and not self.vectorized:
            raise error.Error('Can only disable vectorization when passing 1 remote, not {}: {}'.format(self.unwrapped.n, self.unwrapped.remotes))

        if not self.vectorized:
            # Unvectorize the space!
            self.safe_action_space = self.safe_action_space.spaces[0]
            self.action_space = self.action_space.spaces[0]
            self.observation_space = self.observation_space.spaces[0]
            self.metadata = dict(self.metadata)
            self.metadata['semantics.vectorized'] = False

    def _reset(self):
        observation_n = self.env.reset()
        if not self.vectorized:
            return observation_n[0]

        return observation_n

    def _step(self, action_n):
        if not self.vectorized:
            action_n = [action_n]

        observation_n, reward_n, done_n, info = self.env.step(action_n)
        if not self.vectorized:
            return observation_n[0], reward_n[0], done_n[0], info['n'][0]

        return observation_n, reward_n, done_n, info

    def _render(self, mode='human', close=False):
        if mode == 'rgb_array' and not self.vectorized:
            rendered = self.env.render(mode=mode, close=close)
            return rendered[0]
        else:
            return self.env.render(mode=mode, close=close)
