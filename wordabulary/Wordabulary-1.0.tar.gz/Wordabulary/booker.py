import time
import booker_most_frequent
import booker_correct

def initialise():
	"""

		submenu for dealing with books and docs
	"""
	print '\tLet\'s analyze some books and stuff'

	while True :
		print '\t#operations'
		print '\t1 for finding most frequent chars in a book(txt file)'
		print '\t2 for finding most frequent words in a book(txt file)'
		print '\t3 for finding all typos in a book'
		print '\n\t and 0 to exit this submenu'
	
		option = raw_input("\tYour choice :")
		print '\tTIP : start with / if address for file is not local'
		if option=='0' or option=='clear':
			break


		elif option=='1':
			filer=raw_input("\tEnter your file for frequency distribution:\n\t")
			booker_most_frequent.iterate_booker(filer,'char')	
		
		elif option=='2':
			filer=raw_input("\tEnter your file for word distribution:\n\t")
			booker_most_frequent.iterate_booker(filer,'word')

		elif option=='3':
			filer = raw_input("\tEnter your file for typos:\n\t ")
			booker_correct.correct(filer)	


		else :
			print '\tIncorrect choice :(\n'

		time.sleep(1)
		print '\n'



if __name__=='__main__':
	initialise()
