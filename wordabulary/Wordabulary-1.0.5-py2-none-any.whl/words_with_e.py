from has_no_e import *
import time

def total_words(filename='reference/words.txt'):

	tots = 0
	fin = open(filename)
	for line in fin:
		word = line.strip()#get rid of \r
		if True:
			tots += 1
	return tots


def words_with_e(substring,is_print):
	"""

		Traverse all words to check how many words do not have this substring
		Changed  to return only number for now
		e is the most common letter
	"""
	#print ''
	if is_print:
		print 'Words with',substring
	count = 0
	fin = open('reference/words.txt')
	substring = substring.lower()
	for line in fin:
		word = line.strip().lower()#get rid of \r
	
		if not has_no_e(word,substring):
				if is_print:
					print word
					time.sleep(0.1)
				count += 1
	#Total number of words = 113809 - now updated ! - has some 540233 words
	#count = 113809 - count# faster to check how many words don't have that letter
	# I call B.S - new words should be added freely

	return count


if __name__=='__main__':
	substring = raw_input("Enter substring to check how many words have it : ")
			
	is_print = raw_input("Enter 1 to print , else nothing:")
	print_bool = False
	if is_print=='1':
		print_bool=True
		#if len(char)==1:

	count = words_with_e(substring,print_bool)
		#disable printing words without char

	time.sleep(2)#externally called to save time for allstars
	print '\nwords containing',substring,':',count