from eswrapper.defines import *
from eswrapper.settings import *
import elasticsearch
from elasticsearch import Elasticsearch, helpers
import json
import pprint


##enter ip to connect to server
#print "Enter the ip for es server"
#ip_name = raw_input()

##connect to es server
es = es_client


## function to create index
def create_index(prop, mapping = ES_INDEX_MAPPING, settings = None):

		result = {'status': 0, 'index_created': '', 'error': ''}

		try:

			if(check_index_exists(index_name_new) == True):
				result['status'] = 2
				result['index_created'] = index_name_new
				result['error'] = 'index exists'
				return result


			if(prop == '25rt') or (prop == '679a'):

				settings = ES_INDEX_SETTINGS

			if (prop == 's57v') :

				settings = ES_INDEX_SETTINGS_GP


			index_parameters =  { 'settings': settings, 'mappings': mapping }

			#print index_parameters

			cr_status = es.indices.create(index = index_name_new, body = index_parameters)

			if(cr_status.has_key('acknowledged') and cr_status['acknowledged'] == True):
				result['status'] = 1
				result['index_created'] = index_name_new


		except Exception as (e):
			# TODO: add a logger here
			result['status'] = 0
			result['error'] = str(e)

			print "any exception", str(e)

		return result

###function to check if index exists
def check_index_exists(index):

		status = es.indices.exists(index)
		return status


###function to bulk index the documents
def index_bulk(docs, total):

		'''
		using the bulk insert api of Elasticsearch here and see what happens
		:param json_data:
		:return:
		'''

		actions = []

		if(total == 0 or len(docs) == 0):
			return

		## iterate through the list of docs
		for entry in docs:

			doc_id = entry['_id']

			## TODO log this entry
			if(doc_id is None):
				continue

			action = {
				"_index": index_name_new,
				"_type": 'post',
				"_id": doc_id,
				"_source": json.dumps(entry)
				}

			actions.append(action)


		helpers.bulk(es, actions)

		return





print "*****"
print "Alias ['vb_realtimeposts_alias , gp_realtimeposts_alias , swp_realtimeposts_alias']"
print "*****\n"

all_alias = es.indices.get_aliases(name = ['vb_realtimeposts_alias','gp_realtimeposts_alias','swp_realtimeposts_alias'])
pprint.pprint(all_alias) 

print "\nEnter the name of alias"
alias_name = raw_input()

print "\n"

print "Enter the name of previous index to which the alias is pointing"
index_name = raw_input()

print "\n"


### make the alias point to the index already created for the first time
c_alias = es.indices.put_alias(name = alias_name,index = index_name)
print "The Alias is :"
pprint.pprint(c_alias)

print "\n"

### get the alias and the index it is pointing to
check_alias = es.indices.get_alias(alias_name)
print "The Alias is : \n"
pprint.pprint(check_alias)

print "\n"


###get the total number of documents in the previos index, doc_type = 'post' in defines.py
countdocs = es.count(index=alias_name, doc_type = ES_CONTENT_DOC_TYPE)
totaldocs =  countdocs['count']
print "total docs = " + str(totaldocs)

###get all docs and store them in a list
docs = es.search(index=alias_name, size = totaldocs)

sendList = []
tempDict = {}
for h in docs['hits']['hits'] :
	# if h['_source'].has_key('title') :
		tempDict['sh_heading'] = h['_source']['sh_heading']
		tempDict['ar_id'] = h['_source']['ar_id']
		tempDict['title'] = h['_source']['title']
		tempDict['fImgUrl'] = h['_source']['fImgUrl']
		tempDict['tags'] = h['_source']['tags']
		tempDict['slug'] = h['_source']['slug']
		tempDict['ar_name'] = h['_source']['ar_name']
		tempDict['ar_url'] = h['_source']['ar_url']
		tempDict['swcats'] = h['_source']['swcats']
		tempDict['pub_date'] = h['_source']['pub_date']
		tempDict['date_sort'] = h['_source']['date_sort']
		tempDict['content'] = h['_source']['content']
		tempDict['_id'] = h['_id']
		# print tempDict
		sendList.append(tempDict.copy())

# print sendList
totaldocs =  len(sendList)


print "Enter the name of new index created"
index_name_new = raw_input()

print "Enter the property code of alias for which index is to be created, [ VB='679a' , SW='25rt' , GP='s57v' ] "
prop_name = raw_input()

###create a new index
nindex = create_index(prop_name)
print "\n"
print nindex

####put the documents in the new index by bulk indexing api
print "Bulk indexing the documents to new index: "
index_bulk(sendList,totaldocs)



print "\n enter the index to be removed from alias"
index_name_remove = raw_input()

print "\n enter the index to be added to alias"
index_name_added = raw_input()


a_body = {"actions":
			[
				{ "remove": { "index": index_name_remove, "alias": alias_name }},
				{ "add":    { "index": index_name_added, "alias": alias_name }}
			]
		}

### changing the alias point to index
es.indices.update_aliases(body = a_body)

###check for alias point to index after updation
check_updated_alias = es.indices.get_alias(alias_name)
print check_updated_alias

print "\n Your alias is now pointing to :" + index_name_added
