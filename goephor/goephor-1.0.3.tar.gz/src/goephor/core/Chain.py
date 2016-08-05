'''
Contained in this file is the main loops
:author: iitow
'''

from plugins import *
from plugins.modules.action import Manager
from plugins.modules.environment import EnvManager
from plugins.modules.log import message
import os
import sys


class Run(object):
    '''
    This is the entry point from the cli and drives components
    '''
    def __init__(self,
                 config_file,
                 verbose=False,
                 debug=False):
        '''
        Run Constructor

        :param config_file: path to yaml manifest
        :param verbose: print general run info
        :param debug: print debug info
        '''
        self.verbose = verbose
        self.debug = debug
        self.config_file = config_file
        self.EnvManager = EnvManager(debug=self.debug)
        self.config = self.read_config(config_file)
        self.action_manager = Manager(self.config,
                                      self.EnvManager,
                                      verbose=self.verbose,
                                      debug=self.debug)
        self.on_exit_manager = Manager(self.config,
                              self.EnvManager,
                              verbose=self.verbose,
                              debug=self.debug)
        self.load_actions()
        self.load_on_exit()

    def __enter__(self):
        ''' Entry point for Run obj
        '''
        return self

    def __exit__(self,
                 exception_type,
                 value,
                 trace):
        ''' performs actions on exit of obj
        '''
        self.execute_on_exit()

    def read_config(self, config_file):
        """
        Allows for reading .yaml or .json files

        :param config_file: defines all actions in a build
        :return: dict
        """
        ext = config_file.rsplit('.', 1)[1]
        data = None
        if 'yaml' in ext:
            data = self._read_yaml(config_file)
            self.config_type = ext
        elif 'json' in ext:
            data = self._read_json(config_file)
            self.config_type = ext
        if not data:
            print "[Error] file @ %s" % (config_file)
            sys.exit(1)
        return data

    def _read_yaml(self, config_file):
        """
        Reads in the yaml config

        :param config_file: defines all actions in a build
        :return: dict
        """
        data = None
        try:
            import yaml
            with open(config_file) as file:
                data = yaml.load(file)
                return data
        except Exception:
            print "[Error] %s" % (config_file)
            raise

    def _read_json(self, config_file):
        """
        Reads in the json config

        :param config_file: defines all actions in a build
        :return: dict
        """
        data = None
        try:
            import json
            with open(config_file) as file:
                data = json.loads(file.read())
                return data
        except Exception:
            print "[Error] %s" % (config_file)
            raise

    def add_envs(self, **envs):
        '''
        Overrides environment variables from cli

        :param **envs: dictionary of environment variables
        '''
        for key, value in envs.iteritems():
            self.EnvManager.set(key, value)

    def set_envs(self):
        '''
        sets environment variables inside of manifest
        :params reset: Boolean, If param exists reset it
        '''
        for e in self.config.get('globals'):
            key = e.keys()[0]
            self.EnvManager.set(key, e.get(key), reset=False)

    def load_actions(self):
        '''
        loads actions in to chain resolves yaml/json to a object
        '''
        actions = self.config.get('actions',None)
        if not actions:
            raise Exception('[Missing] actions in manifest')
        for action in actions:
            try:
                action_obj = self.action_manager.to_obj(action,
                                                        self.action_manager)
            except Exception as e:
                print "\n[Error] %s\n" % (e)
                print action
                sys.exit(1)
            self.action_manager.add(action_obj)

    def load_on_exit(self):
        '''
        loads on_exit actions in to chain resolves yaml/json to a object
        '''
        actions = self.config.get('on_exit',None)
        if actions:
            for action in actions:
                try:
                    action_obj = self.on_exit_manager.to_obj(action,
                                                            self.on_exit_manager)
                except Exception as e:
                    print "\n[Error] %s\n" % (e)
                    print action
                    sys.exit(1)
                self.on_exit_manager.add(action_obj)

    def execute_actions(self):
        ''' Executes all action objects
        '''
        this_action = None
        if self.action_manager.chain:
            print message('header','[actions] Start @ %s' % (self.config_file),debug=self.debug)
        for action in self.action_manager.chain:
            try:
                if (self.action_manager.failure is False or
                        action.ignore is True):
                    if self.verbose:
                        print message('header',"\n[%s]" % (action.name),debug=self.debug)
                    action.execute()
                else:
                    pass
            except Exception as e:
                error = '[action] [Error] %s' % (str(e))
                print message('error',error,debug=self.debug)
                self.action_manager.failure = True
                this_action = action
        if self.action_manager.failure is True:
            this_action.pprint(title='Failure', footer='Failure',message_type='error')
            output =  message('fail','manifest @ %s' % (self.config_file),debug=self.debug)
            raise Exception(output)
        else:
            print message('header','[actions] Success @ %s' % (self.config_file),debug=self.debug)

    def execute_on_exit(self):
        ''' Executes all on exit action objects
        '''
        if self.on_exit_manager.chain:
            print message('header','[on_exit] Start @ %s' % (self.config_file),debug=self.debug)
        this_action = None
        for action in self.on_exit_manager.chain:
            try:
                if (self.on_exit_manager.failure is False or
                        action.ignore is True):
                    if self.verbose:
                        print message('header',"\n[%s]" % (action.name),debug=self.debug)
                    action.execute()
                else:
                    pass
            except Exception as e:
                error = '[on_exit] [Error] @ %s: %s' % (self.config_file,str(e))
                print message('error',error,debug=self.debug)
                self.on_exit_manager.failure = True
                this_action = action
        if self.on_exit_manager.failure is True:
            this_action.pprint(title='Failure', footer='Failure',message_type='error')
            output = message('fail','manifest @ %s' % (self.config_file),debug=self.debug)
            raise Exception(output)
        if self.on_exit_manager.chain:
            print message('header','[on_exit] Success @ %s' % (self.config_file),debug=self.debug)
