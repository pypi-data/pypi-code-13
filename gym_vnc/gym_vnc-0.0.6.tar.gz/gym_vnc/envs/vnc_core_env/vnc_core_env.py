import gym
import itertools
import logging
import numpy as np
from gym_vnc import pyprofile
import time

from gym_vnc import spaces, utils
from gym_vnc.envs import vnc_env

logger = logging.getLogger(__name__)

def vnc_action(up=False, down=False, left=False, right=False, z=False):
    return [spaces.KeyEvent.by_name('up', down=up),
            spaces.KeyEvent.by_name('left', down=left),
            spaces.KeyEvent.by_name('right', down=right),
            spaces.KeyEvent.by_name('down', down=down),
            spaces.KeyEvent.by_name('z', down=z)]

class VNCCoreEnv(vnc_env.VNCEnv):
    docker_image = 'quay.io/openai/vnc-core-envs@sha256:e0b7fe6bf0c5fb673696dafeb6972d880663f504a82f452b61efd4268bbe4cca'
    docker_command = ['run', '-o']

    def __init__(self, core_env_id, fps=60):
        super(VNCCoreEnv, self).__init__()

        self.metadata = dict(self.metadata)
        self.metadata['video.frames_per_second'] = fps

        self.core_env_id = core_env_id
        self._seed_value = None

        self.vnc_pixels = True

    def _configure(self, *args, **kwargs):
        super(VNCCoreEnv, self)._configure(*args, **kwargs)

        if self.core_env_id == 'CartPole-v0':
            self.safe_action_space = self._repeat_space(
                spaces.Hardcoded([
                    [spaces.KeyEvent.by_name('left', down=True)],
                    [spaces.KeyEvent.by_name('left', down=False)],
                ])
            )
        else:
            actions = []
            env = gym.spec(self.core_env_id).make()
            for action in env.unwrapped.get_action_meanings():
                z = 'FIRE' in action
                left = 'LEFT' in action
                right = 'RIGHT' in action
                up = 'UP' in action
                down = 'DOWN' in action
                translated = vnc_action(up=up, down=down, left=left, right=right, z=z)
                actions.append(translated)
            self.safe_action_space = self._repeat_space(spaces.Hardcoded(actions))

    def _seed(self, seed):
        self._seed_value = seed

class VNCCoreSyncEnv(VNCCoreEnv):
    """A synchronized version of the core envs. Its semantics should match
    that of the core envs. (By default, observations are pixels from
    the VNC session, but it also supports receiving the normal Gym
    observations over the rewarder socket.)

    Provided primarily for testing and debugging.
    """

    def __init__(self, core_env_id, fps=60, vnc_pixels=True):
        super(VNCCoreSyncEnv, self).__init__(core_env_id, fps=fps)
        # Metadata has already been cloned
        self.metadata['semantics.async'] = False

        self.core_env_id = core_env_id
        self.vnc_pixels = vnc_pixels

        if not vnc_pixels:
            self._core_env = gym.spec(core_env_id).make()
        else:
            self._core_env = None

    def _flip_past(self, when_n):
        info_n = [{} for i in range(self.n)]
        while True:
            observation_n, obs_info_n = self.vnc_session.flip()
            metadata_n = self.diagnostics.extract_metadata(observation_n)

            # Save the update count
            self._propagate_obs_info(info_n, obs_info_n)

            # All remote times, so no clock skew adjustments needed
            invalid = []
            for i, (metadata, when) in enumerate(itertools.izip(metadata_n, when_n)):
                delta = when - metadata.get('now', 0)
                if delta > 0:
                    invalid.append((i, delta))
            if not invalid:
                break
            else:
                tick = 1./self.metadata['video.frames_per_second']
                logger.info('Waiting %sms for the following observations to catch up: %s', int(1000*tick), invalid)
                time.sleep(tick)
        return observation_n, info_n

    def _reset(self):
        self.error_buffer.check()
        assert self.rewarder_session

        result = self.rewarder_session.reset(
            seed=self._seed_value,
            env_id=self.spec.id,
            fps=self.metadata['video.frames_per_second'],
        )
        # Clear seed value so we don't double-send it
        self._seed_value = None

        # Wait until all the observations have passed the reset_time
        remote_reset_time = [response['headers']['sent_at'] for _, _, response in result]
        observation_n, _ = self._flip_past(remote_reset_time)

        # Double check that our reward queue is empty
        assert all(c == 0 for c in self.rewarder_session.rewards_count())

        return self._observation(observation_n)

    def _observation(self, observation_n):
        if self.vnc_pixels:
            return observation_n
        else:
            observation_n = self.rewarder_session.pop_observation()
            assert all(observation is not None for observation in observation_n), 'At least one missing observation: {}'.format(observation_n)
            return self._core_env.observation_space.from_jsonable(observation_n)

    def _step(self, action_n):
        self.error_buffer.check()

        # Add C keypress in order to "commit" the action, as
        # interpreted by the remote.
        action_n = [action + [
            spaces.KeyEvent.by_name('c', down=True),
            spaces.KeyEvent.by_name('c', down=False)
        ] for action in action_n]
        # Submit directly to VNC session, without popping rewards
        logger.debug('Submitting actions: %s', action_n)
        action_n = self._compile_actions(action_n)
        _, obs_info_n = self.vnc_session.step(action_n)
        # Wait until the actions have actually happened
        self.rewarder_session.wait(timeout=5)

        when = self.rewarder_session.rewards_remote_time()
        observation_n, obs_info_n = self._flip_past(when)

        reward_n, done_n, info_n = self.rewarder_session.pop()
        self._propagate_obs_info(info_n, obs_info_n)

        # Warn if we detect multiple rewards
        if any(info['reward.count'] != 1 for info in info_n):
            # Arrived but there was a bug
            logger.warn('Likely bug: should have received 1 reward for every env, but instead received %s. Current return: observation=%s reward=%s done=%s info=%s', [info['reward.count'] for info in info_n], observation_n, reward_n, done_n, info_n)

        return self._observation(observation_n), reward_n, done_n, info_n
