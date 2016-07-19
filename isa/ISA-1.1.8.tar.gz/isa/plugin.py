import logging

_logger = logging.getLogger(__name__)


class Plugin:

    def install_package(self, server, package):
        """
        Use common package managers to install the given package.

        :param server: SSHServer to install the package on
        :param package: name of the package to install
        """
        command = "sudo yum install %s -y" % package
        _logger.debug("[PLUGIN:%s] Install package [%s] if needed (using yum)" % (self.__class__.__name__, package))
        _logger.debug(command)
        _logger.debug(server.execute(command))
        command = "sudo apt-get install %s -y" % package
        _logger.debug("[PLUGIN:%s] Install package [%s] if needed (using apt-get)" % (self.__class__.__name__, package))
        _logger.debug(command)
        _logger.debug(server.execute(command))
        _logger.debug("[PLUGIN:%s] Installing package [%s] done" % (self.__class__.__name__, package))

    def install(self, server):
        """
        Install the plugin on the given server.

        :param server: the SSHServer to install the software on
        """
        raise Exception("[PLUGIN:%s] Method 'install' is not implemented" % self.__class__.__name__)

    def collect(self, server):
        """
        Collect results using the plugin and give back a list of dictionaries where all dictionaries have the same keys.

        :param: server SSHServer object which is used to execute commands on
        :return: list of dictionaries
        """
        _logger.warn("[PLUGIN:%s] Method 'collect' is not implemented" % self.__class__.__name__)
