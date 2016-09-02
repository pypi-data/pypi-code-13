import json
import logging
import Queue

import itertools
import os

from gym_vnc import spaces
from twisted.internet import defer
from gym.envs.classic_control import rendering
from gym_vnc.vncdriver import fbs_reader, vnc_client, vnc_proxy_server

from gym_vnc import utils

logger = logging.getLogger(__name__)

class FakeTransport(object):
    def loseConnection(self):
        pass

    def write(self, data):
        pass

class ActionQueue(object):
    def __init__(self):
        self.actions = []
        self.pixel_format = []

    def key_event(self, key, down):
        event = spaces.KeyEvent(key, down)
        self.actions.append(event)

    def pointer_event(self, x, y, buttonmask):
        event = spaces.PointerEvent(x, y, buttonmask)
        self.actions.append(event)

    def set_pixel_format(self, server_pixel_format):
        self.pixel_format.append(server_pixel_format)

    def pop_all(self):
        output = self.actions, self.pixel_format
        self.actions = []
        self.pixel_format = []
        return output


class RewardReader(object):
    def __init__(self, reward_path, error_buffer):
        self.file = open(reward_path, 'r')

        meta = json.loads(self.file.readline())
        self.version = meta.get('version', 0)
        self._start_timestamp = meta['start_timestamp']

    def __iter__(self):
        return self

    def next(self):
        line = self.file.readline()
        if line == "":
            raise StopIteration()

        line = json.loads(line)
        timestamp = self._start_timestamp + float(line['time_delta'])
        reward = line['reward']
        info = line['info']
        if reward != 0.:
            pass

        done = line['done']
        return timestamp, reward, done, info


class ActionReader(object):
    def __init__(self, action_path, error_buffer):
        self.fbs_reader = iter(fbs_reader.FBSReader(action_path))
        self.action_queue = ActionQueue()
        self.error_buffer = error_buffer
        self.action_processor = vnc_proxy_server.VNCProxyServer(
            action_queue=self.action_queue,
            error_buffer=self.error_buffer)
        self.action_processor.transport = FakeTransport()

        self._advance()

    def __iter__(self):
        return self

    def _advance(self):
        self._data, self._timestamp = self.fbs_reader.next()

    def next(self):
        if self._timestamp is None:
            raise StopIteration

        action = []
        pixel_format = []

        eof = False
        while not (eof or action or pixel_format):
            # Keep cycling until we find something interesting to report

            timestamp = self._timestamp
            while self._timestamp == timestamp:
                assert self._data is not None
                # Advance to the time where this action happened
                self.action_processor.dataReceived(self._data)
                self.error_buffer.check()
                new_action, new_pixel_format = self.action_queue.pop_all()
                action += new_action
                pixel_format += new_pixel_format

                # Advance to the next action
                self._advance()
                if self._timestamp is None:
                    # End of the line. Might have some
                    # action/pixel_formats to return, so don't raise
                    # StopIteration here.
                    eof = True
                    break

        if not (action or pixel_format):
            raise StopIteration
        else:
            return timestamp, action, pixel_format


class Factory(object):
    def __init__(self, error_buffer):
        self.error_buffer = error_buffer
        self.deferred = None

class Playback(object):
    """
    Iterator that replays a VNCDemonstration event by event.
    Outputs a tuple of the following for each event that changed:

        timestamp, action, observation, reward, done, info
    """
    def __init__(self, logfile_dir, render=False):
        observation_path = os.path.join(logfile_dir, 'server.fbs')  # Timestamped log of server data.
        action_path = os.path.join(logfile_dir, 'client.fbs')  # Timestamped log of client data.
        reward_path = os.path.join(logfile_dir, 'rewards.demo')  # Timestamped json dump of rewards data.

        self.error_buffer = utils.ErrorBuffer()
        self.observation_processor = vnc_client.VNCClient()
        self.observation_processor.factory = Factory(self.error_buffer)
        self.observation_processor.transport = FakeTransport()

        self.action_reader = ActionReader(action_path, self.error_buffer)
        self.reward_reader = RewardReader(reward_path, self.error_buffer)
        self.observation_reader = iter(fbs_reader.FBSReader(observation_path))

        self._next_action()
        self._next_observation()
        self._next_reward()

        self._render = render

        self.viewer = None

    def render(self, close=False):
        if close and self.viewer is not None:
            self.viewer.close()
            self.viewer = None
            return

        if self.viewer is None:
            self.viewer = rendering.SimpleImageViewer()

        if self.observation_processor.numpy_screen is None:
            return

        observation = self.observation_processor.numpy_screen.peek()
        self.viewer.imshow(observation)

    def _next_action(self):
        self.action_timestamp, self.action, self.pixel_format = self.action_reader.next()

    def _next_observation(self):
        try:
            self.observation_data, self.observation_timestamp = self.observation_reader.next()
        except StopIteration:
            self.observation_data = self.observation_timestamp = None

    def _next_reward(self):
        self.reward_timestamp, self.reward, self.done, self.info = self.reward_reader.next()

    def __iter__(self):
        return self

    def next(self):
        if self.action_timestamp is None and self.observation_timestamp is None:
            raise StopIteration()

        action = []
        reward = 0.
        done = False
        info = []
        pixel_format = []

        # See which file is currently limiting our playback
        timestamp = min(self.action_timestamp,
                        self.observation_timestamp,
                        self.reward_timestamp,
                        )

        # Pull in actions until they are no longer limiting
        while self.action_timestamp == timestamp:
            # This action is now in effect!
            self.error_buffer.check()
            action += self.action
            pixel_format += self.pixel_format

            # Advance to the next action
            self._next_action()

        # Any SetPixelFormat messages have now come into effect.
        for format in pixel_format:
            assert self.observation_processor.framebuffer
            assert len(format) == 16, "Bad length {} for pixel format: {}".format(len(format), format)
            self.observation_processor.framebuffer.apply_format(format)

        # Pull in observations until they are no longer limiting
        while self.observation_timestamp == timestamp:
            self.observation_processor.dataReceived(self.observation_data)
            self.error_buffer.check()

            # Advance to the next observation
            self._next_observation()

        if self.observation_processor.numpy_screen is not None:
            observation = self.observation_processor.numpy_screen.flip()
        else:
            observation = None

        # Pull in rewards until they are no longer limiting
        while self.reward_timestamp == timestamp:
            self._next_reward()
            reward += self.reward
            done = done or self.done  # Return done if we got any done responses in this timestamp
            info = self.info  # If multiple rewards in the same timestamp, take the last one

        logger.debug('''Current timestamps:
    observation_timestamp=%s
         action_timestamp=%s
         reward_timestamp=%s''',
                    self.observation_timestamp,
                    self.action_timestamp,
                    self.reward_timestamp,
                    )
        if self._render:
            self.render()

        return timestamp, action, observation, reward, done, info

    def close(self):
        self.render(close=True)
        self.file.close()
