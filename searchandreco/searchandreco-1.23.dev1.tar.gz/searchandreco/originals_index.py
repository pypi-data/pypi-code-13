'''

__author__ = 'chitraangi'

the originals app file

'''

import json
import web
from .eswrapper.originals_defines import ES_CONTENT_DOC_TYPE
from .eswrapper.originals_eswrapper import SearchIndexerOriginals, SearchManagerOriginals
from .eswrapper.utils import get_index_name
from .urls import URLS
from .eswrapper.settings import ES_CLIENT
from .paginationspellcheck import functiontosearch_originals

APP = web.application(URLS, globals())


class IndexOriginals:
    '''

    This class contains the api to
    index the article as soon as it is published.

    '''

    def POST(self):
        '''
        :param prop:  code for the property for which index is being created
        :param data: the data to be indexed.
        :return:
        '''

        i = web.input()
        data, prop = i.data, i.prop
        index_name = get_index_name(prop)
        indexer = SearchIndexerOriginals(index_name)
        data_to_index = json.loads(data)
        response = indexer.index_single_prop_originals(data_to_index,
                                                       data_to_index['id'])
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        return json.dumps(response)


class UpdateOriginals:
    '''

    This class contains the api to
    index the article as soon as it is published.

    '''

    def PUT(self):
        '''
        :param prop:  code for the property for which index is being created
        :param data: the data to be indexed.
        :return:
        '''

        i = web.input()
        docid, prop, data = i.docid, i.prop, i.data
        index_name = get_index_name(prop)
        indexer = SearchIndexerOriginals(index_name)
        data_to_update = json.loads(data)
        response = indexer.update_doc_prop_originals(docid, data_to_update)
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        return json.dumps(response)


class DeleteOriginals:
    '''
    This class contains the api to
    remove article from the index when unpublished.
    '''

    def DELETE(self):
        '''
        :param prop:  code for the property for which index is being created
        :param docid: id of the document to be deleted from index
        :return:
        '''

        i = web.input()
        docid, prop = i.docid, i.prop
        index_name = get_index_name(prop)
        indexer = SearchIndexerOriginals(index_name)
        response = indexer.delete_doc_originals(docid)
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        return json.dumps(response)


class MltOriginals:
    '''

    This class contains the apis which are hit
    for any kind of search from Elastic Search
    (SWP = '53e4' SWPRTPUB = '25rt')

    '''

    def GET(self):
        '''
        :param q:  query string for search
        :return:
        '''

        send_data = {'info': '', 'status': '0', 'errmsg': ''}

        try:

            i = web.input()
            docid, prop = i.docid, i.prop
            index_name = get_index_name(prop)
            indexer = SearchManagerOriginals(ES_CLIENT, index_name,
                                             ES_CONTENT_DOC_TYPE)
            send_data['info'] = indexer.more_like_this_originals(docid)
            send_data['status'] = '1'
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Credentials', 'true')
            return json.dumps(send_data)

        except Exception as exp:

            send_data['errmsg'] = str(exp)
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Credentials', 'true')
            return json.dumps(send_data)


class SearchORIGINALSUserFacing:
    '''

    This class contains the apis which
     are hit for any kind of search from
     Elastic Search (SWP = '53e4' SWPRTPUB = '25rt')

    '''

    def GET(self):
        '''

        :param pn:  page number
        :param q:  query string for search
        :param sorttype:  score/latest
        :return:
        '''

        data = web.input(q='', pn=1, searchtype='', sorttype='score')
        response = functiontosearch_originals(data.q, data.pn, data.searchtype,
                                              data.sorttype)
        #print response
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        return json.dumps(response)
