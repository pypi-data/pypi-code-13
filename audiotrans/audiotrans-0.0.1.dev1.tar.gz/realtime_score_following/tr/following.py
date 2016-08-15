# -*- coding: utf-8 -*-

import os
import json
from collections import OrderedDict
import numpy as np
from hmmlearn import hmm
from logging import getLogger, StreamHandler, Formatter, DEBUG

logger = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(Formatter('[%(asctime)s %(levelname)s %(module)s] %(message)s'))
logger.addHandler(handler)


class FollowingTransform():
    """
    Transform module for pattern recognition of observations and following current positions.

    Parameteres
    ----

    keyword arguments
    ````

    patterns_filepath : string
        Filepath for learning data.
        Contents must be formed JSON, contains only one array of observations.

    scenes_filepath : string
        Filepath for definition of scenes.
        Contents must be formed JSON, contains only one object expressing
        time as keys and name of scene as values.
    """

    def __init__(self, bufsize, framerate, channels, verbose=False, *args, **kwargs):
        self.bufsize = bufsize
        self.framerate = framerate
        self.channels = channels
        if verbose:
            logger.setLevel(DEBUG)
            handler.setLevel(DEBUG)

        patterns_filepath = kwargs.get('patterns_filepath', None)
        if patterns_filepath is None:
            raise ValueError('"--patterns_filepath" option is required')
        if not os.path.isfile(patterns_filepath):
            raise IOError('patterns file not found in "{}"'.format(patterns_filepath))
        p = json.load(open(patterns_filepath, 'r'))
        p = OrderedDict(sorted(p.items(), key=lambda k: int(k[0])))  # sorted by keys as int
        self.pattern_times = np.array(list(p.keys())).astype(float)
        self.pattern_obsvs = np.array(list(p.values())).astype(float)

        scenes_filepath = kwargs.get('scenes_filepath', None)
        if scenes_filepath is None:
            self.scenes = {}
        elif not os.path.isfile(scenes_filepath):
            raise IOError('scenes file not found in "{}"'.format(patterns_filepath))
        else:
            self.scenes = json.load(open(scenes_filepath, 'r'))
        self.scene_time_keys = np.sort(np.array(list(self.scenes.keys())).astype(int))

        self.stored_obsvs = np.array([])
        self.p_state = None
        self.p_scene_time = None
        self.p_time = None

        logger.debug('try to create HMM with {}-array means of observations'
                     .format(len(self.pattern_times)))
        self.model = _create_model(self.pattern_obsvs, 0.01)

        logger.info('created HMM')

    def transform(self, obsvs):
        """
        Transform observations to current predicated state

        Parameteres
        ----
        obsvs : array
            array of observations

        Returns
        ----
        current predicted state
        """

        if len(obsvs) > 0:
            self.stored_obsvs = np.append(self.stored_obsvs, obsvs)
            logger.info('store new observations {}'.format(obsvs))

            if len(self.stored_obsvs) > 1:
                logger.debug('try to decode states with HMM by observations...')

                _, pred = self.model.decode(self.stored_obsvs.reshape(-1, 1))
                logger.info('predicted transition of states: {}'.format(pred))

                self.p_state = pred[-1]
                logger.info('updated prediction of current state: {}'.format(self.p_state))

                self.p_time = self.pattern_times[self.p_state]
                logger.info('updated prediction of current time: {}'.format(self.p_time))

        # terminate when no predictables
        if self.p_time is None or self.p_state is None:
            logger.info('no predictable items now')
            return []

        if len(self.scene_time_keys) > 0:
            p_scene_time = self.scene_time_keys[self.scene_time_keys < self.p_time].max()
            if self.p_scene_time != p_scene_time:
                self.p_scene_time = p_scene_time
                logger.info('predicted new scene: {} {}'
                            .format(self.p_scene_time, self.scenes[str(p_scene_time)]))

        self.p_time += self.bufsize / self.framerate * 1000  # milliseconds
        logger.info('update prediction of current time: {}'.format(self.p_time))

        return [self.p_state]


def _create_model(means, r_error):

    n_components = len(means)
    model = hmm.GaussianHMM(n_components=n_components,
                            covariance_type="full", params='', init_params='')

    i_r_error = 1 - r_error

    # pi: start probability
    startprob = np.full(n_components, (1 - i_r_error) / (n_components - 1))
    startprob[0] = i_r_error
    model.startprob_ = startprob

    # A: transition probability
    # On right-to-right HMM considered error,
    # state will transition to the right next to state,
    # but error may occur with probability `r`.
    transmat = np.identity(n_components)
    transmat = np.append(transmat[:, -1:], transmat[:, :-1], axis=1)
    transmat[transmat == 1] = i_r_error
    transmat[transmat == 0] = (1 - i_r_error) / (n_components - 1)
    model.transmat_ = transmat

    # B: emission probability
    # Gaussian distribution with means from supervised onsets
    model.means_ = means.reshape(-1, 1)
    model.covars_ = np.std(model.means_) * np.tile(np.identity(1), (n_components, 1, 1))

    return model
