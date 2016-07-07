import time
import os.path
import string

import is_there_dict 
import booker_most_frequent


#you might want to look at deprecated/ this file for naive implementation
def check_data(transcript,reference_dict):
	"""

		return a dictionary of words in transcript not in reference_dict
		Effectively , these are percieved as misspelled words.
	"""
	incorrect_dict = dict()
	count = 0
	for key ,freq,percent in transcript:

		if key not in reference_dict:
			#print key,' not in dict'
			incorrect_dict[key] = 'suggest_correction_here'
			count += freq	# a word may be misspelled multiple times

	return incorrect_dict,count


def correct(filer):
	
	if not os.path.isfile(filer):
		print '\tNot a valid file !Returning now...'
		return 

	out,tot_words_doc = booker_most_frequent.most_frequent(filer,'word')
	reference_dict = is_there_dict.create_dict()

	incorrect_dict,count = check_data(out,reference_dict)
	print '\n'	
	for key in incorrect_dict:
		print '\t',key

	time.sleep(2)
	print '\n\tTotal misspelled occurences : ',count


if __name__ == '__main__':
	
	filer = raw_input("\tEnter your file for typos:\n\t ")
	correct(filer)