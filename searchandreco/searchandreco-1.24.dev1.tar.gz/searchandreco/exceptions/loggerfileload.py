'''
__author__ = 'chitraangi'

logs the errors.
'''
import json
import logging
import logging.config

FILEPATH = '/mnt' + '/search_logging_config.json'

CONFIG = json.load(open(FILEPATH, 'r'))
logging.config.dictConfig(CONFIG)

LOGGER_SEARCH = logging.getLogger('searchandreco')
