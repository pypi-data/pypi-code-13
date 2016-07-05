import time
from has_no_e import *
#allow usage from other files if only one import
#import file.py necessary in case of wordabulary which imports 12 files!

def has_no_these(word,not_letters,is_print):
	"""

		check if certain letters are not present in the word

		is_print used for larger analysis - to check for the complete set
	"""
	count_breach = 0
	for each_letter in not_letters:
		if has_no_e(word,each_letter):
			#print each_letter,' is not present'
			if is_print:
				print 'working...'
			time.sleep(1)

		else: 
			if is_print:
				print 'The barrier has been breached by ',each_letter
			else:
				return False
			count_breach = count_breach+1
			time.sleep(1)


	if count_breach > 0:
		if is_print:
			print '\nWe have been compromised\n'
		else:
			return False
	else:
		if is_print:
			print '\nThe coast is clear , mate\n'
		else:
			return True
	time.sleep(2)



if __name__=='__main__':
	not_letters = raw_input("Enter forbidden letter(s) ,separated by , : ").split(",")

	word=raw_input("Enter word to check for forbidden letter(s) : ")
	has_no_these(word,not_letters,True)#allow printing