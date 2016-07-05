import time


def length_sorter(longword):
	"""
		print all words only beyond some length
	"""
	print ' '
	count = 0
	fin = open('reference/words.txt')
	for line in fin:
		word = line.strip()#get rid of \r
	
		if len(word) >=longword:
			print word
			time.sleep(1)
			count = count + 1
	
	print '\nTotal words printed : ',count
	print ' '
	time.sleep(2)


if __name__=='__main__':

	longword=raw_input("Print all longer words \nWhat min. length of words? ")
	longword = int(longword)
	length_sorter(longword)