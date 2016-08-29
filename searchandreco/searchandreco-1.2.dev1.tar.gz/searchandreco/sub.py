__author__ = 'monica'



import threading
import time
from eswrapper.settings import *
from eswrapper.eswrapper import SearchIndexer
import json
import logging


VBQ = 'vbq'
INDEX_NAME = 'vb_posts'
DOC_TYPE = 'post'
ES_DOC_ID = 'id'



search_indexer = SearchIndexer(INDEX_NAME, DOC_TYPE)
logging.basicConfig(filename=SUB_LOG_FILE_NAME, level=logging.WARNING)


## Using the WARNING level for now so that only our stuff comes in log file
## For Info and Debug, a lot of unrequired text comes from Elastic Search...
def callback():


  sub = redis_client.pubsub()

  sub.subscribe(VBQ)


  while True:

    for msg in sub.listen():

        if(msg['data'] != 1):

            es_doc = json.loads(msg['data'])
            logging.warning(es_doc[ES_DOC_ID])
            search_indexer.index_single(es_doc, es_doc[ES_DOC_ID]) #'Recieved: {0}'.format(m['data'])

def main():

  t = threading.Thread(target=callback)
  t.setDaemon(True)
  t.start()

  while True:
    logging.warning('Waiting')
    time.sleep(300)



if __name__ == '__main__':
    main()

