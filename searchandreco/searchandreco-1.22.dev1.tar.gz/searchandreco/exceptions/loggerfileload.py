import json
import logging
import logging.config

filepath = '/mnt' + '/search_logging_config.json'

config = json.load(open(filepath, 'r'))
logging.config.dictConfig(config)

logger_search = logging.getLogger('searchandreco')