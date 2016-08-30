# -*- coding: utf-8 -*-

import itertools
import logging
import numpy as np
import time

from gym_vnc import spaces

logger = logging.getLogger(__name__)

def show(ob):
    from PIL import Image
    Image.fromarray(ob).show()

def standard_error(ary, axis, scale=1):
    ary = np.array(ary) * scale
    if len(ary) > 1:
        return np.std(ary, axis=axis) / np.sqrt(len(ary) - 1)
    else:
        return np.std(ary, axis=axis)

def extract_timestamp(observation):
    total = 0
    for byte in observation[0]:
        total = 256 * total + byte
    for byte in observation[1]:
        total = 256 * total + byte

    timestamp = total/1000.
    return timestamp

class Diagnostics(object):
    def __init__(self):
        self.instance_n = None

    def prepare(self, rewarder_session, n):
        self.network = Network(rewarder_session, n)
        self.instance_n = [DiagnosticsInstance(i, self.network) for i in range(n)]

    def add_probe(self, action_n):
        return [instance.add_probe(action) for instance, action in zip(self.instance_n, action_n)]

    def add_metadata(self, observation_n, info_n):
        """Mutates the info_n dictionary."""
        if self.instance_n is None:
            return

        for instance, observation, info in zip(self.instance_n, observation_n, info_n):
            instance.add_metadata(observation, info)

    def extract_metadata(self, observation_n):
        return [instance._extract_metadata(observation)
                for instance, observation in zip(self.instance_n, observation_n)]


class DiagnosticsInstance(object):
    anchor = np.array([
        [(0x12, 0x34, 0x56), (0x78, 0x90, 0xab)],
        [(0x23, 0x45, 0x67), (0x89, 0x0a, 0xbc)],
    ], dtype=np.uint8)

    def __init__(self, i, network):
        self.i = i
        self.network = network

        self.probe_sent_at = None # local time
        self.probe_received_at = None # remote time
        self.action_latency_skewed = None
        self.probe = [
            spaces.KeyEvent(0xbeef1, down=True).compile(),
            spaces.KeyEvent(0xbeef1, down=False).compile(),
        ]
        self.metadata_location = None
        self.last_search_metadata = 0
        self.search_metadata_frequency = 1

    def add_probe(self, action):
        if self.probe_sent_at is None:
            logger.debug('[%d] Sending out new probe', self.i)
            self.probe_sent_at = time.time()
            action = action + self.probe
        return action

    def add_metadata(self, observation, info):
        metadata = self._extract_metadata(observation)
        if not metadata:
            return

        now = metadata['now']
        probe_received_at = metadata['probe_received_at']

        if self.probe_received_at is None: # this also would work for the equality case
            self.probe_received_at = probe_received_at
        elif self.probe_received_at != probe_received_at:
            logger.debug('[%d] Next probe received: old=%s new=%s', self.i, self.probe_received_at, probe_received_at)
            assert self.probe_sent_at is not None

            self.probe_received_at = probe_received_at
            # Subtract the *local* time we sent it from the *remote* time it was received
            self.action_latency_skewed = probe_received_at - self.probe_sent_at
            self.probe_sent_at = None

        info['diagnostics.clock_skew'] = self.network.clock_skew_n[self.i]
        # Subtract *local* time it was received from the *remote* time
        # displayed. Negate to fix time ordering.
        info['diagnostics.lag.observation'] = -(now - time.time() + self.network.reversed_clock_skew_n[self.i])

        if self.action_latency_skewed:
            action_lag = self.action_latency_skewed + self.network.reversed_clock_skew_n[self.i]
        else:
            action_lag = None
        info['diagnostics.lag.action'] = action_lag

    def _extract_metadata(self, observation):
        self._search_metadata_location(observation)
        if not self.metadata_location:
            return

        y, x = self.metadata_location

        return {
            # Timestamp on the image
            'now': extract_timestamp(observation[y, x+2:x+4]),
            # When the last probe was received
            'probe_received_at': extract_timestamp(observation[y, x+4:x+6])
        }

    def _search_metadata_location(self, observation):
        """Mutating: ensure we're calibrated on the right metadata location"""
        # Check to make sure the metadata box didn't move
        if self.metadata_location and \
           not self._check_location(observation, self.metadata_location):
            logger.debug('[%d] Metadata location is no longer valid', self.i)
            self.metadata_location = None

        # Try to find the metadata box, every self.search_metadata_frequency
        if not self.metadata_location and \
           time.time() - self.last_search_metadata > self.search_metadata_frequency:
            self.metadata_location = self._find_metadata_location(observation)
            if self.metadata_location:
                self.last_search_metadata = 0
            else:
                self.last_search_metadata = time.time()

    def _find_metadata_location(self, observation):
        """Non-mutating"""
        ys, xs = np.where(np.all(observation == self.anchor[0, 0], axis=-1))
        if len(ys) == 0:
            logger.info('[%d] Could not find metadata anchor pixels', self.i)
            return False

        # TODO: handle multiple hits
        assert len(ys) == 1
        location = (ys[0], xs[0])

        if not self._check_location(observation, location):
            # This can happen when someone mouses over the pixels,
            # partly occluding the box.
            return False

        logger.info('[%d] Found metadata anchor pixels: %s', self.i, location)
        return location

    def _check_location(self, observation, location):
        """Non-mutating"""
        y, x = location
        return np.all(observation[y:y+2, x:x+2] == self.anchor)

class Network(object):
    def __init__(self, rewarder_session, n):
        self.n = n
        self.connection_samples = 10
        self.application_ping_samples = 10

        connection_times_nm = self._measure_connection_time(rewarder_session)
        clock_skew_nm, request_overhead_nm, response_overhead_nm, application_rtt_nm = self._measure_application_ping(rewarder_session)

        self._report(connection_times_nm, clock_skew_nm, request_overhead_nm, response_overhead_nm, application_rtt_nm)

        # We only need to remember the clock skew
        self.clock_skew_n = clock_skew_nm.mean(axis=1) # add to local time to get remote time, as (min, max) values
        self.reversed_clock_skew_n = -self.clock_skew_n[:, [1, 0]] # add to remote time to get local time, in format (min, max)

    def _measure_connection_time(self, rewarder_session):
        connection_times = np.zeros((self.n, self.connection_samples))

        for i in range(self.connection_samples):
            connection_time_n = rewarder_session.connection_time()
            connection_times[:, i] = connection_time_n

        return connection_times

    def _measure_application_ping(self, rewarder_session):
        clock_skew = np.zeros((self.n, self.application_ping_samples, 2))
        request_overhead = np.zeros((self.n, self.application_ping_samples))
        response_overhead = np.zeros((self.n, self.application_ping_samples))
        application_rtt = np.zeros((self.n, self.application_ping_samples))

        for j in range(self.application_ping_samples):
            start = time.time()
            responses = rewarder_session.ping()
            end = time.time()

            for i, (context, request, response) in enumerate(responses):
                request_sent_at = request['headers']['sent_at'] # local
                response_sent_at = response['headers']['sent_at'] # remote
                response_received_at = context['start'] # local

                # We try to put bounds on clock skew by subtracting
                # local and remote times, for local and remote events
                # that are causally related.
                #
                # For example, suppose that the following local/remote
                # logical timestamps apply to a request (for a system
                # with clock skew of 100):
                #
                # request_sent       local: 0   remote: 100
                # request_recieved   local: 1   remote: 101
                # response_sent      local: 2   remote: 102
                # response_received  local: 3   remote: 103
                #
                # Then:
                #
                # # Remote event *after* local is upper bound
                # request_recieved.remote - request_sent.local = 101
                # # Remote event *before* local is lower bound
                # response_sent.remote - response_received.local = 102 - 3 = 99
                #
                # There's danger of further clock drift over time, but
                # we don't need these to be fully accurate, and this
                # should be fine for now.
                clock_skew[i, j, :] = (response_sent_at-response_received_at, response_sent_at-request_sent_at)
                request_overhead[i, j] = request_sent_at - start
                response_overhead[i, j] = end - response_received_at
                application_rtt[i, j] = response_received_at - request_sent_at
        return clock_skew, request_overhead, response_overhead, application_rtt

    def _report(self, connection_time_nm, clock_skew_nm, request_overhead_nm, response_overhead_nm, application_rtt_nm):
        logger.info('\n\n')
        logger.info('Please include network calibration in any slowness-related bug reports.')
        for i, (connection_time_m, clock_skew_m, request_overhead_m, response_overhead_m, application_rtt_m) in enumerate(zip(connection_time_nm, clock_skew_nm, request_overhead_nm, response_overhead_nm, application_rtt_nm)):
            connection_time = display_timestamps(connection_time_m)
            clock_skew = display_timestamps_pair(clock_skew_m)
            application_rtt = display_timestamps(application_rtt_m)
            request_overhead = display_timestamps(request_overhead_m)
            response_overhead = display_timestamps(response_overhead_m)

            logger.info('[%d] Network calibration: clock_skew=%s connection_time=%s application_rtt=%s request_overhead=%s response_overhead=%s',
                        i, clock_skew, connection_time, application_rtt,
                        request_overhead, response_overhead)
        logger.info('\n\n')

def extract_timestamp(observation):
    total = 0
    for byte in observation[0]:
        total = 256 * total + byte
    for byte in observation[1]:
        total = 256 * total + byte

    timestamp = total/1000.
    return timestamp

def display_timestamps_pair_max(time_m_2):
    # We concatenate the (min, max) lags from a variety of runs. Those
    # runs may have different lengths.
    time_m_2 = np.concatenate(time_m_2)

    if len(time_m_2) == 0:
        return '(empty)'

    return display_timestamps_sigma(time_m_2[:, 1])

def display_timestamps_pair_compact(time_m_2):
    """Takes a list of the following form: [(a1, b1), (a2, b2), ...] and
    returns a string a_mean-b_mean, flooring out at 0.
    """
    if len(time_m_2) == 0:
        return '(empty)'

    time_m_2 = np.array(time_m_2)

    low = time_m_2[:, 0].mean()
    high = time_m_2[:, 1].mean()

    low = max(low, 0)

    # Not sure if this'll always be true, and not worth crashing over
    if high < 0:
        logger.warn('Harmless warning: upper-bound on clock skew is negative: (%s, %s). Please let Greg know about this.', low, high)

    return '{}-{}'.format(display_timestamp(low), display_timestamp(high))

def display_timestamps_pair(time_m_2):
    """Takes a list of the following form: [(a1, b1), (a2, b2), ...] and
    returns a string (a_mean+/-a_error, b_mean+/-b_error).
    """
    if len(time_m_2) == 0:
        return '(empty)'

    time_m_2 = np.array(time_m_2)
    return '({}, {})'.format(
        display_timestamps(time_m_2[:, 0]),
        display_timestamps(time_m_2[:, 1]),
    )

def display_timestamps_sigma(time_m):
    mean = np.mean(time_m)
    std = standard_error(time_m)
    scale, units = pick_time_units(mean)
    return '{:.2f}{} σ={:.2f}{}'.format(mean * scale, units, std * scale, units)

def display_timestamps(time_m):
    mean = np.mean(time_m)
    std = standard_error(time_m)
    return '{}±{}'.format(display_timestamp(mean), display_timestamp(std))

def standard_error(ary, axis=0):
    if len(ary) > 1:
        return np.std(ary, axis=axis) / np.sqrt(len(ary) - 1)
    else:
        return np.std(ary, axis=axis)

def display_timestamp(time):
    assert not isinstance(time, np.ndarray), 'Invalid scalar: {}'.format(time)
    scale, units = pick_time_units(time)
    return '{:.2f}{}'.format(time * scale, units)

def pick_time_units(time):
    assert not isinstance(time, np.ndarray), 'Invalid scalar: {}'.format(time)
    if abs(time) < 1:
        return 1000, 'ms'
    else:
        return 1, 's'
