__author__ = 'chitraangi'


import os
import sys
import json

## Import for instantiating elastic search via elasticsearch-py client library
## (elasticsearch==1.4.0)

from elasticsearch import Elasticsearch


devES = "/mnt/devESsettings.json"


try:

    devsettings = json.loads(open(devES, 'r').read())

except:
    print "file not there"
    pass


# Different nodes of Elastic Search

ES_NODE1 = devsettings['ES_NODE1']

ES_NODE2 = devsettings['ES_NODE2']

ES_NODE3 = devsettings['ES_NODE3']

ES_NODE1_PORT = devsettings['ES_NODE1_PORT']

ES_NODE2_PORT = devsettings['ES_NODE2_PORT']

ES_NODE3_PORT = devsettings['ES_NODE3_PORT']


USE_LOCAL = devsettings['USE_LOCAL']

UWSGI_SETUP = devsettings['UWSGI_SETUP']


GP_STOPWORDS_FILE_NAME = devsettings['GP_STOPWORDS_FILE_NAME']

SUB_LOG_FILE_NAME = devsettings['SUB_LOG_FILE_NAME']
GP_SUB_LOG_FILE_NAME = devsettings['GP_SUB_LOG_FILE_NAME']




ES_HOSTS = [{'host': ES_NODE1, 'port': ES_NODE1_PORT}, {'host': ES_NODE2, 'port': ES_NODE2_PORT}, \
            {'host': ES_NODE3, 'port': ES_NODE3_PORT}]


    ## A little code which instantiates ElasticSearch
print devsettings['ES_LOCAL_HOST']
print USE_LOCAL

if(USE_LOCAL == True):

    es_client = Elasticsearch(devsettings['ES_LOCAL_HOST'], sniff_on_start=True, sniff_on_connection_fail=True, sniffer_timeout=300)
# else:
#     es_client = Elasticsearch(ES_HOSTS, sniff_on_start=True, sniff_on_connection_fail=True, sniffer_timeout=300)