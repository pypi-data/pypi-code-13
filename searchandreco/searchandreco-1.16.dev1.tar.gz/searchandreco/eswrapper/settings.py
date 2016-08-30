__author__ = 'chitraangi'


## Import for instantiating elastic search via elasticsearch-py client library
## (elasticsearch==1.4.0)
from elasticsearch import Elasticsearch
import json


#dev and prod es settings file
devES = "/mnt/espipsettingsfile/devESsettings.json"
prodES = "/mnt/espipsettingsfile/prodESsettings.json"

#get the dev or prod settings from the respective json files
try:
    initiate_settings = json.loads(open(prodES, 'r').read())
except:
    initiate_settings = json.loads(open(devES, 'r').read())


# Different nodes of Elastic Search
ES_NODE1 = initiate_settings['ES_NODE1']
ES_NODE2 = initiate_settings['ES_NODE2']
ES_NODE3 = initiate_settings['ES_NODE3']

ES_NODE1_PORT = initiate_settings['ES_NODE1_PORT']
ES_NODE2_PORT = initiate_settings['ES_NODE2_PORT']
ES_NODE3_PORT = initiate_settings['ES_NODE3_PORT']


#elb node
ES_NODE = initiate_settings['ES_NODE']
ES_NODE_PORT = initiate_settings['ES_NODE_PORT']


#local and prod vars
USE_LOCAL = initiate_settings['USE_LOCAL']
UWSGI_SETUP = initiate_settings['UWSGI_SETUP']


#Gp stopwords file
GP_STOPWORDS_FILE_NAME = initiate_settings['GP_STOPWORDS_FILE_NAME']


SUB_LOG_FILE_NAME = initiate_settings['SUB_LOG_FILE_NAME']
GP_SUB_LOG_FILE_NAME = initiate_settings['GP_SUB_LOG_FILE_NAME']


#host : ports/elb
try :
    ES_HOSTS = [{'host': ES_NODE1, 'port': ES_NODE1_PORT}, {'host': ES_NODE2, 'port': ES_NODE2_PORT}, \
            {'host': ES_NODE3, 'port': ES_NODE3_PORT}]
except :
    ES_HOSTS = [{'host': ES_NODE, 'port': ES_NODE_PORT}]


## A little code which instantiates ElasticSearch
if(USE_LOCAL == "True"):
    es_client = Elasticsearch(initiate_settings['ES_LOCAL_HOST'], sniff_on_start=True, sniff_on_connection_fail=True, sniffer_timeout=300)
else:
    es_client = Elasticsearch(ES_HOSTS, sniff_on_start=True, sniff_on_connection_fail=True, sniffer_timeout=300)