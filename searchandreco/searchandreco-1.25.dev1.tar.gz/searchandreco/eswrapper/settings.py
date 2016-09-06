'''
__author__ = 'chitraangi'

settings file

'''

import json
## Import for instantiating elastic search via elasticsearch-py client library
## (elasticsearch==1.4.0)
from elasticsearch import Elasticsearch

#dev and prod es settings file
ESDEV = "/mnt/espipsettingsfile/devESsettings.json"
ESPROD = "/mnt/espipsettingsfile/prodESsettings.json"

#get the dev or prod settings from the respective json files
try:
    INITIALISE_SETTINGS = json.loads(open(ESPROD, 'r').read())
except:
    INITIALISE_SETTINGS = json.loads(open(ESDEV, 'r').read())

# Different nodes of Elastic Search
ES_NODE1 = INITIALISE_SETTINGS['ES_NODE1']
ES_NODE2 = INITIALISE_SETTINGS['ES_NODE2']
ES_NODE3 = INITIALISE_SETTINGS['ES_NODE3']

ES_NODE1_PORT = INITIALISE_SETTINGS['ES_NODE1_PORT']
ES_NODE2_PORT = INITIALISE_SETTINGS['ES_NODE2_PORT']
ES_NODE3_PORT = INITIALISE_SETTINGS['ES_NODE3_PORT']

#elb node
ES_NODE = INITIALISE_SETTINGS['ES_NODE']
ES_NODE_PORT = INITIALISE_SETTINGS['ES_NODE_PORT']

#local and prod vars
USE_LOCAL = INITIALISE_SETTINGS['USE_LOCAL']
UWSGI_SETUP = INITIALISE_SETTINGS['UWSGI_SETUP']

#Gp stopwords file
GP_STOPWORDS_FILE_NAME = INITIALISE_SETTINGS['GP_STOPWORDS_FILE_NAME']

SUB_LOG_FILE_NAME = INITIALISE_SETTINGS['SUB_LOG_FILE_NAME']
GP_SUB_LOG_FILE_NAME = INITIALISE_SETTINGS['GP_SUB_LOG_FILE_NAME']

#host : ports/elb
try:
    ES_HOSTS = [{'host': ES_NODE1, 'port': ES_NODE1_PORT},\
                {'host': ES_NODE2, 'port': ES_NODE2_PORT}, \
            {'host': ES_NODE3, 'port': ES_NODE3_PORT}]
except:
    ES_HOSTS = [{'host': ES_NODE, 'port': ES_NODE_PORT}]

## A little code which instantiates ElasticSearch
if USE_LOCAL == "True":
    ES_CLIENT = Elasticsearch(INITIALISE_SETTINGS['ES_LOCAL_HOST'],\
                              sniff_on_start=True,\
                              sniff_on_connection_fail=True, sniffer_timeout=300)
else:
    ES_CLIENT = Elasticsearch(ES_HOSTS, sniff_on_start=True,\
                              sniff_on_connection_fail=True, sniffer_timeout=300)
