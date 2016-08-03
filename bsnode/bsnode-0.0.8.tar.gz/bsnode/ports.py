# -*- coding: utf-8 -*-

import os
import logging
import configparser


logger = logging.getLogger(__name__)


class Ports:
    ports_conf = '/etc/bs/ports.conf'

    def __init__(self, node_name=None, range_ports=None, section='default'):
        """Getting port:
            p = Ports(<node_name>, <range_ports>)
            p.get()

        Removing node:

            p = Ports(<node_name>)
            p.remove()

        :type node_name: str
        :type range_ports: range
        :type section: str
        """
        self.section = section
        self.node_name = node_name
        self.range_ports = range_ports

    def exists_ports(self, conf=None):
        """
        :type conf: configparser.ConfigParser
        :return: list
        """

        if not conf:
            conf = configparser.ConfigParser()
            conf.read(self.ports_conf)

        return [int(item[1]) for item in conf.items(self.section)]

    def exists_nodes(self, conf=None):
        """
        :type conf: configparser.ConfigParser
        :return: dict
        """

        if not conf:
            conf = configparser.ConfigParser()
            conf.read(self.ports_conf)

        return {item[0]: int(item[1]) for item in conf.items(self.section)}

    def get(self):
        """
        :return: int
        """
        conf = configparser.ConfigParser()

        if os.path.exists(self.ports_conf):
            # Add to exists file
            # todo: check body of file
            conf.read(self.ports_conf)
            ex_ports = self.exists_ports(conf)

            for number in self.range_ports:
                if number in ex_ports:
                    continue
                else:
                    logger.info('port {} is free'.format(number))
                    conf.set(self.section, self.node_name, str(number))
                    with open(self.ports_conf, 'w') as ports:
                        conf.write(ports)
                    return number
        else:
            # Write a new file if specify file is not exists
            logger.info('file ports.conf not exist, it will create')
            conf.add_section(self.section)
            conf.set(self.section, self.node_name, str(self.range_ports[0]))
            with open(self.ports_conf, 'w') as port:
                conf.write(port)
            return self.range_ports[0]

        return 0

    def remove(self):
        """
        :return: bool
        """
        conf = configparser.ConfigParser()
        conf.read(self.ports_conf)

        if self.node_name in self.exists_nodes(conf):
            if conf.remove_option(self.section, self.node_name):
                with open(self.ports_conf, 'w') as ports:
                    conf.write(ports)
                logger.info('success deleting port of node {}'.format(
                    self.node_name))
                return True
            else:
                logger.error('deleting port of node {} is failed'.format(
                    self.node_name))
                return False
        else:
            logger.error('node {} not found in ports'.format(self.node_name))
            return False
