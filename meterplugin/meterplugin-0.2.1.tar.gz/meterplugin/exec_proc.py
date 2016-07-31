# Copyright 2014 Boundary, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from subprocess import Popen,PIPE
import shlex
import logging


class ExecProc:
    
    def __init__(self):
        self._command = None
        self._debug = False

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, debug):
        self._debug = debug

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command):
        if type(command) != str:
            raise ValueError
        self._command = command
        
    def execute(self):
        if self.command is None:
            raise ValueError
        args = shlex.split(self.command)
        if self.debug:
            logging.info("command=\"{0}\"".format(args))
        p = Popen(args, stdout=PIPE)
        o, e = p.communicate()
        if self.debug:
            logging.info("before: " + ':'.join(x.encode('hex') for x in o))
        # Remove carriage returns from output
        o = o.replace('\r', '')
        if self.debug:
            logging.info("after: " + ':'.join(x.encode('hex') for x in o))
        if self.debug:
            logging.info("output=\"%s\"",o)
            logging.info(':'.join(x.encode('hex') for x in o))
        return o

