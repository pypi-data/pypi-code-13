import logging
import threading

logger = logging.getLogger()

class EnvStatus(object):
    def __init__(self):
        self.cv = threading.Condition()
        self._env_id = None
        self._env_state = None
        self._metadata = {}

    def env_info(self):
        with self.cv:
            return {
                'env_state': self._env_state,
                'metadata': self._metadata,
                'env_id': self.env_id
            }

    def set_env_info(self, env_state, metadata=None, env_id=None):
        with self.cv:
            logger.info('Setting env_state: %s -> %s', self._env_state, env_state)
            self.cv.notifyAll()
            self._env_state = env_state
            self._metadata = metadata
            if env_id != None:
                self.env_id = env_id

    @property
    def env_state(self):
        with self.cv:
            return self._env_state

    @env_state.setter
    def env_state(self, value):
        # TODO: Validate env_state
        self.set_env_info(value)

    @property
    def env_id(self):
        with self.cv:
            return self._env_id

    @env_id.setter
    def env_id(self, value):
        with self.cv:
            self.cv.notifyAll()
            self._env_id = value

    def wait_for_env_state_change(self, start_state):
        with self.cv:
            while True:
                if self._env_state != start_state:
                    return self._env_state
                self.cv.wait(timeout=10)
