__author__ = 'monica'

from eswrapper.eswrapper import *
from eswrapper.utils import *
import web
from urls import urls
from eswrapper.settings import *
from paginationspellcheck import *
from originals_index import *


app = web.application(urls, globals())


class Home:

	def GET(self):

		return 'Frozen..... Let it Go... Let it Go... Try search..! :)'



class IndexExists:

	'''

	This class contains the apis which are hit for any kind of search from Elastic Search

	'''

	def GET(self):

		'''

		:param p:  p signifies the property whose index should be hit
		:param q:  query string for search
		:return:
		'''

		data = web.input()

		index_name = get_index_name(data.p)

		indexer = SearchIndexer(index_name)

		response = indexer.check_index_exists()

		print "exists ka response", response

		return json.dumps(response)



class CreateIndex:

	'''

	This class contains the apis which are hit for any kind of search from Elastic Search

	'''

	def POST(self):

		'''

		:param prop:  code for the property for which index is being created
		:param mapping: the mapping dictionary for this index
		:return:
		'''

		print "i come in createindex"
		print "data ius ", web.input()



		data = web.input()

		## we get the code from front end and we create the predefined index name..
		## So for example Property is VB ..code will be
		index_name = get_index_name(data.prop)


		print "index name is ", index_name

		if index_name is None:
			response = {'status': False, 'error': 'Invalid Property Index'}

		else:

			indexer = SearchIndexer(index_name)

			mapping, setting = self._get_index_params(data)

			response = indexer.create_index(mapping, setting)

		print response

		return json.dumps(response)


	def _get_index_params(self, data):

		'''

		:param data:
		:return: mapping: mapping for the Es Index
				 settings: setting for the ES Index
		'''

		# mapping is expected in JSON format
		mapping = get_mapping(data)

		# setting is expected in JSON format
		setting = get_setting(data)

		return mapping, setting





### added classes

class IndexPublishedDraftsArticlesProp:

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
		data,prop = i.data,i.prop
		index_name = get_index_name(prop)
		indexer = SearchIndexer(index_name)
		print data
		data_to_index = json.loads(data)
		response = indexer.index_single_prop(data_to_index,data_to_index['id'])
		print response
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		return json.dumps(response)


class RemoveUnpublishedArticles:

	'''

	This class contains the api to remove article from the index when unpublished.

	'''

	def DELETE(self):

		'''
		:param prop:  code for the property for which index is being created
		:param docid: id of the document to be deleted from index
		:return:
		'''

		i = web.input()
		docid,prop = i.docid,i.prop
		index_name = get_index_name(prop)
		indexer = SearchIndexer(index_name)
		#print docid
		response = indexer.delete_doc(docid)
		print response
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		return json.dumps(response)


class UpdateArticlesDocumentProp:

	'''

	This class contains the api to update article document in index after it is published.

	'''

	def PUT(self):

		'''
		:param prop:  code for the property for which index is being created
		:param docid: id of the document to be updated from index
		:param data: data to be updated
		:return:
		'''

		i = web.input()
		docid,prop,data = i.docid,i.prop,i.data
		index_name = get_index_name(prop)
		indexer = SearchIndexer(index_name)
		#print docid
		data_to_update = json.loads(data)
		#print data_to_update
		response = indexer.update_doc_prop(docid,data_to_update)
		print response
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		return json.dumps(response)



class SearchSWUserFacing:

	'''

	This class contains the apis which are hit for any kind of search from Elastic Search (SWP = '53e4' SWPRTPUB = '25rt')

	'''

	def GET(self):

		'''

		:param pn:  page number
		:param q:  query string for search
		:return:
		'''

		data = web.input(q = '', pn=1, searchtype='', sorttype= 'score')
		response = functiontosearch(data.q,data.pn,data.searchtype,data.sorttype)
		#print response
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		return json.dumps(response)


class SearchVBUserFacing:

	'''

	This class contains the apis which are hit for any kind of search from Elastic Search (SWP = '53e4' SWPRTPUB = '25rt')

	'''

	def GET(self):

		'''

		:param pn:  page number
		:param q:  query string for search
		:return:
		'''

		data = web.input(q = '', pn=1, searchtype='', sorttype= 'score')
		response = functiontosearchVB(data.q,data.pn,data.searchtype,data.sorttype)
		#print response
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		return json.dumps(response)


class SearchGPUserFacing:

	'''

	This class contains the apis for search from Elastic Search for gazabpost

	'''

	def GET(self):

		'''

		:param pn:  page number
		:param q:  query string for search
		:return:
		'''

		data = web.input(q = '', pn=1, searchtype='', sorttype= 'score')
		response = functiontosearchGP(data.q,data.pn,data.searchtype,data.sorttype)
		#print response
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		return json.dumps(response)



class SearchSWPubDrftAuth:

	def GET(self):

		'''

		:param pn:  page number
		:param q:  query string for search
		:param id:  list of ids
		:return:
		'''

		data = web.input(pn=1,q = '',aid='')

		print data.pn
		print data.q
		print data.aid

		response = searchmanfunpubdrftauth(data.pn,data.q,data.aid)
		#print response
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		return json.dumps(response)


class MltDocProp:

	def GET(self):

		'''

		:param id:  id of document
		:return:
		'''

		i = web.input(docid='',category='',prop='')

		#print docid

		response = findmltdocsprop(i.docid,i.prop,i.category)
		#print response
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		return json.dumps(response)


class CreateIndexGP:

	def POST(self):

		i = web.input()
		print i
		prop = i.prop
		print prop
		# data = json.loads(data)
		index_name = get_index_name(prop)
		indexer = SearchIndexer(index_name)

		response = indexer.create_gpindex()
		print response
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		return json.dumps(response)




if UWSGI_SETUP == True:

	application = app.wsgifunc()

else:

	if __name__ == "__main__":
		app.run()
