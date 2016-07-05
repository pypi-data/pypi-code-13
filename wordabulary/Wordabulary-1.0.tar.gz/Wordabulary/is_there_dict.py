import time
import is_there

def create_dict(filename='reference/words.txt'):
	"""

		Add each string as key in a dict
	"""
	word_dict = dict()
	fin = open(filename)

	for line in fin:
		word = line.strip()
		word = word.lower()
		word_dict[word] = word

	return word_dict

def is_there_dict(word):
 	"""

 		U still here ?Why are you so obsessed with this . Go , away !
 		Good . Use your in method , because #tables were made for you
 	"""
	start_time = time.time()
	source = create_dict()
	print '\n',word,'in dict : ',word in source

	elapsed_time = time.time() - start_time
	#print 'elapsed_time :',elapsed_time,'seconds'
	# upto 50 % better - check where this backtracks to in wordabulary

if __name__ == '__main__':
	search_this = raw_input("Enter word to search for , in database : ")
			
	#	dict method faster upto 50% - for word boy - 0.06 and 0.04 resp
	#										map for worst case
	# check speed , uncomment time prints in these files v

	#print 'Method 1 : list and append'
	#is_there.is_there(search_this)
	#print 'Method 2 : dict()
	is_there_dict(search_this)