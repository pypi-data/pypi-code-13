from is_there_dict import create_dict
import time
"""
	uses tuple to solve this dilemma
"""


def known_length(mystery_word):
	"""

		consider -y---n => known length = 2
		used to check if all known chars also in word
	"""
	known = 0
	missing = {'-':'dash','_':'underscore'}#add reject indices
	for char in mystery_word:
		if char not in missing:
			known += 1

	return known


def crossword(mystery_word):
	"""
		crossword aid
		prints all words of given length and only a few known chars in it
	"""
	look_in = create_dict()

	#create frequently used functions outside
	mystery_tuple = tuple(mystery_word)
	known = known_length(mystery_word)
	
	missing = dict()
	missing = {'-':'dash','_':'underscore'}#add reject indices
	matches = 0
	match_list = []#create for sorting

	for word in look_in:
		
		if len(word) ==len(mystery_word):
		
			this_tuple = tuple(word)
			word_match = 0

			for x,y in zip(mystery_tuple,this_tuple):

				if x not in missing and x==y:
					# i.e, char in this place is known,and it matches with word's that position
					word_match += 1

			if word_match==known:
				# i.e,all known words have matched
				match_list.append(word)
				matches += 1

	#at this point , all suitable matches found
	print 'Working ....'
	time.sleep(2)#pause for dramatic effect
	
	match_list.sort()
	for word in match_list:
		print word
		time.sleep(0.1)

	print '\nTotal alternatives : ',matches


if __name__ == '__main__':
	
	print 'Do you wonder what is 6 letter word with y as 2nd letter and ends with n ?'
	time.sleep(1)
	print 'i.e, a word _y___n ?\nThis is perfect for you !'
	time.sleep(1)
	print 'just type _y__n or -y--n and voila , all possibilities are given!'
	print 'Psst : it\'s python'
	time.sleep(1)
	mystery_word = raw_input("\nEnter your mystery word in the above format : ")
	crossword(mystery_word)