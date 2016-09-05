"""
Default Sensu-Auditor Settings. Override in the defaults file
"""
import sys
import logging

CONFIG_PATH = '/etc/default/sensu-auditor.ini'

SENSU_LOG_FOLDER = '/var/log/sensu/'

LOG_LOCATION = 'log_location'

LOG_TYPES = ['sensu-client', 'sensu-server', 'sensu-api']

DEFAULT_CONFIG_FIELDS = {'log_location': '/var/log/sensu',
                         'log_level': logging.DEBUG,
                         'log_output': sys.stdout,
                         'days': 30}

DEFAULT_SECTIONS = {
    'user': 'User',
    'group': 'Groups'
}

MESSAGES = {
    'RECEIVED_MESSAGE': 'received check request',
    'PUBLISHED_MESSAGE': 'publishing check result'

}