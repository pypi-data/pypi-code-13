#   Copyright 2015-2016 University of Lancaster
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import copy
import random
import time

import cherrypy

DEFAULT_CONFIG = {
    'http-error': {
        'codes': [500],
        'chance': {'pre-handler': 0.0, 'post-handler': 0.0}},
    'stall': {
        'range': range(1, 2),
        'chance': {'pre-handler': 0.2, 'post-handler': 0.2}},
}


class MisfortuneTool(cherrypy.Tool):
    def __init__(self, point='before_handler', name=None, priority=99):
        self._point = point
        self._name = name
        self._priority = priority

    def callable(self, http_error=None, stall=None):
        config = copy.deepcopy(DEFAULT_CONFIG)
        if http_error:
            config['http-error'].update(http_error)
        if stall:
            config['stall'].update(stall)

        inner_handler = cherrypy.serving.request.handler

        def wrapper(*args, **kwargs):
            try_stall('pre-handler', config)
            try_http_error('pre-handler', config)

            response = inner_handler(*args, **kwargs)

            try_stall('post-handler', config)
            try_http_error('post-handler', config)

            return response

        cherrypy.serving.request.handler = wrapper


def try_stall(when, config):
    if random.random() < config['stall']['chance'][when]:
        stall_time = random.choice(config['stall']['range'])
        msg = "Misfortune: Stall {} for {}s"
        cherrypy.log(msg.format(when, stall_time))
        time.sleep(stall_time)


def try_http_error(when, config):
    if random.random() < config['http-error']['chance'][when]:
        http_code = random.choice(config['http-error']['codes'])
        msg = "Misfortune: HTTP error {} code {}"
        msg = msg.format(when, http_code)
        cherrypy.log(msg)
        raise cherrypy.HTTPError(http_code, msg)


def install_tool():
    cherrypy.tools.misfortune = MisfortuneTool()
