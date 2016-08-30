__author__ = 'monica'


import json
from datetime import datetime,timedelta
from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import NotFoundError
from defines import *
from settings import *

class SearchIndexer(object):


	def __init__(self, index_name, doc_type =  ES_CONTENT_DOC_TYPE):

		self.index = index_name
		self.type = doc_type

		self.es = es_client

		return

	def create_index(self, mapping = ES_INDEX_MAPPING, settings = ES_INDEX_SETTINGS):

		'''

		:param index_name: name of the index which needs to be created
		:param mapping: the mapping for the ES Index

		:return: status
		'''

		result = {'status': 0, 'index_created': '', 'error': ''}

		try:

			## In case a mapping has not been provided and user wants Elastic Search to use its own mapping
			## for each of the fields

			if(self.check_index_exists() == True):
				result['status'] = 2
				result['index_created'] = self.index
				result['error'] = 'index exists'
				return result

			if (MAPPING_TYPE == USE_NO_MAPPING):
				cr_status = self.es.indices.create(index = self.index)
			else:
				## in case by mistake mapping comes to be None here, we still define our mapping..

				if(mapping is None):
					mapping = ES_INDEX_MAPPING

				index_parameters =  { 'settings': settings, 'mappings': mapping }

				print index_parameters


				cr_status = self.es.indices.create(index = self.index, body = index_parameters)

				if(cr_status.has_key('acknowledged') and cr_status['acknowledged'] == True):
					result['status'] = 1
					result['index_created'] = self.index


		except Exception as (e):
			# TODO: add a logger here
			result['status'] = 0
			result['error'] = str(e)

			print "any exception", str(e)

		return result


	def create_gpindex(self, mapping = ES_INDEX_MAPPING, settings = ES_INDEX_SETTINGS_GP):

		'''

		:param index_name: name of the index which needs to be created
		:param mapping: the mapping for the ES Index

		:return: status
		'''

		result = {'status': 0, 'index_created': '', 'error': ''}

		print mapping
		try:

			print settings
			## In case a mapping has not been provided and user wants Elastic Search to use its own mapping
			## for each of the fields

			if(self.check_index_exists() == True):
				result['status'] = 2
				result['index_created'] = self.index
				result['error'] = 'index exists'
				return result

			if (MAPPING_TYPE == USE_NO_MAPPING):
				cr_status = self.es.indices.create(index = self.index)
			else:
				## in case by mistake mapping comes to be None here, we still define our mapping..

				if(mapping is None):
					mapping = ES_INDEX_MAPPING

				index_parameters =  { 'settings': settings, 'mappings': mapping }

				print index_parameters


				cr_status = self.es.indices.create(index = self.index, body = index_parameters)

				if(cr_status.has_key('acknowledged') and cr_status['acknowledged'] == True):
					result['status'] = 1
					result['index_created'] = self.index


		except Exception as (e):
			# TODO: add a logger here
			result['status'] = 0
			result['error'] = str(e)

			print "any exception", str(e)

		return result



	def check_index_exists(self):

		'''

		:param index_name:
		:return:

		'''

		status = self.es.indices.exists(self.index)



		return status


	def index_single(self, doc_data, doc_id):

		'''

		This API adds a single document to the index

		:param index_name: name of the ES index
		:param type_name: name of the type (ie. the set of documents)
		:param id: id of the document to be indexed
		:return: status

		'''

		results = {'status' : 0, 'err_message': ''}
		try:

			self.es.create(index=self.index, doc_type=self.type, body=doc_data, id=doc_id)

			results['status'] = 1

		except Exception as (e):

			results['status'] = -1
			results['err_message'] = str(e)

		return results



	#### added function for indexing

	def index_single_prop(self, doc_data, doc_id):

		'''

		This API adds a single document to the index

		:param index_name: name of the ES index
		:param type_name: name of the type (ie. the set of documents)
		:param id: id of the document to be indexed
		:return: status

		'''

		results = {'status' : 0, 'err_message': ''}
		try:

			d = datetime.strptime(doc_data['pub_date'], "%B %d, %Y %H:%M:%S")
			datesortform = d.strftime("%Y-%m-%d")

			doc_dict = {'sh_heading': doc_data['sh_heading'], 'ar_id':doc_data['ar_id'], 'title':doc_data['title'],\
			'fImgUrl':doc_data['fImgUrl'], 'tags':doc_data['tags'], 'id':doc_data['id'], 'content':doc_data['content'],\
						'ar_name':doc_data['ar_name'],'swcats':doc_data['swcats'],'ar_url':doc_data['ar_url'],\
						'pub_date':doc_data['pub_date'],'slug':doc_data['slug'], 'date_sort':datesortform}
			self.es.create(index=self.index, doc_type=self.type, body=doc_dict, id=doc_id)

			results['status'] = 1
			# print doc_dict

		except Exception as (e):

			results['status'] = -1
			results['err_message'] = str(e)

		return results


	def index_bulk(self, docs, total):

		'''

		Will be using the bulk insert api of Elasticsearch here and see what happens

		:param json_data:
		:return:
		'''

		actions = []

		if(total == 0 or len(docs) == 0):
			return


		## iterate through the list of docs
		for entry in docs:

			doc_id = entry[ES_FIELD_ID]

			# print entry[ES_FIELD_ID], entry[ES_FIELD_SLUG]


			## TODO log this entry
			if(doc_id is None):
				continue

			action = {
				"_index": self.index,
				"_type": self.type,
				"_id": doc_id,
				"_source": json.dumps(entry)
				}

			actions.append(action)


		helpers.bulk(self.es, actions)

		return

	def delete_doc(self, doc_id):

		'''

		:param id: id of the document which needs to be deleted
		:return:
		'''

		results = {'status' : 0, 'err_message': ''}

		if(id is not None):

			try:

				self.es.delete(self.index, doc_type=self.type, id=doc_id)
				results['status'] = 1

			except Exception as (e):
				#TODO: add logger

				results['status'] = -1
				results['err_message'] = str(e)



		return results

	def update_doc(self, doc_id, doc_data):

		'''

		:param id: id of the document which needs to be deleted
		:return:
		'''

		results = {'status' : 0, 'err_message': ''}

		if(id is not None):

			try:

				self.es.update(self.index, doc_type=self.type, id=doc_id, body={"doc": doc_data})
				results['status'] = 1

			except Exception as (e):
				#TODO: add logger

				results['status'] = -1
				results['err_message'] = str(e)



		return results


	#### added function
	def update_doc_prop(self, doc_id, doc_data):

		'''

		:param id: id of the document which needs to be deleted
		:return:
		'''

		results = {'status' : 0, 'err_message': ''}


		if(id is not None):

			try:

				d = datetime.strptime(doc_data['pub_date'], "%B %d, %Y %H:%M:%S")
				datesortform = d.strftime("%Y-%m-%d")

				doc_dict = {'sh_heading': doc_data['sh_heading'], 'ar_id':doc_data['ar_id'], 'title':doc_data['title'],\
			'fImgUrl':doc_data['fImgUrl'], 'tags':doc_data['tags'], 'content':doc_data['content'],\
						'ar_name':doc_data['ar_name'],'swcats':doc_data['swcats'],'ar_url':doc_data['ar_url'],\
						'pub_date':doc_data['pub_date'],'slug':doc_data['slug'], 'date_sort':datesortform}

				self.es.update(self.index, doc_type=self.type, id=doc_id, body={"doc": doc_dict})
				results['status'] = 1

			except Exception as (e):
				#TODO: add logger

				results['status'] = -1
				results['err_message'] = str(e)



		return results


	#### added function for SW index mapping - add field for date sort
	def update_mapping_SW(self):

		results = {'status' : 0, 'err_message': ''}

		try:

			update_body = {
				  "properties": {
				"date_sort": {
						  "type":   "date",
						  "format": "yyyy-MM-dd"
						}
				}
				}

			self.es.indices.put_mapping(index = self.index, doc_type=self.type, body = update_body)
			results['status'] = 1

		except Exception as (e):
			#TODO: add logger

			results['status'] = -1
			results['err_message'] = str(e)

		return results


###added class
class SearchManagerMultiIndex(object):



	def __init__(self, es_client, doc_type):


		self.type = doc_type
		self.es = es_client

		return


	def _build_field_dismax_list_SW(self, f_dict = None):

		'''

		:param f_dict: dictionary containing the fields and their associated weightages
		:return:

		'''

		f_list = []

		if (f_dict == None):
			f_dict = DEFAULT_SWP_FIELDS_DICT

		for f_name, weight in f_dict.iteritems():
			f_list.append(f_name + "^" + str(weight))

		return f_list


	def _build_field_dismax_list_VB(self, f_dict = None):

		'''

		:param f_dict: dictionary containing the fields and their associated weightages
		:return:

		'''

		f_list = []

		if (f_dict == None):
			f_dict = DEFAULT_VB_FIELDS_DICT

		for f_name, weight in f_dict.iteritems():
			f_list.append(f_name + "^" + str(weight))

		return f_list



	def search_dismax_SW(self, q_str, pgno, fields_dict = None):

		'''

		:param fields_dict: This dictionary contains the weightages to be applied to the different fields
		:return:
		'''

		query_body = {
                                        "bool":{
                                        "should": [
                                        { "match": {"title" : {   "query":  q_str , "fuzziness" : 1 , "operator": "and", "boost": 4}}},
                                        { "bool":  {
                         "should": [
                        { "match": { "tags": { "query" : q_str, "fuzziness" : 1 , "operator": "and" ,  "boost": 3  }}},
                        { "bool":  {
                        "should": [
                                 { "match": { "content": { "query" :  q_str, "fuzziness" : 1 , "operator": "and" , "boost": 2   }}},
                        { "bool":  {
                        "should": [
                                { "match": { "category_display": { "query" :  q_str, "fuzziness" : 1 , "operator": "and"   }}},{ "match": { "ar_name": { "query" : q_str, "fuzziness" : 1 , "operator": "and"  }}}, { "match": { "sh_heading": { "query" :  q_str, "fuzziness" : 1 , "operator": "and"  }}}
                                  ]}}
                                ]}}
                                ]}}
                                         ]}}

		m = 50
		sugestsize = 1
		pgno = int(pgno)

		index_list = SW_INDEX_LIST

		ret_fields = [ ES_FIELD_SH_HEADING, ES_FIELD_AR_ID, ES_FIELD_TAGS, ES_FIELD_AR_URL, ES_FIELD_TITLE, ES_FIELD_SLUG, ES_FIELD_AUTHOR_NAME, ES_FIELD_SWCATS, ES_FIELD_CAT_SLUG, ES_FIELD_DIS_NAME, ES_FIELD_FI_URL, ES_FIELD_PUB_DATE, ES_FIELD_ID ]

		response = self.es.search(index = index_list , doc_type = self.type, body = {"query": query_body}, _source = ret_fields, from_ = (pgno-1)*m , size = m,  sort = ['_score:desc','date_sort:desc'])


		return response


	def search_dismax_SW_latest(self, q_str, pgno, fields_dict = None):

		'''

		:param fields_dict: This dictionary contains the weightages to be applied to the different fields
		:return:
		'''

		query_body = {
                         "bool":{
                                        "should": [
                                        { "match": {"title" : {   "query":  q_str  , "operator": "and", "fuzziness" : 1 , "boost": 4}}},
                                        { "bool":  {
                         "should": [
                        { "match": { "tags": { "query" : q_str, "operator": "and", "fuzziness" : 1 , "boost": 2  }}},
                        { "bool":  {
                        "should": [
                                { "match": { "category_display": { "query" :  q_str , "operator": "and" , "fuzziness" : 1   }}},{ "match": { "ar_name": { "query" : q_str, "operator": "and" , "fuzziness" : 1   }}}, { "match": { "sh_heading": { "query" :  q_str, "fuzziness" : 1 , "operator": "and" ,   }}}
                                ]}}
                                ]}}
                                         ]}
                }
		

		m = 50
		sugestsize = 1
		pgno = int(pgno)

		index_list = SW_INDEX_LIST

		ret_fields = [ ES_FIELD_SH_HEADING, ES_FIELD_AR_ID, ES_FIELD_TAGS, ES_FIELD_AR_URL, ES_FIELD_TITLE, ES_FIELD_SLUG, ES_FIELD_AUTHOR_NAME, ES_FIELD_SWCATS, ES_FIELD_CAT_SLUG, ES_FIELD_DIS_NAME, ES_FIELD_FI_URL, ES_FIELD_PUB_DATE, ES_FIELD_ID ]

		response = self.es.search(index = index_list , doc_type = self.type, body = {"query": query_body}, _source = ret_fields, from_ = (pgno-1)*m , size = m, sort = ['date_sort:desc'])
	

		count = response['hits']['total']
                if count == 0 :
                        query_body = {
                                "bool":{
                                "should": [
                                { "match": {"content" : {   "query":  q_str  , "operator": "and", "fuzziness" : 1 }}}
                                ]}}
                response = self.es.search(index = index_list , doc_type = self.type, body = {"query": query_body}, _source = ret_fields, from_ = (pgno-1)*m , size = m, sort = ['date_sort:desc'])
	
		return response


	def search_dismax_VB(self, q_str, pgno, fields_dict = None):

		'''

		:param fields_dict: This dictionary contains the weightages to be applied to the different fields
		:return:
		'''

		query_body = {
                                        "bool":{
                                        "should": [
                                        { "match": {"title" : {   "query":  q_str , "fuzziness" : 1 , "operator": "and", "boost": 4}}},
                                        { "bool":  {
                         "should": [
                        { "match": { "tags": { "query" : q_str, "fuzziness" : 1 , "operator": "and" ,  "boost": 3  }}},
                        { "bool":  {
                        "should": [
                                 { "match": { "content": { "query" :  q_str, "fuzziness" : 1 , "operator": "and" , "boost": 2   }}},
                        { "bool":  {
                        "should": [
                                { "match": { "category_display": { "query" :  q_str, "fuzziness" : 1 , "operator": "and"   }}},{ "match": { "ar_name": { "query" : q_str, "fuzziness" : 1 , "operator": "and"  }}}, { "match": { "sh_heading": { "query" :  q_str, "fuzziness" : 1 , "operator": "and"  }}}
                                  ]}}
                                ]}}
                                ]}}
                                         ]}}

		m = 48
		sugestsize = 1
		pgno = int(pgno)

		index_list = VB_INDEX_LIST

		ret_fields = [ ES_FIELD_SH_HEADING, ES_FIELD_AR_ID, ES_FIELD_TAGS, ES_FIELD_AR_URL, ES_FIELD_TITLE, ES_FIELD_SLUG, ES_FIELD_AUTHOR_NAME,\
					   ES_FIELD_SWCATS, ES_FIELD_CAT_SLUG, ES_FIELD_DIS_NAME, ES_FIELD_FI_URL, ES_FIELD_PUB_DATE, ES_FIELD_ID ]

		response = self.es.search(index = index_list , doc_type = self.type, body = {"query": query_body}, _source = ret_fields, from_ = (pgno-1)*m , size = m, sort = ['_score:desc','date_sort:desc'])


		return response


	def search_dismax_VB_latest(self, q_str, pgno, fields_dict = None):

		'''

		:param fields_dict: This dictionary contains the weightages to be applied to the different fields
		:return:
		'''

		query_body = {
                         "bool":{
                                        "should": [
                                        { "match": {"title" : {   "query":  q_str  , "operator": "and", "fuzziness" : 1 , "boost": 4}}},
                                        { "bool":  {
                         "should": [
                        { "match": { "tags": { "query" : q_str, "operator": "and", "fuzziness" : 1 , "boost": 2  }}},
                        { "bool":  {
                        "should": [
                                { "match": { "category_display": { "query" :  q_str , "operator": "and" , "fuzziness" : 1   }}},{ "match": { "ar_name": { "query" : q_str, "operator": "and" , "fuzziness" : 1   }}}, { "match": { "sh_heading": { "query" :  q_str, "fuzziness" : 1 , "operator": "and" ,   }}}
                                ]}}
                                ]}}
                                         ]}
                }


		m = 48
		sugestsize = 1
		pgno = int(pgno)

		index_list = VB_INDEX_LIST

		ret_fields = [ ES_FIELD_SH_HEADING, ES_FIELD_AR_ID, ES_FIELD_TAGS, ES_FIELD_AR_URL, ES_FIELD_TITLE, ES_FIELD_SLUG, ES_FIELD_AUTHOR_NAME,\
					   ES_FIELD_SWCATS, ES_FIELD_CAT_SLUG, ES_FIELD_DIS_NAME, ES_FIELD_FI_URL, ES_FIELD_PUB_DATE, ES_FIELD_ID ]

		response = self.es.search(index = index_list , doc_type = self.type, body = {"query": query_body}, _source = ret_fields, from_ = (pgno-1)*m , size = m, sort = ['date_sort:desc'])


		count = response['hits']['total']
                if count == 0 :
                        query_body = {
                                "bool":{
                                "should": [
                                { "match": {"content" : {   "query":  q_str  , "operator": "and", "fuzziness" : 1 }}}
                                ]}}
                response = self.es.search(index = index_list , doc_type = self.type, body = {"query": query_body}, _source = ret_fields, from_ = (pgno-1)*m , size = m, sort = ['date_sort:desc'])


		return response


	def search_dismax_VBarticle(self, q_str, pgno, fields_dict = DEFAULT_SWP_FIELDS_DICT_ARTICLE):

		'''

		:param fields_dict: This dictionary contains the weightages to be applied to the different fields
		:return:
		'''

		f_list = self._build_field_dismax_list_VB(fields_dict)

		query_body = {

			"query_string" : {

				"fields" : f_list,
				"query" : q_str,
				"use_dis_max" : True

			}
		}

		m = 48
		sugestsize = 1
		pgno = int(pgno)

		index_list = VB_INDEX_LIST

		response = self.es.search(index = index_list , doc_type = self.type, body = {"query": query_body}, _source = 'true', from_ = (pgno-1)*m , size = m, suggest_text = q_str, suggest_field = '_all', suggest_size = sugestsize)


		return response


	def search_dismax_VBauthor(self, q_str, pgno, fields_dict = None):

		'''

		:param fields_dict: This dictionary contains the weightages to be applied to the different fields
		:return:
		'''

		f_list = [ES_FIELD_AUTHOR_NAME]

		query_body = {

			"query_string" : {

			"fields" : f_list,
			"query" : q_str,
			   # "match_all" : {}
			"use_dis_max" : True

			}
		}


		m = 50
		sugestsize = 1
		pgno = int(pgno)

		index_list = VB_INDEX_LIST

		response = self.es.search(index = index_list , doc_type = self.type, body = {"query": query_body}, _source = 'true', from_ = (pgno-1)*m , size = m, suggest_text = q_str, suggest_field = ES_FIELD_AUTHOR_NAME, suggest_size = sugestsize)


		return response



	def search_dismax_VBcategory(self, q_str, pgno, fields_dict = None):

		'''

		:param fields_dict: This dictionary contains the weightages to be applied to the different fields
		:return:
		'''

		f_list = [ES_FIELD_CATS]

		query_body = {

			"query_string" : {

			"fields" : f_list,
			"query" : q_str,
			   # "match_all" : {}
			"use_dis_max" : True

			}
		}


		m = 50
		sugestsize = 1
		pgno = int(pgno)

		index_list = VB_INDEX_LIST

		response = self.es.search(index = index_list , doc_type = self.type, body = {"query": query_body}, _source = 'true', from_ = (pgno-1)*m , size = m, suggest_text = q_str, suggest_field = ES_FIELD_CATS, suggest_size = sugestsize)


		return response



	def search_dismax_GP(self, q_str, pgno, fields_dict = None):

		'''

		:param fields_dict: This dictionary contains the weightages to be applied to the different fields
		:return:
		'''

		f_list = self._build_field_dismax_list_VB(fields_dict)

		query_body = {

			"query_string" : {

				"fields" : f_list,
				"query" : q_str,
				"use_dis_max" : True

			}
		}

		m = 50
		sugestsize = 1
		pgno = int(pgno)

		index_list = GP_INDEX_LIST

		ret_fields = [ ES_FIELD_SH_HEADING, ES_FIELD_AR_ID, ES_FIELD_TAGS, ES_FIELD_AR_URL, ES_FIELD_TITLE, ES_FIELD_SLUG, ES_FIELD_AUTHOR_NAME,\
					   ES_FIELD_SWCATS, ES_FIELD_CAT_SLUG, ES_FIELD_DIS_NAME, ES_FIELD_FI_URL, ES_FIELD_PUB_DATE, ES_FIELD_ID ]

		response = self.es.search(index = index_list , doc_type = self.type, body = {"query": query_body}, _source = ret_fields, from_ = (pgno-1)*m , size = m, suggest_text = q_str, suggest_field = '_all', suggest_size = sugestsize, sort = ['_score:desc','date_sort:desc'])


		return response


	def search_dismax_GP_latest(self, q_str, pgno, fields_dict = None):

		'''

		:param fields_dict: This dictionary contains the weightages to be applied to the different fields
		:return:
		'''

		query_body = {
					"bool":{
					"should": [
					{ "match_phrase": { "title":  q_str }},
						{ "bool":  {
			 "should": [
			{ "match_phrase": { "tags": q_str   }},
			{ "bool":  {
			 "should": [
			 { "match_phrase": { "ar_name": q_str   }},
			{ "bool":  {
			"should": [
				{ "match_phrase": { "category_display":  q_str}}, { "match_phrase": { "sh_heading": q_str   }}
				 ] 
				}}

				]
			}}
				 ] }}
					]
					}
		}


		m = 50
		sugestsize = 1
		pgno = int(pgno)

		index_list = GP_INDEX_LIST

		ret_fields = [ ES_FIELD_SH_HEADING, ES_FIELD_AR_ID, ES_FIELD_TAGS, ES_FIELD_AR_URL, ES_FIELD_TITLE, ES_FIELD_SLUG, ES_FIELD_AUTHOR_NAME,\
					   ES_FIELD_SWCATS, ES_FIELD_CAT_SLUG, ES_FIELD_DIS_NAME, ES_FIELD_FI_URL, ES_FIELD_PUB_DATE, ES_FIELD_ID ]

		response = self.es.search(index = index_list , doc_type = self.type, body = {"query": query_body}, _source = ret_fields, from_ = (pgno-1)*m , size = m, suggest_text = q_str, suggest_field = '_all', suggest_size = sugestsize, sort = ['date_sort:desc'])


		count = response['hits']['total']
		if count == 0 :
			query_body = {
				"bool":{
				"should": [
				{ "match_phrase": { "content": q_str   }}
				]}}
			response = self.es.search(index = index_list , doc_type = self.type, body = {"query": query_body}, _source = ret_fields, from_ = (pgno-1)*m , size = m, suggest_text = q_str, suggest_field = '_all', suggest_size = sugestsize, sort = ['date_sort:desc'])


		return response


	def checkauthsearch(self,aeid,q_str,pgno,fields_dict = None):

		'''

		:param fields_dict: This dictionary contains the weightages to be applied to the different fields
		:param aeid: list of author-ids, for cms
		:return:
		'''


		f_list = self._build_field_dismax_list_SW(fields_dict)

		index_list = ['swp_realtimeposts','swp_realtimedrafts']

		m = 50
		sugestsize = 1
		pgno = int(pgno)
		print type(aeid)

		aeids = ' '.join(aeid)
		print aeids

		response = self.es.search(index = index_list , doc_type = self.type,\
									  body = {"query":{
										  "bool":{"must":
													  [{"match":{"ar_id":aeids}},
													   {"multi_match":{"query":q_str,
																	   "fields":f_list}}]
																	   }}},\
									  _source = 'true',from_ = (pgno-1)*m , size = m,\
								  suggest_text = q_str, suggest_field = '_all', suggest_size = sugestsize)

		return response


	def more_like_this_prop(self, doc_id, prop, category, stopwords = None ):

		'''
		:param id: id of the document for which we are searching similar documents
		:return: resulting documents..

		'''

		nowtime = datetime.now()
		dtoday = nowtime.strftime("%Y-%m-%d")
		#print dtoday
		#print type(dtoday)

		mod_time = datetime.now() + timedelta(days=-(2))
		dbac = datetime.strftime(mod_time, "%Y-%m-%d")
		#print dbac
		#print type(dbac)

		index_list = []

		ret_fields = [ ES_FIELD_SH_HEADING, ES_FIELD_AR_ID, ES_FIELD_TAGS, ES_FIELD_AR_URL, ES_FIELD_TITLE, ES_FIELD_SLUG, ES_FIELD_AUTHOR_NAME, ES_FIELD_SWCATS, ES_FIELD_CAT_SLUG, ES_FIELD_DIS_NAME, ES_FIELD_FI_URL, ES_FIELD_PUB_DATE, ES_FIELD_DATE_SORT, ES_FIELD_ID ]

		if prop == VB :
			index_list = VB_INDEX_LIST
			stopwords = ES_MLT_STOPWORDS

		if prop == GPRT :
			index_list = GP_INDEX_LIST

		if prop == SWPRTPUB :
			index_list = SW_INDEX_LIST
			stopwords = ES_MLT_STOPWORDS



		if category == 'news' :

			# print "news"
			query_body =  {
						"query": {
									"filtered": {
							"query":{
								"more_like_this" : {
									"fields" : ["tags", "title","content"],
							"docs": [{"_id" : doc_id}],
										"min_term_freq" : ES_MLT_MIN_TERM_FREQ,
										 "max_query_terms" : ES_MLT_MAX_QUERY_TERMS,
										"stop_words" : stopwords,
										  "include" : False
								}
							}
										,
							"filter":{
								"query":{"range":{  "date_sort":{ "lte":dtoday,"gte":dbac}   }}
									}
			}}}

			response = self.es.search(index = index_list , doc_type = self.type,\
														  body = query_body, _source = ret_fields, sort = ['date_sort:desc','_score:desc']
														)
			res = self.remove_news_article_from_mlt(response)

			count = response['hits']['total']
			if count == 0 :
				query_body =  {
                                                "query": {
                                                                        "filtered": {
                                                        "query":{
                                                                "match":{"swcats.category_slug":"news"}
                                                        }
                                                                                ,
                                                        "filter":{
                                                                "query":{"range":{  "date_sort":{ "lte":dtoday,"gte":dbac}   }}
                                                                        }
                        }}}

                        	response = self.es.search(index = index_list , doc_type = self.type,\
                                                                                                                  body = query_body, _source = ret_fields, sort = ['date_sort:desc','_score:desc']
                                                                                                                )
				#self.remove_same_news_article_from_mlt_when_no_mlt_found(doc_id,response)
				res = self.remove_news_article_from_mlt(response)
		


		else :

			query_body = {"query":{
								  "more_like_this" : {
										 "fields" : ["title","tags","content"],
								  "docs" : [
									  {
										 "_id" : doc_id
									  }
								  ],
									"min_term_freq" : ES_MLT_MIN_TERM_FREQ,
									 "max_query_terms" : ES_MLT_MAX_QUERY_TERMS,
									"stop_words" : stopwords,
									  "include" : False
								  }
							  }
							  }


			response = self.es.search(index = index_list , doc_type = self.type,\
							  body = query_body, _source = ret_fields,sort = ['_score:desc','date_sort:desc'])


			res = self.remove_news_article_from_mlt(response)

		return res





	def remove_news_article_from_mlt(self,listofmltarticles) :


                mod_time = datetime.now() + timedelta(days=-(2))
                dbac = datetime.strftime(mod_time, "%Y-%m-%d")	

		try : 

			newrecodict = {'hits':{}}

			listmodify = listofmltarticles['hits']['hits']

			for lmt in listmodify :

					for cs in lmt['_source']['swcats'] :
						#print cs
						if cs['category_slug'] == 'news' and lmt['_source']['date_sort'] < dbac :
							lmt.clear()
			listmodify = filter(None, listmodify)

			newrecodict['hits']['hits'] = listmodify
			return newrecodict

		except Exception as e :
			print str(e)





	def remove_same_news_article_from_mlt_when_no_mlt_found(self,docid,listofmltarticles) :

		try : 

			for lmt in listofmltarticles['hits']['hits'] :

				if lmt['_id'] == docid :
					listofmltarticles.remove(lmt)

		except Exception as e : 
			print str(e)
