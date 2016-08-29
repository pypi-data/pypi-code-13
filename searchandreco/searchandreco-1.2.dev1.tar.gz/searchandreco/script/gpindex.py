from eswrapper.defines import *
from eswrapper.settings import *
import elasticsearch
from elasticsearch import Elasticsearch, helpers
import json
import pprint

### creating new index for gp and adding it to gp alias, data will populated through mongo.

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







print "*****"
print "Alias ['vb_realtimeposts_alias , gp_realtimeposts_alias , swp_realtimeposts_alias']"
print "*****\n"

all_alias = es.indices.get_aliases(name = ['vb_realtimeposts_alias','gp_realtimeposts_alias','swp_realtimeposts_alias'])
pprint.pprint(all_alias)

print "\nEnter the name of alias"
alias_name = raw_input()

print "\n"



print "Enter the name of new index created\n"
index_name_new = raw_input()

print "\nEnter the property code of alias for which index is to be created, [ VB='679a' , SW='25rt' , GP='s57v' ] "
prop_name = raw_input()

###create a new index
nindex = create_index(prop_name)
print "\n"
print nindex


a_body = {"actions":
			[
				{ "add":    { "index": nindex, "alias": alias_name }}
			]
		}

### changing the alias point to index
#es.indices.update_aliases(body = a_body)
es.indices.put_alias(name = alias_name,index = index_name_new)

###check for alias point to index after updation
check_updated_alias = es.indices.get_alias(alias_name)
print check_updated_alias

print "\n Your alias is now pointing to :" + index_name_new
