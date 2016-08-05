# coding=utf-8
u"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of kudubot.

    kudubot makes use of various third-party python modules to serve
    information via online chat services.

    kudubot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    kudubot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with kudubot.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from __future__ import absolute_import
import os
from typing import List
from puffotter.fileops import ensure_directory_exists, ensure_file_exists, ensure_sqlite3_db_exists

# Import structure to combat cyclic imports
try:
    from kudubot.connection.generic.Connection import Connection
except ImportError:
    Connection = None


class LocalConfigChecker(object):
    u"""
    The LocalConfigVChecker that makes sure that the local config is in a correct
    state and fixes it in case it is not.
    """

    program_directory = os.path.join(os.path.expanduser(u"~"), u".kudubot")
    u"""
    The parent directory of all config (and other local) files
    """

    config_directory = os.path.join(program_directory, u"config")
    u"""
    Directory containing configuration files
    """

    log_directory = os.path.join(program_directory, u"logs")
    u"""
    Directory containing program logs
    """

    exception_logs_directory = os.path.join(log_directory, u"exceptions")
    u"""
    Directory containing exception logs
    """

    contacts_directory = os.path.join(program_directory, u"contacts")
    u"""
    Directory containing contact files
    """

    services_directory = os.path.join(program_directory, u"services")
    u"""
    Directory reserved for service files
    """

    # noinspection PyTypeChecker
    @staticmethod
    def check_and_fix_config(connection_types):
        u"""
        Checks if the config is correct and fixes it if that is not the case

        :param connection_types: A list of possible connection types to be able to check the individual
                                    connection configs as well
        :return: None
        """

        ensure_directory_exists(LocalConfigChecker.program_directory)
        ensure_directory_exists(LocalConfigChecker.config_directory)
        ensure_directory_exists(LocalConfigChecker.log_directory)
        ensure_directory_exists(LocalConfigChecker.contacts_directory)
        ensure_directory_exists(LocalConfigChecker.exception_logs_directory)
        ensure_directory_exists(LocalConfigChecker.services_directory)

        for connection in connection_types:
            connection_logs = os.path.join(LocalConfigChecker.log_directory, connection.identifier)
            connection_config = os.path.join(LocalConfigChecker.config_directory, connection.identifier)
            connection_service_config = connection_config + u"-services"
            connection_contacts = os.path.join(LocalConfigChecker.contacts_directory, connection.identifier)
            connection_service_directory = os.path.join(LocalConfigChecker.services_directory, connection.identifier)

            ensure_directory_exists(connection_logs)
            ensure_directory_exists(connection_contacts)
            ensure_directory_exists(connection_service_directory)
            ensure_file_exists(connection_service_config)
            ensure_file_exists(connection_config)

            message_logs = os.path.join(connection_logs, u"messages")
            group_logs = os.path.join(message_logs, u"groups")
            user_logs = os.path.join(message_logs, u"users")

            ensure_directory_exists(message_logs)
            ensure_directory_exists(group_logs)
            ensure_directory_exists(user_logs)

            admin_contacts = os.path.join(connection_contacts, u"admin")
            blacklist_contacts = os.path.join(connection_contacts, u"blacklist")
            connection_addressbook = os.path.join(connection_contacts, u"addressbook.db")

            ensure_file_exists(admin_contacts)
            ensure_file_exists(blacklist_contacts)

            addressbook_sql = u"CREATE TABLE Contacts (" \
                              u"    address TEXT," \
                              u"    name TEXT)"

            ensure_sqlite3_db_exists(connection_addressbook, addressbook_sql, True)
