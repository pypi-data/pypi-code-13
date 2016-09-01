import itertools
import gym
import logging
import os

from gym_vnc import pyprofile

from gym_vnc import error, remotes as remotes_module, rewarder, spaces, twisty, utils, vncdriver
from gym_vnc.envs import diagnostics

from gym_vnc.remotes import healthcheck

logger = logging.getLogger(__name__)

def go_vncdriver():
    import go_vncdriver
    go_vncdriver.setup()
    return go_vncdriver.VNCSession

def py_vncdriver():
    return vncdriver.VNCSession

def vnc_session(which=None):
    if which is None:
        which = os.environ.get('GYM_VNCDRIVER')

    if which == 'go':
        return go_vncdriver()
    elif which == 'py':
        return py_vncdriver()
    elif which is None:
        try:
            go = go_vncdriver()
            logger.info('Using golang VNC implementation')
            return go
        except ImportError:
            logger.info("Using pure Python vncdriver implementation. Run 'pip install go-vncdriver' to install the more performant Go implementation.")
            return py_vncdriver()
    else:
        raise error.Error('Invalid VNCSession driver: {}'.format(which))

def parse_remotes(remotes):
    vnc_addresses = []
    rewarder_addresses = []

    for remote in remotes:
        res = remote.split('+')
        if len(res) == 1:
            vnc_addresses.append(res[0])
        elif len(res) == 2:
            vnc_address, rewarder_address = res
            host, vnc_port = vnc_address.split(':')
            if ':' not in rewarder_address:
                # User only gave us a port
                rewarder_address = '{}:{}'.format(host, rewarder_address)
            vnc_addresses.append(vnc_address)
            rewarder_addresses.append(rewarder_address)
        else:
            raise error.Error('A remote spec must have zero or one commas: {}'.format(remote))
    if rewarder_addresses and len(vnc_addresses) != len(rewarder_addresses):
        raise error.Error('Either all or no VNC addresses must have rewarders: {}'.format(remotes))
    return vnc_addresses, rewarder_addresses

class VNCEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'configure.required': True,
        'semantics.async': True,
        'video.frames_per_second' : 60,
        'semantics.tags': ['vnc'],
        'semantics.vectorized': True,
    }

    docker_image = None
    docker_command = None

    def __init__(self):
        self.error_buffer = utils.ErrorBuffer()
        self._started = False

        self.observation_space = None
        self.action_space = None
        self.safe_action_space = None

        self._seed_value = None
        self._remotes_manager = None

    def _seed(self, seed):
        self._seed_value = seed

    def _configure(self, remotes=None, start_timeout=None):
        if self._started:
            raise error.Error('{} has already been started; cannot change configuration now.'.format(self))

        twisty.start_once()

        waited = False
        if isinstance(remotes, int):
            self._remotes_manager = remotes_module.Docker(image=self.docker_image, command=self.docker_command, n=remotes)
            self._remotes_manager.start()
            remotes = self._remotes_manager.connection_strings()
            waited = True
        elif remotes is None:
            remotes = os.environ.get('GYM_VNC_REMOTES')
            if remotes is None:
                raise error.Error("""No remotes provided.

(HINT: you can also set GYM_VNC_REMOTES to a comma separated list of VNC/rewarder pairs to connect to.

For example, you can run: export GYM_VNC_REMOTES=127.0.0.1:5900+15900,127.0.0.1:5901+15901.)""")

        if isinstance(remotes, str):
            remotes = remotes.split(',')

        vnc_addresses, rewarder_addresses = parse_remotes(remotes)

        self.remotes = remotes
        self.n = len(self.remotes)
        logger.info('Connecting to remotes: vnc_addresses=%s rewarder_addresses=%s', vnc_addresses, rewarder_addresses)

        if not waited:
            if start_timeout is None and self._remotes_manager is None:
                # Environments are being started externally, so
                # hardcode an arbitrary timeout for them to be
                # connectable at all.
                start_timeout = 2 * self.n + 5

            # Make sure we've healthchecked the remotes
            healthcheck.run(vnc_addresses, rewarder_addresses, start_timeout=start_timeout)

        cls = vnc_session()
        self.vnc_session = cls(vnc_addresses, self.error_buffer)
        if rewarder_addresses:
            self.rewarder_session = rewarder.RewarderSession(rewarder_addresses, self.error_buffer)
        else:
            self.rewarder_session = None

        self.observation_space = self._repeat_space(spaces.VNCObservationSpace())
        self.action_space = self._repeat_space(spaces.VNCActionSpace())
        self.safe_action_space = self.action_space

        if self.rewarder_session:
            self.diagnostics = diagnostics.Diagnostics()
            self.diagnostics.prepare(self.rewarder_session, self.n)
        else:
            self.diagnostics = None

    def _reset(self):
        self.error_buffer.check()

        if self.rewarder_session:
            response = self.rewarder_session.reset(
                seed=self._seed_value,
                env_id=self.spec.id,
                fps=self.metadata['video.frames_per_second'],
            )
            # Clear seed value so we don't double-send it
            self._seed_value = None
        observation_n, _ = self.vnc_session.flip()
        return observation_n

    def _compile_actions(self, action_n):
        try:
            return [[event.compile() for event in action] for action in action_n]
        except Exception as e:
            raise error.Error('Could not compile actions. Original error: {} ({}). action_n={}', e, type(e), action_n)

    def _step(self, action_n):
        self.error_buffer.check()

        action_n = self._compile_actions(action_n)
        if self.diagnostics:
            action_n = self.diagnostics.add_probe(action_n)

        observation_n, obs_info_n = self.vnc_session.step(action_n)

        if self.rewarder_session:
            reward_n, done_n, info_n = self.rewarder_session.pop()
        else:
            reward_n = done_n = [None] * len(observation_n)
            info_n = [{} for _ in range(len(observation_n))]

        if self.diagnostics:
            pyprofile.push('function.add_metadata')
            self.diagnostics.add_metadata(observation_n, info_n)
            pyprofile.pop()

        self._propagate_obs_info(info_n, obs_info_n)
        return observation_n, reward_n, done_n, {'n': info_n}

    def _propagate_obs_info(self, info_n, obs_info_n):
        for obs_info, info in itertools.izip(obs_info_n, info_n):
            info.setdefault('vnc.updates.n', 0)
            info['vnc.updates.n'] += obs_info['vnc.updates.n']

    def _render(self, mode='human', close=False):
        if close:
            return
        self.error_buffer.check()

        if mode == 'rgb_array':
            return self.vnc_session.peek()
        elif mode is 'human':
            self.vnc_session.render()

    def __str__(self):
        return 'VNCEnv<{}>'.format(self.spec.id)

    def _repeat_space(self, space):
        return utils.repeat_space(space, self.n)

    def _close(self):
        if self._remotes_manager:
            self._remotes_manager.close()
