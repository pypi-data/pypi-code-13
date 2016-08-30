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


print devsettings
print type(devsettings)


# Different nodes of Elastic Search

ES_NODE1 = '10.2.3.xx'

ES_NODE2 = '10.2.3.xxx'

ES_NODE3 = '10.2.3.xxx'

ES_NODE1_PORT = '8080'

ES_NODE2_PORT = '8080'

ES_NODE3_PORT = '8080'


USE_LOCAL = True

UWSGI_SETUP = False


GP_STOPWORDS_FILE_NAME = "/mnt/apps/repo/searchandreco/searchandreco/hindi_stpwords.txt"

SUB_LOG_FILE_NAME = '/mnt/logs/esapi/vbsub.log'
GP_SUB_LOG_FILE_NAME = '/mnt/logs/esapi/gpsub.log'




ES_HOSTS = [{'host': ES_NODE1, 'port': ES_NODE1_PORT}, {'host': ES_NODE2, 'port': ES_NODE2_PORT}, \
            {'host': ES_NODE3, 'port': ES_NODE3_PORT}]


    ## A little code which instantiates ElasticSearch

if(USE_LOCAL == True):

    es_client = Elasticsearch("http://10.2.1.14:9200/", sniff_on_start=True, sniff_on_connection_fail=True, sniffer_timeout=300)
else:
    es_client = Elasticsearch(ES_HOSTS, sniff_on_start=True, sniff_on_connection_fail=True, sniffer_timeout=300)