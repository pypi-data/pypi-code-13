import logging
import gym
from gym import spaces
from gym_vnc.wrappers import vnc_wrapper
import time

logger = logging.getLogger(__name__)

ATARI_HEIGHT = 210
ATARI_WIDTH = 160

def _crop_frame(obs):
    return obs[:ATARI_HEIGHT, :ATARI_WIDTH, :]

class CropAtari(vnc_wrapper.VNCWrapper):
    def _configure(self, **kwargs):
        super(CropAtari, self)._configure(**kwargs)
        self.observation_space = self.tuple(spaces.Box(ATARI_HEIGHT, ATARI_WIDTH, 3))

    def _step(self, action):
        observation, reward, done, info = self.env.step(action)
        return _crop_frame(observation), reward, done, info

    def _reset(self):
        observation = self.env.reset()
        return _crop_frame(observation)

class Throttle(vnc_wrapper.VNCWrapper):
    def __init__(self, env, fps=None):
        super(Throttle, self).__init__(env)

        if fps is None:
            fps = self.metadata['video.frames_per_second']
        self.env = env
        self.target = None
        self.fps = fps

    def _reset(self):
        observation = self.env.reset()
        self.target = time.time()
        return observation

    def _step(self, action):
        self.target += 1./self.fps
        delta = self.target - time.time()
        if delta > 0:
            time.sleep(delta)
        else:
            logger.debug('Fell behind by %ss', -delta)
            self.target = time.time()
        return self.env.step(action)

class DiscreteToVNCAction(vnc_wrapper.VNCWrapper):
    def _configure(self, **kwargs):
        super(DiscreteToVNCAction, self)._configure(**kwargs)
        real_action_space = self.detuple(self.env.safe_action_space)
        self._actions = real_action_space.actions

        action_space = spaces.Discrete(len(self._actions))
        self.action_space = self.tuple(action_space)
        self.safe_action_space = action_space

    def _step(self, action_n):
        if self.vectorized:
            action_n = [self._actions[action] for action in action_n]
        else:
            action_n = self._actions[action_n]
        return self.env.step(action_n)

# def wrap(env):
#     return DiscreteToVNCAction(CropAtari(Throttle(env)))
