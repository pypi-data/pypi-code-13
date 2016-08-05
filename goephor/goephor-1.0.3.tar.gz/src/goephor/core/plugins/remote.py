'''
Created on Apr 28, 2016

:author: iitow
'''
from modules.remote import Run
from pluginable import Plugin
from modules.log import message


class ssh(Plugin):
    '''
    This class can perform ssh commands
    '''
    def __init__(self, action_manager):
        '''
        ssh Constructor

        :param action_manager: Obj, from action_manager class
        '''
        self.action_manager = action_manager
        Plugin.__init__(self, self.action_manager)

    def cmd(self,
            cmdstr,
            server,
            user,
            rsa_private_path,
            **defaults):
        '''
        Run a command remotely via ssh
        :param cmdstr: String
        :param server: String
        :param user: String
        :param rsa_private_path: String
        :example:
        ```
               - remote.ssh.cmd:
                    - "uname -a"
                    - "some.server.com"
                    - "root"
                    - "~/.ssh/id_rsa"
        ```
        '''
        session = Run(server,
                      rsa_private_path,
                      user,
                      '')
        output = session.cmd(cmdstr)
        if not output.get('code') == 0:
            raise Exception(output.get('stdout'))
        return output.get('stdout')
