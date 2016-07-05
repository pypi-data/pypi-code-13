import time
import os.path

def contents_of(word):
	"""

		return a string containing all letters in order
	"""
	c = list(word)
	c.sort()
	c = ''.join(c)
	return c


def find_anagrams(word,filename='reference/words.txt'):
	"""

		find all anagrams of word in file
	"""
	if not os.path.isfile(filename):
		print 'Not a valid file! Returning now...'
		return 

	content = contents_of(word)
	lister = []
	count = 0
	for line in open(filename):
		word_iter = line.strip().lower()
		sign = contents_of(word_iter)

		if sign==content :
			if word_iter!=word:
				lister.append(word_iter)
				count += 1

	lister.sort()
	return lister,count


def print_anagrams(word,filename='reference/words.txt'):
	"""
		Da MVP . Print all anagrams of given word found in file
	"""
	lister,count = find_anagrams(word)
	if count==0:
		print 'No anagram found'
		return

	for word in lister:
		print word
		time.sleep(0.1)
	
	print '\nTotal anagrams found : ',count


if __name__=='__main__':
	word = raw_input("Enter word to check all its anagrams : ")
	print_anagrams(word)