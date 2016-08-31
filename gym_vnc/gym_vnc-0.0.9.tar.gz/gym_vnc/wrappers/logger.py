import logging
import time

from gym_vnc.envs import diagnostics
from gym_vnc.wrappers import vnc_wrapper

logger = logging.getLogger(__name__)

class Logger(vnc_wrapper.VNCWrapper):
    def __init__(self, env):
        super(Logger, self).__init__(env)

    def _configure(self, print_frequency=5, **kwargs):
        self.print_frequency = print_frequency
        logger.info('Running VNC environments with Logger set to print_frequency=%s. To change this, pass "print_frequency=k" or "print_frequency=None" to "env.configure".', self.print_frequency)

        super(Logger, self)._configure(**kwargs)
        self._clear_step_state()

    def _clear_step_state(self):
        self.frames = 0
        self.last_print = time.time()
        self.observation_lag_n = [[] for _ in range(self.unwrapped.n)]
        self.action_lag_n = [[] for _ in range(self.unwrapped.n)]

    def _step(self, action_n):
        observation_n, reward_n, done_n, info_n = self.env.step(action_n)
        if self.print_frequency is None:
            return observation_n, reward_n, done_n, info_n

        # Printing
        self.frames += 1
        delta = time.time() - self.last_print
        if delta > self.print_frequency:
            fps = int(self.frames/delta)

            # Displayed independently
            # action_lag = ','.join([diagnostics.display_timestamps_pair_max(action_lag) for action_lag in self.action_lag_n])
            # observation_lag = ','.join([diagnostics.display_timestamps_pair_max(observation_lag) for observation_lag in self.observation_lag_n])

            # Smooshed together
            action_lag = diagnostics.display_timestamps_pair_max(self.action_lag_n)
            observation_lag = diagnostics.display_timestamps_pair_max(self.observation_lag_n)

            logger.info('Stats for the past %ss: action_lag=%s observation_lag=%s fps=%s',
                        self.print_frequency, action_lag, observation_lag, fps)

            self._clear_step_state()

        # Saving of lags
        for i, info in enumerate(info_n['n']):
            observation_lag = info.get('diagnostics.lag.observation')
            if observation_lag is not None:
                self.observation_lag_n[i].append(observation_lag)

            action_lag = info.get('diagnostics.lag.action')
            if action_lag is not None:
                self.action_lag_n[i].append(action_lag)

        return observation_n, reward_n, done_n, info_n
