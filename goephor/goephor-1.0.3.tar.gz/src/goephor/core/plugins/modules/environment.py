'''
Created on Apr 26, 2016

:author: iitow
'''
import os
import re


class EnvManager(object):
    '''
    Management of runtime environment

    :note: This is passed to each of the plugins
    when the action obj is initialized
    Its contained within the action_manager.
    '''
    def __init__(self, debug=False):
        '''
        Constructor

        :param debug: Bool
        '''
        self.debug = debug
        self.envs = {}

    def set(self, key, value, reset=True):
        '''
        set an environment variable

        :param key: String
        :param value: String
        :param reset: Bool, if false it will not override an existing env value
        '''
        has_value = self.get(key)
        value = self._sanitize(value)
        if reset:
            if self.debug:
                print '[set] %s=%s' % (key, value)
            self.envs[key] = value
            os.environ[key] = str(value)
        elif not reset and not has_value:
            if self.debug:
                print '[set] %s=%s' % (key, value)
            self.envs[key] = value
            os.environ[key] = str(value)
        else:
            if self.debug:
                print '[reset] ignore set %s=%s' % (key, value)
    def unset(self,key):
        '''
        unset environment variable

        :param value: String
        '''
        has_value = self.get(key)
        if has_value:
            self.envs.pop(key, None)
            del(os.environ[key])

    def get(self, key):
        '''
        get an environment variable

        :param key: String
        '''
        env = os.environ.get(key, None)
        if self.debug:
            print '[get] %s=%s' % (key, env)
        return env

    def sanitize(self, values):
        '''
        sanitizes environment variables in a given values

        :param values: List
        '''
        if isinstance(values, dict):
            dfts = {}
            for key, value in values.iteritems():
                if "$" in key:
                    key = self._sanitize(key)
                if isinstance(value, list):
                    dfts[key] = value
                else:
                    dfts[key] = self._sanitize(value)
            return dfts
        else:
            params = []
            for param in values:
                params.append(self._sanitize(param))
            return params

    def _sanitize(self, stri):
        """ Replace all environment variables into command

        :param stri: String,Bool,Int
        :note: when nested environment variables are used
        in a string convert all
        """
        if isinstance(stri, bool) or isinstance(stri, int):
            return stri
        if isinstance(stri, str):
            matches = re.findall(r'(?<=\${)[^}]*', stri)
            for match in matches:
                old = '${%s}' % match
                new = os.environ.get(match)
                if new:
                    stri = stri.replace(old, new)
        return stri
