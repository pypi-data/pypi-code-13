'''
Created on Apr 25, 2016

:author: iitow
'''
from modules.environment import EnvManager
from modules.log import message
import types
import sys


class DecoMeta(type):
    '''
    This is a meta class for decorating all classes
    '''
    def __new__(cls, name, bases, attrs):
        '''
        Allows for grabbing class info for parsing
        '''
        for attr_name, attr_value in attrs.iteritems():
            if isinstance(attr_value, types.FunctionType):
                attrs[attr_name] = cls.deco(attr_value)
        return super(DecoMeta, cls).__new__(cls, name, bases, attrs)

    @classmethod
    def deco(cls, func):
        '''
        We use this to append defaults actions here
        '''
        def wrapper(*args, **kwargs):
            '''
            This is a decorator for adding global key,value pairs
            '''
            # filter updates
            filter_args = []
            filter_kwargs = {}
            keywords = {}
            # filter parameters
            for arg in args:
                if isinstance(arg, str):
                    filter_args.append(EnvManager()._sanitize(arg))
                else:
                    filter_args.append(arg)
            # filter defaults
            for key, value in kwargs.iteritems():
                if isinstance(value, str):
                    # create environment variable
                    if 'set_env' == key:
                        keywords[key] = EnvManager()._sanitize(value)
                    else:
                        if '$' in key:
                            key = EnvManager()._sanitize(key)
                        filter_kwargs[key] = EnvManager()._sanitize(value)
                else:
                    filter_kwargs[key] = value
            result = func(*filter_args, **filter_kwargs)
            if keywords.get('set_env'):
                EnvManager().set(keywords.get('set_env'),
                                 result,
                                 reset=True)
            return result
        sys.stdout.flush()
        return wrapper


class Plugin(object):
    ''' This is the base class for a plugin
    '''
    __metaclass__ = DecoMeta

    def __init__(self, action_manager):
        '''
        Plugin constructor
        '''
        self.action_manager = action_manager
        self.verbose = self.action_manager.verbose
        self.debug = self.action_manager.debug
        self.EnvManager = self.action_manager.EnvManager
