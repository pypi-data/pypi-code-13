#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   Copyright 2016 Satoyuki Tsukano

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import boto3
import json
import logging
import uuid
from functools import wraps

logger = logging.getLogger(__name__)
pycro_context_repositry = dict()
config_repositry = dict()


class LocalContext:
    def __init__(self, function_name):
        self.function_name = function_name

RUN_MODE_AWS = 'AWS'
RUN_MODE_LOCAL = 'local'


class PycroContext:
    def __init__(self, name, mode):
        logger.info("init PycroContext name={}".format(name))
        self.mode = mode
        self.name = name

        if self.name not in config_repositry:
            _load_config(self.name)
        config = config_repositry[self.name]
        self.my_prop = _create_my_prop(config, self.mode)

        if self.mode is RUN_MODE_AWS:
            # AWS mode
            self.client = boto3.client('lambda')

    def emit(self, out_payload, context):
        out_event = {"payload": out_payload}
        in_event = context.in_event

        # set trace_id to out_event
        if 'trace_id' in in_event:
            trace_id = in_event['trace_id']
        else:
            trace_id = str(uuid.uuid4())
        out_event['trace_id'] = trace_id

        # check 'call depth limit'
        limit = self.my_prop['call_depth_limit']
        roots = in_event.get('roots', [])
        if len(roots) >= limit:
            logger.warn("limit over! limit is {}, roots is {}".format(limit, roots))
            return
        roots.append(self.name)
        out_event['roots'] = roots

        # invoke following functions
        if self.mode is RUN_MODE_AWS:
            # AWS mode
            for following in self.my_prop['followings']:
                out_json = json.JSONEncoder().encode(out_event)
                logger.info("invoke_async following=" + following + " event=" + out_json)
                self.client.invoke_async(FunctionName=following, InvokeArgs=out_json)
        else:
            # local mode
            from multiprocessing import Process
            for (function_name, target_method) in self.my_prop['followings']:
                context = LocalContext(function_name)
                logger.info("invoke_async following=" + function_name + " event=" + str(out_event))
                process = Process(target=target_method, args=(out_event, context))
                process.start()


def _load_config(name):
    with open(name + '.json', mode='r') as f:
        config_repositry[name] = json.load(f)


def _create_my_prop(config_json, mode):
    call_depth_limit = config_json.get('call_depth_limit', 10)

    if mode is RUN_MODE_AWS:
        # AWS mode
        return {
            'name': config_json['name'],
            'call_depth_limit': call_depth_limit,
            'followings': config_json.get('followings', [])
        }
    else:
        # local mode
        if 'followings' not in config_json:
            return {
                'name': config_json['name'],
                'call_depth_limit': call_depth_limit,
                'followings': []
            }

        followings = config_json['followings']
        my_prop_followings = []
        for following in followings:
            if following not in config_repositry:
                _load_config(following)
            handler = config_repositry[following]['handler']

            [module_name, attr_name] = handler.split('.')
            mod = __import__(module_name)
            target_method = getattr(mod, attr_name)
            my_prop_followings.append((following, target_method))
        return {
            'name': config_json['name'],
            'call_depth_limit': call_depth_limit,
            'followings': my_prop_followings
        }


def _get_pc(context):
    name = context.function_name
    if name not in pycro_context_repositry:
        if hasattr(context, 'aws_request_id'):
            # AWS mode
            pycro_context_repositry[name] = PycroContext(name, RUN_MODE_AWS)
        else:
            # local mode
            pycro_context_repositry[name] = PycroContext(name, RUN_MODE_LOCAL)
    return pycro_context_repositry[name]


def function(auto_emit=True):
    def _function(func):
        @wraps(func)
        def wrapper(*args):
            in_event = args[0]
            context = args[1]
            logger.info("receive={}".format(str(in_event)))

            # add attributes to context
            pc = _get_pc(context)
            context.pycro_context = pc
            context.in_event = in_event

            # parse in_event
            in_payload = in_event.get('payload', in_event)

            # call original function
            out_payload = func(in_payload, context)

            # call following functions
            if auto_emit and out_payload is not None:
                pc.emit(out_payload, context)

            return out_payload
        return wrapper
    return _function
