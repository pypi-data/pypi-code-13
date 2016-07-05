from has_no_e import *
from words_with_e import *
import time
import string
from prettytable import PrettyTable

import matplotlib.pyplot as plt
from plotters import *
import booker_most_frequent #use for ordering

def get_percent_in2points(freq,total):
	"""
		get percent of total from freq as xx.xx%
	"""
	percent = 100.0*freq/total
	percent = int(100*percent)/100.0
	return percent

def allstar_words():
	"""

		Traverse all words to check how many words do not have a char

		traverse for all chars
	"""
	print ''
	table = PrettyTable(['Char','Freq','%'])
	frequency=[]
	letters=[]

	start=ord('a')#convert char to int for iteration
	for i in range(26):
		char = chr(start+i)

		#print char 	#At this point , it just prints every alphabet
		#print 'words containing',char,':',words_with_e(char,False)
		letters.append(i+1)
		frequency.append(words_with_e(char,False))

		percent = get_percent_in2points(frequency[i],total_words())#total from words_with_e

		table.add_row([char , frequency[i] , percent])	
		print 'Counting words with ',char,'...'
		time.sleep(0.08)

	time.sleep(1)
	print '\nTotal number of words = ',total_words()
	print table

	show_freq = raw_input("Enter y to display alphabet wise plot : ")
	if show_freq=='y':
		plot_letters(letters,frequency)

	#under development
	"""
	to_sort = raw_input("See sorted version ? press y : ")
	if to_sort == 'y':
	
		book = booker_most_frequent.read_file('reference/words.txt')
		result , tots = booker_most_frequent.most_frequent(book)
		
		let = []
		frew = []
		for x,freq,percent in result:
			let.append(ord(x) - start)
			frew.append(freq)
		plot_letters(let,frew)
	"""
	#To Do : 
	
	#a graph can be added
	# freq.wise



if __name__ == '__main__':
	print 'Crunching numbers ... displaying count of words containing each letter'
	allstar_words()