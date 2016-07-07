import time
from has_no_e import *


def has_only_these(word,only_letters,is_print):
	"""

		check if certain letters are only present in the word

		is_print used for reference
	"""
	count_accept = 0
	#revert the approach of has_no_these
	for each_letter in word:
		if has_no_e(only_letters,each_letter)==False:
			count_accept = count_accept+1
			if is_print:
				print 'working...'
			time.sleep(1)

		else: #a letter in the word is not in the allowed area
			if is_print:
				print 'The barrier has been breached by ',each_letter
			else:
				return False
			time.sleep(1)

	if count_accept !=len(word):
		if is_print:
			print '\nWe have been compromised\n'
		else:
			return False
	else:
		if is_print:
			print '\nAll good !\n'
		else:
			return True
	time.sleep(2)



if __name__=='__main__':
	only_letters = raw_input("Enter allowed letter(s), unseparated: ")

	word=raw_input("Enter word to check for allowed letter(s) : ")
	has_only_these(word,only_letters,True)#allow printing