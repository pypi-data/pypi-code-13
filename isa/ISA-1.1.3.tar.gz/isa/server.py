import logging
import re
import pexpect

_logger = logging.getLogger(__name__)


class SSHServer:
    def __init__(self, host=None, username=None, password=None, identity_file=None, timeout=3, parent_server=None):
        """
        Connect to an SSH server.

        :param host: host to connect to
        :param username: username to use for the connection
        :param password: password to use for the connect
        :param identity_file: identity file to use to connect to the server
        :param timeout: number of seconds after which the connection will time-out
        :param parent_server: an other SSH server on which the connection will be made
        """
        self.host = host
        self.bash = ".*[\$\#]"
        identity_str = "-i %s" % identity_file if identity_file is not None else ""
        if parent_server is None:
            self.ssh = pexpect.spawn("ssh %s %s@%s" % (identity_str, username, host), timeout=timeout)
            _logger.info("Connecting to host [%s]" % host)
            _logger.debug("ssh %s %s@%s" % (identity_str, username, host))
        else:
            self.ssh = parent_server.ssh
            self.ssh.sendline("ssh %s %s@%s" % (identity_str, username, host))
            _logger.info("Connecting to host [%s] via [%s]" % (host, parent_server.host))
            _logger.debug("ssh %s %s@%s" % (identity_str, username, host))
        if password is not None:
            self.ssh.expect(['[Pp]assword:'])
            _logger.debug("Filling in a password")
            self.ssh.sendline("%s\r" % password)
        self.ssh.expect(self.bash)
        self.bash = self.ssh.after.replace("\r", "\n").split("\n")[-1]
        _logger.debug("Prompt string: %s" % self.bash)
        _logger.info("Connection to host [%s] successful" % host)

    def _get_output(self):
        result = self.ssh.before
        if type(result) == bytes:
            result = result.decode("utf-8")
        return result

    def execute(self, command):
        """
        Execute a command and retrieve the output stream.

        :param command: command to execute
        :return: output stream
        """
        self.ssh.sendline(command)
        self.ssh.expect_exact(self.bash)
        result = self._get_output()
        return "\n".join(result.split("\n")[1:-1])