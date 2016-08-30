import ast
from eswrapper.eswrapper import *
from eswrapper.originals_eswrapper import *

search_mgr = SearchManagerMultiIndex(es_client, ES_CONTENT_DOC_TYPE)


def functiontosearch(q,pn,searchtype,sorttype):

	data = {'info': {}, 'next_page': '', 'errmsg': '', 'status':0}

	try:
		mj = []
		# search function called with arguments
		if searchtype == '' and sorttype == 'score':
			data['info'] = search_mgr.search_dismax_SW(q,pn)

		if searchtype == '' and sorttype == 'latest':
			data['info'] = search_mgr.search_dismax_SW_latest(q,pn)

		if data['info']['hits']['total'] < 50 :
			data['next_page'] = -1
		else:
			data['next_page'] = nextPage(data['info']['hits']['hits'], pn)
		data['status'] = 1

	except Exception as (e):
		data['errmsg'] = str(e)
		data['status'] = 0
		data['info'] = {}


	#print data
	return data


def functiontosearchVB(q,pn,searchtype,sorttype):

	data = {'info': {}, 'next_page': '', 'errmsg': '', 'status':0}

	try:
		mj = []
		# search function called with arguments
		if searchtype == '' and sorttype == 'score':
			data['info'] = search_mgr.search_dismax_VB(q,pn)
		elif searchtype == '' and sorttype == 'latest':
			data['info'] = search_mgr.search_dismax_VB_latest(q,pn)
		elif searchtype == 'article':
			data['info'] = search_mgr.search_dismax_VBarticle(q,pn)
			mj = data["info"]["suggest"]["_all"]
		elif searchtype == 'author':
			data['info'] = search_mgr.search_dismax_VBauthor(q,pn)
			mj = data["info"]["suggest"]["ar_name"]
		elif searchtype == 'category':
			data['info'] = search_mgr.search_dismax_VBcategory(q,pn)
			mj = data["info"]["suggest"]["cats"]
		else :
			data['info'] = 'No Such Searchtype exists'

		'''sug_li = []
		for s in mj:
			if s["options"]:
				for o in s["options"]:
					sug_li.append(o["text"])

		if len(sug_li) != 0:
			data['showresultsfor'] = sug_li[0]

		for s in sug_li:
			if searchtype == '' and sorttype == 'score':
				data['info'] = search_mgr.search_dismax_VB(s,pn)
			elif searchtype == '' and sorttype == 'latest':
				data['info'] = search_mgr.search_dismax_VB_latest(s,pn)
			elif searchtype == 'article':
				data['info'] = search_mgr.search_dismax_VBarticle(s,pn)
			elif searchtype == 'author':
				data['info'] = search_mgr.search_dismax_VBauthor(s,pn)
			elif searchtype == 'category':
				data['info'] = search_mgr.search_dismax_VBcategory(s,pn)
			else :
				data['info'] = 'No Such Searchtype exists' '''

		if data['info']['hits']['total'] < 50 :
			data['next_page'] = -1
		else:
			data['next_page'] = nextPage(data['info']['hits']['hits'], pn)
		#data['next_page'] = nextPage(data['info']['hits']['hits'], pn)
		data['status'] = 1

	except Exception as (e):
		data['errmsg'] = str(e)
		data['status'] = 0
		data['info'] = {}


	#print data
	return data



def functiontosearchGP(q,pn,searchtype,sorttype):

	data = {'info': {}, 'next_page': '', 'showresultsfor': '', 'errmsg': '', 'status':0}

	try:
		mj = []
		# search function called with arguments
		if searchtype == '' and sorttype == 'score':
			data['info'] = search_mgr.search_dismax_GP(q,pn)
			mj = data["info"]["suggest"]["_all"]

		if searchtype == '' and sorttype == 'latest':
			data['info'] = search_mgr.search_dismax_GP_latest(q,pn)
			mj = data["info"]["suggest"]["_all"]

		sug_li = []
		for s in mj:
			if s["options"]:
				for o in s["options"]:
					sug_li.append(o["text"])

		if len(sug_li) != 0:
			data['showresultsfor'] = sug_li[0]

		for s in sug_li:
			if searchtype == '' and sorttype == 'score':
				data['info'] = search_mgr.search_dismax_GP(s,pn)

			if searchtype == '' and sorttype == 'latest':
				data['info'] = search_mgr.search_dismax_GP_latest(s,pn)

		if data['info']['hits']['total'] < 50 :
			data['next_page'] = -1
		else:
			data['next_page'] = nextPage(data['info']['hits']['hits'], pn)
		#data['next_page'] = nextPage(data['info']['hits']['hits'], pn)
		data['status'] = 1

	except Exception as (e):
		data['errmsg'] = str(e)
		data['status'] = 0
		data['info'] = {}


	#print data
	return data



def searchmanfunpubdrftauth(pn,q, auth):
	'''returns the search result, page number and mis-spelt word correction '''

	data = {'info': {}, 'next_page': '', 'showresultsfor': '', 'errmsg': '', 'status':0}

	try:


		ids = ast.literal_eval(auth)
		print ids
		if type(ids) is list:
			print "id is list"
					# search function called with arguments
			data['info'] = search_mgr.checkauthsearch(ids,q,pn)
			#print data['info']['hits']

			sug_li = []
			for s in data["info"]["suggest"]["_all"]:
				if s["options"]:
					for o in s["options"]:
						sug_li.append(o["text"])

			if len(sug_li) != 0:
				data['showresultsfor'] = sug_li[0]

			for s in sug_li:
				data['info'] = search_mgr.checkauthsearch(ids,s, pn)

			data['next_page'] = nextPage(data['info']['hits']['hits'], pn)
			data['status'] = 1

		else :
			data['info'] = ''
			data['status'] = 0
			data['showresultsfor'] = ''
			data['next_page'] = ''
			data['errmsg'] = 'ids should be in a list of string'


	except Exception as (e):
		data['errmsg'] = str(e)
		data['status'] = 0
		data['info'] = {}


	#print data
	return data



def nextPage(data, pn):
	'''function to determine the next page number'''

	if data == []:
		next_page = -1
	else:
		next_page = int(pn) + 1
	return next_page


def findmltdocsprop(docid,prop,category):

	data = {'info': {},'status':0,'errmsg':''}

	try :

		data['info'] = search_mgr.more_like_this_prop(docid,prop,category)

		if data['info'] is not None :
			data['status'] = 1
		else :
			data['status'] = 0
			data['errmsg'] = 'error parameters, prop'

		return data

	except Exception as e :

		data['errmsg'] = str(e)

		return data



#ORIGINALS FUNTION TO SEARCH
def functiontosearchORIGINALS(q,pn,searchtype,sorttype):

	data = {'info': {}, 'next_page': '', 'errmsg': '', 'status':0}

	try:

		index_name = SWORI_INDEX_LIST

		search_mgr_originals = SearchManagerOriginals(es_client,index_name,ES_CONTENT_DOC_TYPE)

		# search function called with arguments
		if searchtype == '' and sorttype == 'score':
			data['info'] = search_mgr_originals.search_dismax_OR(q,pn)

		if searchtype == '' and sorttype == 'latest':
			data['info'] = search_mgr_originals.search_dismax_OR_latest(q,pn)

		if data['info']['hits']['total'] < 50 :
			data['next_page'] = -1
		else:
			data['next_page'] = nextPage(data['info']['hits']['hits'], pn)
		data['status'] = 1

	except Exception as (e):
		data['errmsg'] = str(e)
		data['status'] = 0
		data['info'] = {}


	#print data
	return data