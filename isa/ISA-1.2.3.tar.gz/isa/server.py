import logging

import re

import pexpect

_logger = logging.getLogger(__name__)


class SSHServer:
    def __init__(self, host=None, username=None, password=None, identity_file=None, timeout=3, parent_server=None, port=22):
        """
        Connect to an SSH server.

        :param host: host to connect to
        :param username: username to use for the connection
        :param password: password to use for the connect
        :param identity_file: identity file to use to connect to the server
        :param timeout: number of seconds after which the connection will time-out
        :param parent_server: an other SSH server on which the connection will be made
        :param port: the port to connect to
        """
        self.host = host
        self.bash = ".*[^\r\n][\$\#]"
        identity_str = "-i %s " % identity_file if identity_file is not None else ""
        port_str = "-p %s " % str(port)
        command = "ssh %s%s%s@%s" % (port_str, identity_str, username, host)
        if parent_server is None:
            self.ssh = pexpect.spawn(command, timeout=timeout)
            _logger.info("Connecting to host %s" % host)
        else:
            self.ssh = parent_server.ssh
            self.ssh.sendline(command)
            _logger.info("Connecting to host %s via host %s" % (host, parent_server.host))
        _logger.debug(command)
        choice = -1
        while choice in [-1, 0, 1]:
            choice = self.ssh.expect(['[Pp]assword:', 'Are you sure you want to continue connecting', pexpect.EOF, self.bash])
            if choice == 1:
                _logger.debug("Answering 'yes' to 'Are you sure ... continue connecting?'")
                self.ssh.sendline('yes')
            if choice == 0 and password is not None:
                _logger.debug("Filling in a password")
                self.ssh.sendline("%s\r" % password)
            if choice > 1:
                _logger.debug("Received prompt")

        # Try to switch to default bash
        self.ssh.sendline('/bin/bash')
        self.ssh.expect(self.bash)

        _logger.debug("Prompt string: %s" % self.bash)
        _logger.info("Connection to host %s successful" % host)

    def _decode(self, result):
        if type(result) == bytes:
            result = result.decode("utf-8")
        return result

    def _get_output(self):
        return self._decode(self.ssh.before) + self._decode(self.ssh.after)

    def execute(self, command):
        """
        Execute a command and retrieve the output stream.

        :param command: command to execute
        :return: output stream
        """
        self.ssh.sendline(command)
        self.ssh.expect(self.bash)
        result = self._get_output()
        return "\n".join(result.split("\n")[1:-1])
