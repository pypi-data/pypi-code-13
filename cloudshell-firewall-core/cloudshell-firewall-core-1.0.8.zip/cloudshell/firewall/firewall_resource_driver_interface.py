#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABCMeta
from abc import abstractmethod


class FirewallResourceDriverInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def send_custom_command(self, context, command):
        pass

    @abstractmethod
    def send_custom_config_command(self, context, command):
        pass

    @abstractmethod
    def save(self, context, folder_path, configuration_type):
        pass

    @abstractmethod
    def restore(self, context, path, config_type, restore_method):
        pass

    @abstractmethod
    def get_inventory(self, context):
        pass

    @abstractmethod
    def update_firmware(self, context, remote_host, file_path):
        pass

    @abstractmethod
    def shutdown(self, context):
        pass
