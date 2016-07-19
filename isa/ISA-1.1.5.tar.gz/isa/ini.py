import logging
import distutils.util as util
from isa.exceptions import CircularException

_logger = logging.getLogger(__name__)


def parse_nodes(ini_path):
    """
    Parse a nodes INI file.

    :param ini_path: path to the nodes INI file
    :return: dictionary with node names as key and a dictionary of all settings per node as value
    """
    try:
        import ConfigParser
    except ImportError:
        import configparser
        ConfigParser = configparser

    def resolve_via(node, node_ini_data):
        """
        Resolve the via path for a given node and a given nodes configuration.

        :param node: the node to resolve the via path for
        :param node_ini_data: the nodes configuration (obtained by parse_nodes_ini)
        :return: an array where the n-th element is the n-th node to connect to via SSH
        """
        if node_ini_data[node]['via'] is None:
            return []
        else:
            via_nodes = []
            current_node = node
            via = node_data[current_node]['via']
            while via is not None:
                if via in via_nodes or via == node:
                    raise CircularException(
                        "Circular via-chain found: node=%s, via_chain=%s" % (node, [node] + via_nodes + [via]))
                via_nodes += [via]
                current_node = via
                via = node_data[current_node]['via']
            return via_nodes[::-1]

    # Initialize a configuration parser to read to INI file
    config = ConfigParser.ConfigParser()
    config.read(ini_path)
    nodes = config.sections()
    _logger.debug("Nodes found: %s" % nodes)

    # Set some default values
    node_data = {node: {
        # Default values
        'host': None,
        'enabled': True,
        'via': None,
        'username': 'root',
        'password': None,
        'identity_file': None
    } for node in nodes}

    # Retrieve the node information
    for node in nodes:
        node_data[node]['host'] = config.get(node, 'host')
        for key, value in config.items(node):
            if key == 'enabled':
                node_data[node]['enabled'] = util.strtobool(value)
            if key in ['via', 'username', 'password', 'identity_file']:
                node_data[node][key] = value

    # Add meta information
    for node in node_data:
        node_data[node]['via-chain'] = resolve_via(node, node_data)

    # Remove unneeded flags
    node_data = {node: {
        key: node_data[node][key]
        for key in node_data[node].keys()
        if key not in ['via']
        } for node in node_data}

    return node_data
