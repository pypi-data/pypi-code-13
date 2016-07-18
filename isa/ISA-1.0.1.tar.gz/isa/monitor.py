import logging
import threading
import datetime
from isa.server import SSHServer

_logger = logging.getLogger(__name__)


class Monitor:
    """
    Class for monitoring a set of nodes.
    """

    def __init__(self, nodes, time_interval=1, init_time=3, result_handler=None, plugins=[]):
        """
        Monitor a set of nodes. After init_time seconds, the script should be logged into the server and every
        time_interval seconds results are collected from the servers. The results are given to the result_handler.

        :param nodes: node configuration obtained by ini.parse_nodes
        :param time_interval: after which interval results should be obtained
        :param init_time: the expected time to log in into the server
        :param result_handler: a method with two arguments: node and result where node is the name of the node and result is a dictionary containing the results
        :param plugins: a list of plugins which are used to collect statistics
        which results are retrieved and result is the results that were collected
        """
        if result_handler is None:
            raise Exception("result_handler is None, should be specified.")
        self.threads = []
        for node in nodes:
            node_info = nodes[node]
            if node_info['enabled']:
                logging.info("Start monitoring node [%s]" % node)
                # Make threads for each of the nodes
                thread = MonitorThread(node, nodes, init_time, time_interval, result_handler, plugins)
                self.threads.append(thread)

    def run(self):
        """ Run all monitors. """
        for thread in self.threads:
            thread.start()


class MonitorThread(threading.Thread):
    """
    Helper class for creating threads.
    """

    def __init__(self, node, nodes, init_time, time_interval, result_handler, plugins):
        """
        Creating threads.

        :param node: the name of the node
        :param nodes: node information
        :param init_time: time needed to initialize a node
        :param time_interval: the specified time interval
        :param result_handler: the result handler
        :param plugins: the list of plugins
        """
        threading.Thread.__init__(self)
        self.node = node
        self.nodes = nodes
        self.time_interval = time_interval
        self.result_handler = result_handler
        self.timeout = 2 * (time_interval + init_time)
        self.server = None
        self.plugins = plugins

    def run(self):
        """ Keep collecting results. """
        if self.server is None:
            self.server = {}
            for plugin in self.plugins:
                node_info = self.nodes[self.node]
                via_server = None
                for via in node_info['via-chain']:
                    parent = self.nodes[via]
                    via_server = SSHServer(parent['host'], parent['username'], parent['password'],
                                           parent_server=via_server, identity_file=parent['identity_file'],
                                           timeout=self.timeout)
                _logger.info("Setting up connection to node [%s] for plugin (%s)" % (self.node, plugin))
                self.server[plugin] = SSHServer(node_info['host'], node_info['username'], node_info['password'],
                                                identity_file=node_info['identity_file'], parent_server=via_server,
                                                timeout=self.timeout)
        while True:
            fields = ['plugin']
            for plugin_name in self.plugins:
                plugin = self.plugins[plugin_name]
                result_data = plugin.collect(self.server[plugin_name])
                for item in result_data:
                    for field in sorted(item.keys()):
                        fields += [plugin_name + '::' + field]
            for plugin_name in self.plugins:
                plugin = self.plugins[plugin_name]
                result_data = plugin.collect(self.server[plugin_name])
                for item in result_data:
                    data = {key: "NULL" for key in fields}
                    data['plugin'] = plugin_name
                    data['time'] = datetime.datetime.now()
                    for field in item:
                        field_name = plugin_name + '::' + field
                        data[field_name] = item[field]
                    self.result_handler(self.node, data)
