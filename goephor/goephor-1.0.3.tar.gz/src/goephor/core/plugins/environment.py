'''
Created on Apr 27, 2016

:author: iitow
'''
import os
from pluginable import Plugin
from modules.log import message


class env(Plugin):
    ''' Environment specific tasks go here
    '''
    def __init__(self, action_manager):
        '''
        env Constructor

        :param action_manager: Obj, from action_manager class
        '''
        self.action_manager = action_manager
        Plugin.__init__(self, self.action_manager)

    def set(self,
            key,
            value,
            **defaults):
        '''
        Set an environment variable

        :param key: String
        :param value: String
        :example:
        ```
        - environment.env.set:
           - "VAR1"
           - "some value"
        ```
        '''
        self.EnvManager.set(key, value)
        if self.verbose:
            print message('info',"[set] %s=%s" % (key, value),debug=self.debug)

    def unset(self,
            key,
            **defaults):
        '''
        Unset an environment variable

        :param key: String
        :param value: String
        :example:
        ```
        - environment.env.unset:
           - "VAR1"
        ```
        '''
        self.EnvManager.unset(key)
        if self.verbose:
            print message('info',"[unset] %s" % (key),debug=self.debug)

class utils(Plugin):
    ''' Environment utilities
    '''
    def __init__(self, action_manager):
        '''
        env Constructor

        :param action_manager: Obj, from action_manager class
        '''
        self.action_manager = action_manager
        Plugin.__init__(self, self.action_manager)
    
    def has_path(self,path_str,**defaults):
        '''
        Checks if a pth exists
        
        :param path_str: String
        :return: boolean
        :example:
        ```
        - environment.utils.has_path:
           - "/some/path"
           - set_env: "VAR1"
        ```
        '''
        output = os.path.exists(path_str)
        if self.verbose:
            print message('info',"[has_path] %s @ %s" % (output,path_str),debug=self.debug)
        return output
        

