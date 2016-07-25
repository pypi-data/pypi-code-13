#import umls_request_cache
import umls_request_manager
import umls_auth
import pprint
import json
import sys
import copy
import os
import json
import csv
import numbers
import decimal
import pprint
import itertools
#import sklearn
#import numpy
#import scipy
import requests
import grequests
import time
#import statistics


start = time.time()
last_collection = time.time()
current_data_recieved = 0
total_data_recieved = 0
throughput = 0


umls_url = "https://uts-ws.nlm.nih.gov/rest"
service="http://umlsks.nlm.nih.gov"
auth = umls_auth.Authentication()
TGT = auth.gettgt()
s = requests.Session()
pageSize = 400
window_size = 5

failed_request_responses = []


def pretty_print(data):
	print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


def parse_args():
	return sys.argv[1]


def request_exception_handler(request, exception):
	print "Request failed: "
	print request
	print exception


def auth_exception_handler(request, exception):
	print "Auth failed: "
	print request
	print exception


def async_request(i, url, ticket):
	if ticket and ticket.text:
		ticket = ticket.text
	else:
		ticket = ""
	print "Generating request for page: " + str(i) + " using ticket " + ticket
	payload = {'ticket': ticket, 'pageSize': pageSize};
	return grequests.get(url, params = payload, session = s)


def async_auth(i):
	print "Generating ticket " + str(i) + ", " + str(window_size) + " needed"
	params = {'service': service}
	h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent":"python"}
	return grequests.post(TGT,data=params,headers=h, session = s)


def calc_throughput():
	global current_data_recieved
	global last_collection
	current = time.time()
	avg_throughput = float(total_data_recieved)/(current - start)
	cur_throughput = float(current_data_recieved)/(current - last_collection)
	print "AVERAGE THROUGHPUT: " + str(avg_throughput)
	print "CURRENT THROUGHPUT: " + str(cur_throughput)
	last_collection = time.time()
	current_data_recieved = 0


def get_response_data(response):
	global total_data_recieved
	global current_data_recieved
	if response:
		if response.status_code == 200:
			total_data_recieved = total_data_recieved + len(response.text)
			current_data_recieved = current_data_recieved + len(response.text)
			try:
				return response.json()
			except:
				print response.url
				print response.text
				print "JSON CONVERSION FAILED"

	print "request failed in get_response_data()"
	print response
	print response.url
	failed_request_responses.append(response)


def get_descendants(codes, source):
	urls = map(lambda code: umls_url + "/content/current/source/" + source + "/" + code + "/descendants", codes)
	responses = client.get(urls, params = {"pageSize": pageSize})
	response_data = map(lambda response: get_response_data(response), responses)
	calc_throughput()
	return response_data
	

def get_strings(codes, source):
	urls = map(lambda code: umls_url + "/content/current/source/" + source + "/" + code, codes)
	responses = client.get(urls , params = {"pageSize": pageSize})
	response_data = map(lambda response: get_response_data(response), responses)
	return response_data
	

def augment_edges_helper(f,snocodes_data,key,codeKey,outputTo,sourceString):#,getDecen,getStringName):
	ORIGLEN=str(len(str(outputTo)))
	countDone=0
	print f
	all_edges=snocodes_data[key]["id_lookup"][codeKey]
	codes = all_edges.keys()
	#print "ALL EDGES KEYS: "+str(codes)
	goodCodes=[]
	g2old={}
	for code in codes:
		if code.find('|')>0:
			codeSplit=code.split('|')
			if len(codeSplit)==2:
				newCode=codeSplit[1].strip()
				goodCodes.append(newCode)
				g2old[newCode]=code
		else:
			goodCodes.append(code)
			g2old[code]=code
	codes=goodCodes
	print "ALL EDGES KEYS: "+str(codes)
	#return
	#for code in all_edges:
	for idx in range(0, len(codes), window_size):
		edgesSource=snocodes_data[key]["id_lookup"][codeKey][g2old[codes[idx]]]

		resp_data_list = get_descendants(codes[ idx : idx + window_size ], sourceString)
		code_data_list = get_strings(codes[ idx : idx + window_size ], sourceString)

		#desc_data = get_descendants(all)
		for resp_idx in range(0 , len(resp_data_list)):
			resp_data = resp_data_list[resp_idx]
			code_data = code_data_list[resp_idx]
			if resp_data:
				if code_data:
					codeName=code_data["result"]["name"].encode('ascii', 'ignore')
				else:
					codeName = ""
					print "Request for code description failed"

				countDone+=len(codes[ idx : idx + window_size ])

				#UNCOMMENT THIS TO QUICKLY GENERATE OUTPUT FILES FOR TESTING
				'''
				print "count done: ".upper() + str(countDone)
				if countDone > 10:
					print "NEW LEN: "+str(len(str(outputTo))) +" vs "+ str(ORIGLEN)
					return outputTo
				'''
				print "TESTING DESCENDANTS OF: "+str(codeName)+" ["+str(countDone)+"/"+str(len(all_edges))+"] for :: "+str(f)
				if resp_data["result"]:	
					for result in resp_data["result"]:
						source=result["rootSource"]
						if source == sourceString:
							decendantsName=result["name"].encode('ascii', 'ignore')
							decendantsUI=result["ui"]
							if decendantsUI not in outputTo:
								print "ADDING: "+str(decendantsName) +" "+str(decendantsUI) + " TO : "+str(code_data["result"]["name"])+":"+str(codes[idx])
								outputTo[decendantsUI]=copy.deepcopy(edgesSource)

								outputTo[decendantsUI].append(sourceString+"_DECENDANTS_" + codes[resp_idx] + "_" + codeName)
			else:
				print "HUH?"
		print "NEW LEN: "+str(len(str(outputTo)))+" vs "+str(ORIGLEN)
	return outputTo	
	

def augment_edges(fileName,snocodes_data):
	ORIGLEN=str(len(str(snocodes_data)))
	snocodes_data_copy = copy.deepcopy(snocodes_data)
	for key in snocodes_data:
		#print "KEY: " + str(key)
		#print snocodes_data_copy[key].keys()
		#print snocodes_data_copy[key]["id_lookup"].keys()
		
		#ICD9
		outputToICD9 = snocodes_data_copy[key]["id_lookup"]["http://hl7.org/fhir/sid/icd-9-cm"]
		outputToICD9 = augment_edges_helper(fileName,snocodes_data,key,"http://hl7.org/fhir/sid/icd-9-cm",outputToICD9,"ICD9CM")#,get_descendants_icd9,get_string_icd9)
		snocodes_data_copy[key]["id_lookup"]["http://hl7.org/fhir/sid/icd-9-cm"] = outputToICD9
		#ICD10
		outputToICD10 = snocodes_data_copy[key]["id_lookup"]["http://hl7.org/fhir/sid/icd-10"]
		outputToICD10 = augment_edges_helper(fileName,snocodes_data,key,"http://hl7.org/fhir/sid/icd-10",outputToICD10,"ICD10CM")#,get_descendants_icd10,get_string_icd10)
		snocodes_data_copy[key]["id_lookup"]["http://hl7.org/fhir/sid/icd-10"] = outputToICD10
		#SNOMED
		outputTo = snocodes_data_copy[key]["id_lookup"]["http://snomed.info/sct"]
		outputTo = augment_edges_helper(fileName,snocodes_data,key,"http://snomed.info/sct",outputTo,"SNOMEDCT_US")#,get_descendants,get_string)
		snocodes_data_copy[key]["id_lookup"]["http://snomed.info/sct"]=outputTo
		
		#print key
		print "NEW ALL LEN: "+str(len(str(snocodes_data)))+" vs "+str(ORIGLEN)
		
	return snocodes_data_copy


def get_filepaths(directory):
	file_paths = []  # List which will store all of the full filepaths.
	# Walk the tree.
	for root, directories, files in os.walk(directory):
		for filename in files:
			# Join the two strings in order to form the full filepath.
			filepath = os.path.join(root, filename)
			file_paths.append(filepath)  # Add it to the list.
	return file_paths  # Self-explanatory.

#client = umls_request_cache.RequestManager()
client = umls_request_manager.RequestManager()

pp = pprint.PrettyPrinter(indent = 1)

if len(sys.argv) > 1:
	current_dir = sys.argv[1]
else:
	current_dir=os.getcwd()

print current_dir
full_file_paths = get_filepaths(current_dir)

c=0
limit=1
for f in full_file_paths:
	if f.find(".json")>0 and f.find("NEW")<0:
		print "DOING: "+f
		with open(f) as f:
			snocodes_data = json.loads(f.read())
			result = augment_edges(f,snocodes_data)
			#print result
			out_filename = f.name + ".NEW"
			print "WRITING TO: " + out_filename
			with open(out_filename, "w") as outfile:
				outfile.write(json.dumps(result,indent=4))
			#c=c+1
			
			if c>=limit:
				break
				
	if c>=limit:
		break
