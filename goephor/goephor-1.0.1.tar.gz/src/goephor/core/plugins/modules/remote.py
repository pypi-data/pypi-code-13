'''
Created on Nov 18, 2015

:author: iitow
'''
import socket
import sys
from terminal import ssh, shell
import time


class Run(object):
    ''' This class represents a remote machine
    using SSH to perform all needed actions
    '''
    def __init__(self,
                 server,
                 rsa_private,
                 user,
                 password,
                 strict=True,
                 verbose=True,
                 show_cmd=True):
        """ Initializes a Remote session
        :param server: server address
        :param rsa_private: path to the private key file
        :param user: Username used to log into system
        :param password: Password used to log into system
        :param strict: boolean fail on error
        :param verbose: print out all debug messaging
        :param show_cmd: show the command given to remote server
        """
        self.hostname = socket.gethostname()
        self.server = server
        self.rsa_private = rsa_private
        self.user = user
        self.password = password
        self.strict = strict
        self.verbose = verbose
        self.show_cmd = show_cmd
        if not self.is_alive_poll():
            print "\n[Error] unable to ping host %s" % (self.server)
            sys.exit(1)
        if not self.has_access():
            print "[Info] No rsa key on host %s" % self.server
            print "[Info] lets try to add one %s" % self.server
            self.set_rsa()
            if not self.has_access():
                print "\n[Error] add rsa key to host %s" % (self.server)
                sys.exit(1)
        print "\n[connection] Successful %s\n" % self.server
        if not self.is_writable_poll():
            print "[Warning] servers file system is not writable"

    def is_alive(self):
        """ Pings the remote to make sure its a valid address
        :return: boolean
        """
        session = shell('/usr/bin/env ping -c 1 %s' % (self.server),
                        strict=False,
                        verbose=False,
                        show_cmd=False)
        if session.get('code') == 0:
            return True
        return False

    def is_alive_poll(self, timeout=30):
        """ Polls for a ping
        :param timeout: default 30 seconds
        :return: boolean
        """
        cnt = 0
        while True:
            if self.is_alive():
                return True
            if cnt > timeout:
                break
            time.sleep(1)
            cnt += 1
        return False

    def is_writable(self):
        """ Check to make sure the file system is writable
        :return: boolean
        """
        file = "is_writable.test.%s" % (self.hostname)
        cmd = 'touch %s' % (file)
        session = ssh(self.server,
                      cmd,
                      rsa_private=self.rsa_private,
                      user=self.user,
                      password=self.password,
                      strict=False,
                      verbose=False,
                      add_rsa=False,
                      show_cmd=False)
        if session.get('code') == 0:
            return True
        return False

    def is_writable_poll(self, timeout=30):
        """ Check to make sure file system is writable poll
        :param timeout: default 30 seconds
        :return: boolean
        """
        cnt = 0
        while True:
            if self.is_writable():
                return True
            if cnt > timeout:
                break
            time.sleep(1)
            cnt += 1
        return False

    def has_access(self):
        """ Does a key already exist on the remote?
        :return: boolean
        """
        cmd = 'hostname'
        session = ssh(self.server,
                      cmd,
                      rsa_private=self.rsa_private,
                      user=self.user,
                      password=self.password,
                      strict=False,
                      verbose=False,
                      add_rsa=False,
                      show_cmd=False)
        if session.get('code') == 0:
            return True
        return False

    def has_file(self, file):
        """ Does a file exist on the remote?
        :param path: path where file should exist
        :param file: name of the file
        """
        cmd = "[ -f %s ] && echo 'true' || echo 'false'" % (file)
        session = self.cmd(cmd)
        output = session.get('stdout').split('\n')
        code = session.get('code')
        if not code == 0:
            print "[Error] code:" % str(code)
            return False
        if 'true' in output:
            return True
        return False

    def has_dir(self, dir):
        """ Does a file exist on the remote?
        :param path: path where file should exist
        :param file: name of the file
        :return boolean
        """
        cmd = "[ -d %s ] && echo 'true' || echo 'false'" % (dir)
        session = self.cmd(cmd)
        output = session.get('stdout').split('\n')
        code = session.get('code')
        if not code == 0:
            print "[Error] code:" % str(code)
            return False
        if 'true' in output:
            return True
        return False

    def remove(self, path, recursive=True):
        """ Remove a file or directory on remote
        :param path:path to file/dir to remove
        :param recursive: adds a -r to the rm command
        :return: boolean
        """
        if recursive:
            cmd = "rm -rf %s" % path
        else:
            cmd = "rm -f %s" % path
        session = ssh(self.server,
                      cmd,
                      rsa_private=self.rsa_private,
                      user=self.user,
                      password=self.password,
                      strict=False,
                      verbose=False,
                      add_rsa=False,
                      show_cmd=False)
        if session.get('code') == 0:
            return True
        return False

    def move(self, src, dest):
        """ Perform a move operation
        :param src: String
        :param dest: String
        """
        cmd = "mv %s %s" % (src, dest)
        session = ssh(self.server,
                      cmd,
                      rsa_private=self.rsa_private,
                      user=self.user,
                      password=self.password,
                      strict=False,
                      verbose=False,
                      add_rsa=False,
                      show_cmd=False)
        if session.get('code') == 0:
            return True
        return False

    def copy(self, src, dest, opts=''):
        """ Perform a copy operation
        :param src: String
        :param dest: String
        """
        cmd = "cp %s %s %s" % (opts, src, dest)
        session = ssh(self.server,
                      cmd,
                      rsa_private=self.rsa_private,
                      user=self.user,
                      password=self.password,
                      strict=False,
                      verbose=False,
                      add_rsa=False,
                      show_cmd=False)
        if session.get('code') == 0:
            return True
        return False

    def set_rsa(self):
        """ Put a rsa key on the remote
        :return: None
        """
        cmd = 'hostname'
        session = ssh(self.server,
                      cmd,
                      rsa_private=self.rsa_private,
                      user=self.user,
                      password=self.password,
                      strict=False,
                      verbose=False,
                      add_rsa=True,
                      show_cmd=False)
        return session

    def cmd(self, cmd):
        """ Runs a shell command on the remote
        :return: session info
        """
        session = ssh(self.server,
                      cmd,
                      rsa_private=self.rsa_private,
                      add_rsa=False,
                      user=self.user,
                      password=self.user,
                      strict=self.strict,
                      verbose=self.verbose)
        return session

    def find(self, path, file):
        """ Finds a file on the remote system returns a list of values
        :param path: path where file should exist
        :param file: name of the file
        :return: output from the session
        """
        cmd = "/usr/bin/find %s -name %s" % (path, file)
        session = self.cmd(cmd)
        output = session.get('stdout').split('\n')
        code = session.get('code')
        if not code == 0:
            print "[Error] code:" % str(code)
            return None
        return output

    def os_type(self):
        """ Gets the os type of the system
        :return: returns os string
        """
        cmd = "uname -mrs"
        session = self.cmd(cmd)
        output = session.get('stdout')
        code = session.get('code')
        if not code == 0:
            print "[Error] code:" % str(code)
            return None
        return output

    def onefs_version(self):
        '''
        Get onefs os version
        '''
        os_type = self.os_type()
        if "OneFS" not in os_type:
            print "[Error] not onefs system"
            return None
        version_str = os_type.split('OneFS', 1)[1]
        version = version_str.split(' ')[1].replace('v', '').split('.')
        return version

    def get_MD5(self, file):
        """ gets the md5sum of a file
        Supports Freebsd and Linux
        :return: md5 string
        """
        os_type = self.os_type()
        md5_type = None
        if "Linux" in os_type:
            md5_type = '/usr/bin/md5sum'
        else:
            md5_type = '/sbin/md5'
        cmd = "%s %s" % (md5_type, file)
        session = self.cmd(cmd)
        output = session.get('stdout')
        code = session.get('code')
        if not code == 0:
            print "[Error] code:" % str(code)
            return None
        return self._clean_MD5(os_type, output)

    def _clean_MD5(self, os_type, output):
        """ private Cleans the md5 string produced
        :param os_type: type of operating system
        :param output: string from get_MD5
        """
        md5_str = None
        if "Linux" in os_type:
            md5_str = output.partition(' ')[0].strip()
        else:
            md5_str = output.partition('=')[2].strip()
        return md5_str
