import logging
import gym
from gym import spaces
from gym_vnc.wrappers import vnc_wrapper

ATARI_HEIGHT = 210
ATARI_WIDTH = 160

def _crop_frame(obs):
    return obs[:ATARI_HEIGHT, :ATARI_WIDTH, :]

class CropAtari(vnc_wrapper.VNCWrapper):
    def _configure(self, **kwargs):
        super(CropAtari, self)._configure(**kwargs)
        self.observation_space = spaces.Box(ATARI_HEIGHT, ATARI_WIDTH, 3)

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

    def reset(self):
        observation = self.env.reset()
        self.target = time.time()
        return observation

    def step(self, action):
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
        self.action_space = spaces.Discrete(len(self.env.safe_action_space.spaces[0].actions))
        self.safe_action_space = self.action_space
        self.actions = self.env.safe_action_space.spaces[0].actions

    def _step(self, action_n):
        action_n = [actions[action] for action in action_n]
        return self._step(action_n)

def wrap(env):
    return DiscreteToVNCAction(CropAtari(Throttle(env)))
