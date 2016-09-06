'''
__author__ = 'chitraangi'

sportscrumbs app file

'''

import json
import web
from .eswrapper.sportscrumbs_eswrapper import SearchIndexerSportscrumbs
from .eswrapper.utils import get_index_name
from .urls import URLS
from .paginationspellcheck import functiontosearch_sc, functiontosuggest_sc

APP = web.application(URLS, globals())


class IndexSport:
    '''
    This class contains the api to index the article as soon as it is published.
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
        indexer = SearchIndexerSportscrumbs(index_name)
        data_to_index = json.loads(data)
        response = indexer.index_single_prop_sprtcrmbs(data_to_index,
                                                       data_to_index['id'])
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        return json.dumps(response)


class SearchSport:
    '''
    This class contains the apis which are hit
     for any kind of search from Elastic Search (SWP = '53e4' SWPRTPUB = '25rt')
    '''

    def GET(self):
        '''
        :param pn:  page number
        :param q:  query string for search
        :return:
        '''

        data = web.input(q='', pn=1, sorttype='score')
        response = functiontosearch_sc(data.q, data.pn, data.sorttype)
        #print response
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        return json.dumps(response)


class SuggestSport:
    '''
    This class contains the apis which are hit
     for any kind of search from Elastic Search (SWP = '53e4' SWPRTPUB = '25rt')
    '''

    def GET(self):
        '''
        :param pn:  page number
        :param q:  query string for search
        :return:
        '''

        data = web.input(q='', pn=1, searchtype='')
        response = functiontosuggest_sc(data.q, data.pn, data.searchtype)
        #print response
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        return json.dumps(response)

# class UpdateSport:
#
# 	'''
# 	This class contains the api to index the article as soon as it is published.
# 	'''
#
# 	def PUT(self):
#
# 		'''
# 		:param prop:  code for the property for which index is being created
# 		:param data: the data to be indexed.
# 		:return:
# 		'''
#
# 		i = web.input()
# 		docid,prop,data = i.docid,i.prop,i.data
# 		index_name = get_index_name(prop)
# 		indexer = SearchIndexerOriginals(index_name)
# 		data_to_update = json.loads(data)
# 		response = indexer.update_doc_prop_originals(docid,data_to_update)
# 		web.header('Access-Control-Allow-Origin', '*')
# 		web.header('Access-Control-Allow-Credentials', 'true')
# 		return json.dumps(response)
#
#
#
# class DeleteSport:
#
# 	'''
# 	This class contains the api to remove article from the index when unpublished.
# 	'''
#
# 	def DELETE(self):
#
# 		'''
# 		:param prop:  code for the property for which index is being created
# 		:param docid: id of the document to be deleted from index
# 		:return:
# 		'''
#
# 		i = web.input()
# 		docid,prop = i.docid,i.prop
# 		index_name = get_index_name(prop)
# 		indexer = SearchIndexerOriginals(index_name)
# 		response = indexer.delete_doc_originals(docid)
# 		web.header('Access-Control-Allow-Origin', '*')
# 		web.header('Access-Control-Allow-Credentials', 'true')
# 		return json.dumps(response)
#
#
#
# class MltSport:
#
# 	'''
# 	This class contains the apis which are hit
# for any kind of search from Elastic Search (SWP = '53e4' SWPRTPUB = '25rt')
# 	'''
#
# 	def GET(self):
#
# 		'''
# 		:param q:  query string for search
# 		:return:
# 		'''
#
#
# 		i = web.input(docid='',prop='')
# 		docid,prop = i.docid,i.prop
# 		index_name = get_index_name(prop)
# 		indexer = SearchManagerOriginals(es_client,index_name,ES_CONTENT_DOC_TYPE)
# 		response = indexer.more_like_this_originals(docid,prop)
# 		web.header('Access-Control-Allow-Origin', '*')
# 		web.header('Access-Control-Allow-Credentials', 'true')
# 		return json.dumps(response)
