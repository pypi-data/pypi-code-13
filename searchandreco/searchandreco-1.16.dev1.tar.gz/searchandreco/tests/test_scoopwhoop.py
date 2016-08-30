from base import *
from ..eswrapper.utils import *
from ..eswrapper.eswrapper import *
from ..paginationspellcheck import *

## the prop value for scoopwhoop is 25rt
PROP = '25rt'


def functionToGetIdCatMLT():

	q = 'scoopwhoop'
	pn=1
	searchtype=''
	sorttype= 'score'
	response = functiontosearch(q,pn,searchtype,sorttype)

	return response['info']


class TestScoopwhoop(SearchDbTestCase):

	#1 index article into es (all fields of data variable present)
	def test_indexArticle(self):

		data_to_index = {"id":"5694b6aa2d07dfc5072cb4bc","slug":"slug","ar_url":"ar_url","ar_name":"ar_name","content":"content","tags":["tags"],"fImgUrl":"fImgurl","title":"title","ar_id":"12","sh_heading":"123","pub_date":"June 04, 2015 13:39:33","swcats":[{"category_display":"category_dis","category_slug":"category_slug"},{"category_display":"vid","category_slug":"vid"}]}
		index_name = get_index_name(PROP)
		indexer = SearchIndexer(index_name)
		response = indexer.index_single_prop(data_to_index,data_to_index['id'])
		# print "Scoopwhoop Indexed Article Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,1)


	#2 index article into es - document already exists (all fields of data variable present)
	def test_indexArticle_exists(self):

		data_to_index = {"id":"5694b6aa2d07dfc5072cb4bc","slug":"slug","ar_url":"ar_url","ar_name":"ar_name","content":"content","tags":["tags"],"fImgUrl":"fImgurl","title":"title","ar_id":"12","sh_heading":"123","pub_date":"June 04, 2015 13:39:33","swcats":[{"category_display":"category_dis","category_slug":"category_slug"},{"category_display":"vid","category_slug":"vid"}]}
		index_name = get_index_name(PROP)
		indexer = SearchIndexer(index_name)
		response = indexer.index_single_prop(data_to_index,data_to_index['id'])
		# print "Scoopwhoop Indexed Article Already Exists Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,-1)


	#3 index article into es - (any of the fields of data variable is not present - ex: fImgUrl)
	def test_indexArticle_check_data_format(self):

		data_to_index = {"id":"7694b6aa2d07dfc5072cb4bc","slug":"slug","ar_url":"ar_url","ar_name":"ar_name","content":"content","tags":["tags"],"title":"title","ar_id":"12","sh_heading":"123","pub_date":"June 04, 2015 13:39:33","swcats":[{"category_display":"category_dis","category_slug":"category_slug"},{"category_display":"vid","category_slug":"vid"}]}
		index_name = get_index_name(PROP)
		indexer = SearchIndexer(index_name)
		response = indexer.index_single_prop(data_to_index,data_to_index['id'])
		# print "Scoopwhoop Indexed Article All Data Fields Not Present Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,-1)


	#4 index article into es - (extra fields of data variable is present - ex: version)
	def test_indexArticle_check_data_format_extra_field(self):

		data_to_index = {"id":"7694b6aa2d07dfc5072cb4bc","slug":"slug","ar_url":"ar_url","version":"version","ar_name":"ar_name","content":"content","tags":["tags"],"fImgUrl":"fImgurl","title":"title","ar_id":"12","sh_heading":"123","pub_date":"June 04, 2015 13:39:33","swcats":[{"category_display":"category_dis","category_slug":"category_slug"},{"category_display":"vid","category_slug":"vid"}]}
		index_name = get_index_name(PROP)
		indexer = SearchIndexer(index_name)
		response = indexer.index_single_prop(data_to_index,data_to_index['id'])
		# print "Scoopwhoop Indexed Article Extra Data Fields Present Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,1)


	#5 index article into es - (the datatype of fields of data variable - ex: content:string, category:nested object and so on..)
	def test_indexArticle_check_data_format_type_content_not_string(self):

		data_to_index = {"id":"d694b6aa2d07dfc5072cb4bc","slug":"slug","ar_url":"ar_url","ar_name":"ar_name","content":[{"category_display":"category_dis","category_slug":"category_slug"},{"category_display":"vid","category_slug":"vid"}],"tags":["tags"],"fImgUrl":"fImgurl","title":"title","ar_id":"12","sh_heading":"123","pub_date":"June 04, 2015 13:39:33","swcats":[{"category_display":"category_dis","category_slug":"category_slug"},{"category_display":"vid","category_slug":"vid"}]}
		index_name = get_index_name(PROP)
		indexer = SearchIndexer(index_name)
		response = indexer.index_single_prop(data_to_index,data_to_index['id'])
		# print "Scoopwhoop Indexed Article datatype of Data Fields Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,-1)


	#6 index article into es (the datatype of fields of data variable - date fields : pub_date : "June 04, 2015 13:39:33" format , datesortform)
	def test_indexArticle_check_data_format_type_date(self):

		data_to_index = {"id":"dateb6aa2d07dfc5072cb4bc","slug":"slug","ar_url":"ar_url","ar_name":"ar_name","content":"content","tags":["tags"],"fImgUrl":"fImgurl","title":"title","ar_id":"12","sh_heading":"123","pub_date":"Jan 04 2015 13:39:33","swcats":[{"category_display":"category_dis","category_slug":"category_slug"},{"category_display":"vid","category_slug":"vid"}]}
		index_name = get_index_name(PROP)
		indexer = SearchIndexer(index_name)
		response = indexer.index_single_prop(data_to_index,data_to_index['id'])
		# print "Scoopwhoop Indexed Article Date Format Not proper Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,-1)


	#7 remove article from es
	def test_removeArticle(self):

		docid = '5694b6aa2d07dfc5072cb4bc'
		prop = PROP
		index_name = get_index_name(prop)
		indexer = SearchIndexer(index_name)
		response = indexer.delete_doc(docid)
		# print "Scoopwhoop Remove Article Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,1)


	#8 remove article from es - when document is not present in es
	def test_removeArticle_again(self):

		docid = '5694b6aa2d07dfc5072cb4bc'
		prop = PROP
		index_name = get_index_name(prop)
		indexer = SearchIndexer(index_name)
		response = indexer.delete_doc(docid)
		# print "Scoopwhoop Remove Article Which is not in es database Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,-1)


	#9 index article into es - to test edit
	def test_editArticle_1(self):

		data_to_index = {"id":"5694b6edit07dfc5072cb4bc","slug":"slug","ar_url":"ar_url","ar_name":"ar_name","content":"content","tags":["tags"],"fImgUrl":"fImgurl","title":"title","ar_id":"12","sh_heading":"123","pub_date":"June 04, 2015 13:39:33","swcats":[{"category_display":"category_dis","category_slug":"category_slug"},{"category_display":"vid","category_slug":"vid"}]}
		index_name = get_index_name(PROP)
		indexer = SearchIndexer(index_name)
		response = indexer.index_single_prop(data_to_index,data_to_index['id'])
		# print "Scoopwhoop Indexed Article Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,1)


	#10 edit article info - es (proper data sent, docid exists)
	def test_editArticle_2(self):

		docid = '5694b6edit07dfc5072cb4bc'
		prop = PROP
		data_to_update = {"slug":"slug","ar_url":"ar_url","ar_name":"ar_name_edit","content":"content","tags":["tags"],"fImgUrl":"fImgurl_edit","title":"title","ar_id":"12","sh_heading":"123","pub_date":"June 04, 2015 13:39:33","swcats":[{"category_display":"category_dis","category_slug":"category_slug"},{"category_display":"vid","category_slug":"vid"}]}
		index_name = get_index_name(prop)
		indexer = SearchIndexer(index_name)
		response = indexer.update_doc_prop(docid,data_to_update)
		# print "Scoopwhoop Edited Article Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,1)


	#11 edit article info - es (proper data sent, docid does not exist)
	def test_editArticle_3(self):

		docid = '5694b6edit07idc5072cb4bc'
		prop = PROP
		data_to_update = {"slug":"slug","ar_url":"ar_url","ar_name":"ar_name_edit","content":"content","tags":["tags"],"fImgUrl":"fImgurl_edit","title":"title","ar_id":"12","sh_heading":"123","pub_date":"June 04, 2015 13:39:33","swcats":[{"category_display":"category_dis","category_slug":"category_slug"},{"category_display":"vid","category_slug":"vid"}]}
		index_name = get_index_name(prop)
		indexer = SearchIndexer(index_name)
		response = indexer.update_doc_prop(docid,data_to_update)
		# print "Scoopwhoop Edited Article docid not present Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,-1)


	#12 edit article info - es (data dict - missing field sent (ex : fImgUrl), docid exists)
	def test_editArticle_4(self):

		docid = '5694b6edit07dfc5072cb4bc'
		prop = PROP
		data_to_update = {"slug":"slug","ar_url":"ar_url","ar_name":"ar_name_edit","content":"content","tags":["tags"],"title":"title","ar_id":"12","sh_heading":"123","pub_date":"June 04, 2015 13:39:33","swcats":[{"category_display":"category_dis","category_slug":"category_slug"},{"category_display":"vid","category_slug":"vid"}]}
		index_name = get_index_name(prop)
		indexer = SearchIndexer(index_name)
		response = indexer.update_doc_prop(docid,data_to_update)
		# print "Scoopwhoop Edited Article Missing field in data dict Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,-1)


	#13 edit article info - es (data sent - extra field : version, docid exists)
	def test_editArticle_5(self):

		docid = '5694b6edit07dfc5072cb4bc'
		prop = PROP
		data_to_update = {"slug":"slug","ar_url":"ar_url","ar_name":"ar_name_edit","version":"version","content":"content-edit","tags":["tags"],"fImgUrl":"fImgurl_edit","title":"title","ar_id":"12","sh_heading":"123","pub_date":"June 04, 2015 13:39:33","swcats":[{"category_display":"category_dis","category_slug":"category_slug"},{"category_display":"vid","category_slug":"vid"}]}
		index_name = get_index_name(prop)
		indexer = SearchIndexer(index_name)
		response = indexer.update_doc_prop(docid,data_to_update)
		# print "Scoopwhoop Edited Article containing extra field Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,1)


	#14 edit article info - es (the datatype of fields of data variable - ex: content:string, category:nested object, docid exists)
	def test_editArticle_6(self):

		docid = '5694b6edit07dfc5072cb4bc'
		prop = PROP
		data_to_update = {"slug":"slug","ar_url":"ar_url","ar_name":"ar_name_edit","content":[{"category_display":"category_dis","category_slug":"category_slug"},{"category_display":"vid","category_slug":"vid"}],"tags":["tags"],"fImgUrl":"fImgurl_edit","title":"title","ar_id":"12","sh_heading":"123","pub_date":"June 04, 2015 13:39:33","swcats":[{"category_display":"category_dis","category_slug":"category_slug"},{"category_display":"vid","category_slug":"vid"}]}
		index_name = get_index_name(prop)
		indexer = SearchIndexer(index_name)
		response = indexer.update_doc_prop(docid,data_to_update)
		# print "Scoopwhoop Edited Article containing content field as list of dict and not string Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,-1)


	#15 edit article info - es (data sent - date fields : pub_date : "June 04, 2015 13:39:33" format, docid exists)
	def test_editArticle_7(self):

		docid = '5694b6edit07dfc5072cb4bc'
		prop = PROP
		data_to_update = {"slug":"slug","ar_url":"ar_url","ar_name":"ar_name_edit","content":"content","tags":["tags"],"fImgUrl":"fImgurl_edit","title":"title","ar_id":"12","sh_heading":"123","pub_date":"Jan 04 2015 13:39","swcats":[{"category_display":"category_dis","category_slug":"category_slug"},{"category_display":"vid","category_slug":"vid"}]}
		index_name = get_index_name(prop)
		indexer = SearchIndexer(index_name)
		response = indexer.update_doc_prop(docid,data_to_update)
		# print "Scoopwhoop Edited Article with improper date format Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,-1)


	#16 search published article - es // searchtype: for future, can be article,category,author... ,
	def test_searchArticle_1(self):

		q = 'scoopwhoop'
		pn=1
		searchtype=''
		sorttype= 'score'
		response = functiontosearch(q,pn,searchtype,sorttype)
		# print "Scoopwhoop Search Articles Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,1)

	#17 search published article - es // searchtype: for future, can be article,category,author... , pn=2
	def test_searchArticle_2(self):

		q = 'scoopwhoop'
		pn=2
		searchtype=''
		sorttype= 'score'
		response = functiontosearch(q,pn,searchtype,sorttype)
		# print "Scoopwhoop Search Articles Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,1)


	#18 search published article - es // searchtype: for future, can be article,category,author... , sorttype=latest
	def test_searchArticle_3(self):

		q = 'scoopwhoop'
		pn=1
		searchtype=''
		sorttype= 'latest'
		response = functiontosearch(q,pn,searchtype,sorttype)
		# print "Scoopwhoop Search Articles Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,1)


	#19 search published article - es // searchtype: for future, can be article,category,author... , pn=2, sorttype=latest
	def test_searchArticle_4(self):

		q = 'sports'
		pn=2
		searchtype=''
		sorttype= 'latest'
		response = functiontosearch(q,pn,searchtype,sorttype)
		# print "Scoopwhoop Search Articles Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,1)


	#20 search published article - es // searchtype: for future, can be article,category,author... , pn=-1, sorttype=latest
	def test_searchArticle_5(self):

		q = 'sports'
		pn=-1
		searchtype=''
		sorttype= 'latest'
		response = functiontosearch(q,pn,searchtype,sorttype)
		# print "Scoopwhoop Search Articles Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,0)


	#21 search published article - es // searchtype: for future, can be article,category,author... , fuzzy match
	def test_searchArticle_6(self):

		q = 'salmaan khan'
		pn=1
		searchtype=''
		sorttype= 'score'
		response = functiontosearch(q,pn,searchtype,sorttype)
		# print "Scoopwhoop Search Articles Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,1)


	#22 search published article - es // searchtype: for future, can be article,category,author... , sorttype=oldest(any other except latest,score)
	def test_searchArticle_7(self):

		q = 'scoopwhoop'
		pn=1
		searchtype=''
		sorttype= 'oldest'
		response = functiontosearch(q,pn,searchtype,sorttype)
		# print "Scoopwhoop Search Articles Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,0)


	#23 search published article - es // searchtype: for future, can be article,category,author... , pn=0, pn has to a positive integer starting from 1
	def test_searchArticle_8(self):

		q = 'scoopwhoop'
		pn=0
		searchtype=''
		sorttype= 'score'
		response = functiontosearch(q,pn,searchtype,sorttype)
		# print "Scoopwhoop Search Articles Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,0)


	#24 get mlt results : docid, category, prop
	def test_mltResponse_1(self):

		x = functionToGetIdCatMLT()
		did =  x['hits']['hits'][0]['_source']['id']
		dcategory = x['hits']['hits'][0]['_source']['swcats'][0]['category_slug']

		docid=did
		category=dcategory
		prop=PROP
		response = findmltdocsprop(docid,prop,category)
		# print "Scoopwhoop MLT Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,1)


	#25 get mlt results : docid, category, [prop : incorrect value/not given]
	def test_mltResponse_2(self):

		x = functionToGetIdCatMLT()
		did =  x['hits']['hits'][0]['_source']['id']
		dcategory = x['hits']['hits'][0]['_source']['swcats'][0]['category_slug']

		docid=did
		category=dcategory
		prop='anything'
		response = findmltdocsprop(docid,prop,category)
		# print "Scoopwhoop MLT Response: " + str(response)
		st = response['status']
		self.assertIsNotNone(response)
		self.assertEqual(st,0)


	#26 get mlt results : docid, category : news, prop
	def test_mltResponse_3(self):

		mod_time = datetime.now() + timedelta(days=-(2))
		dbac = datetime.strftime(mod_time, "%Y-%m-%d")

		x = functionToGetIdCatMLT()
		try :
			for inf in x['hits']['hits'] :
				if {'category_display': "News",'category_slug': "news"} in inf['_source']['swcats'] :
					newsart = inf
					break
		except Exception as e :
			print str(e)

		did =  newsart['_source']['id']

		docid=did
		category='news'
		prop=PROP
		response = findmltdocsprop(docid,prop,category)
		# print "Scoopwhoop MLT Response: " + str(response)
		st = response['status']
		info = response['info']
		try :
			for inf in info['hits']['hits'] :
				print inf['_source']['date_sort']
				if inf['_source']['date_sort'] < dbac :
					self.assertIsNone(inf['_source']['date_sort'])
		except Exception as e :
			print str(e)
		self.assertIsNotNone(response)
		self.assertEqual(st,1)


	#27 get mlt results : docid, category : news, prop
	def test_mltResponse_4(self):

		x = functionToGetIdCatMLT()
		did =  x['hits']['hits'][0]['_source']['id']
		dcategory = x['hits']['hits'][0]['_source']['swcats'][0]['category_slug']

		docid=did
		category=dcategory
		prop=PROP
		response = findmltdocsprop(docid,prop,category)
		# print "Scoopwhoop MLT Response: " + str(response)
		st = response['status']
		info = response['info']
		try :
			for inf in info['hits']['hits'] :
				self.assertNotIn({'category_display': "News",'category_slug': "news"},inf['_source']['swcats'])
		except Exception as e :
			print str(e)
		self.assertIsNotNone(response)
		self.assertEqual(st,1)