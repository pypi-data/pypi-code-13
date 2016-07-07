import time
from has_no_e import *

def ends_with(substring):
	"""
		check how many words ends with that substring
 	"""
	print 'Words ending with ',substring,'\n'

	#Approach 1
	#check out the deprecated folder for naive and initial implementations
	#Approach 2 found to be marginally faster
	# 0.2417 and 0.24107 - approach 2 overall better
	count = 0
	start_time = time.time()
	fin = open('reference/words.txt')
	for line in fin:
		##Approach 2:check only for words containing that substring
		word = line.strip()#get rid of \r

		if has_no_e(word,substring)==False:
			#the substring is already present in the words

			word_start = len(word) - len(substring)
			if word.find(substring,word_start)==word_start:
			#start finding from last 3rd in case of bro
				print word
				count += 1
				time.sleep(0.2)

	elapsed_time = time.time() - start_time
	print '\nTotal words :', count#,' in time :',elapsed_time


if __name__=='__main__':

	substring=raw_input("Enter substring to check words which end with it : ")
	
	ends_with(substring)