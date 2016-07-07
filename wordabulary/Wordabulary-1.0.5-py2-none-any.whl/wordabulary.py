# check this out - https://en.wikipedia.org/wiki/Moby_Project
import time
from prettytable import PrettyTable

#All hand-made modules
from length_sorter import *
from has_no_e import * 
from has_no_these import *
from has_only_these import *
from is_abecedarian import *
from words_with_e import *
from ends_with import *
from allstar_words import *
from is_there import *
from is_there_dict import *
from reverse_pairs import *
from interlocked import *
from histogram import *
from rotate_pairs import *
from pronounce import *
from rhyming import *
from crossword import *
from booker import *#new submenu
from booker_most_frequent import *
from booker_correct import *
from anagrams import *
#####
#####	install prettytable - pip install prettytable
#####


####
####	<3 : All functions are now imported ,for future clarity	
####	I could have had a function called display in each of the modules
####	which would handle the input like their main 's , but I intend not to do so.
####	This way, you don't have to view each file to understand what that option does
####	So , without wasting time , you can understand the code structure in this file itself
####	That being said , each module can be run individually as well
####	This file just unites and displays them together
####

if __name__=='__main__':
	
	print '\nWelcome to Wordabulary ! Choose your operation '

	while True:
		time.sleep(1)
		print '\n#operations '
		print '1 for printing words above some length'
		print '2 for checking if a group of letters are not present in a word'
		print '3 for checking if a group of letters are only present in a word'
		print '4 for checking if a group of letters are all exclusively present in a word'
		print '5 for checking if a word is abecedarian(arranged alphabetically)'
		print '6 for checking how many words contain given substring'
		print '7 for checking how many words end with given substring'
		print '8 for checking popularity of each char'
		print '9 for checking if given word makes sense'
		print '10 for printing all reverse pairs'
		print '11 for printing interlocked words'
		print '12 for obtaining char-distribution for a string'
		print '13 for all rotated pair iterations'
		print '14 for pronounciation for a word'
		print '15 for rhyming words '
		print '16 for crossword-aids/find out what this is'
		print '17 for books/document analysis'
		print '18 for anagram of given word'

		print 'and 0 to exit\n'
		
		option = raw_input("Enter choice : ")

		if option=='0' or option=='clear':
			break


		elif option=='1':
			longword=raw_input("Print all longer words \nWhat min. length of words? ")
			longword = int(longword)
			length_sorter.length_sorter(longword)


		elif option=='2':
			not_letters = raw_input("Enter forbidden letter(s) ,separated by , : ").split(",")
			#not_let = map(char,not_letters.split(","))

			word=raw_input("Enter word to check for forbidden letter(s) : ")
			has_no_these.has_no_these(word,not_letters,True)#allow printing


		elif option=='3':
			only_letters = raw_input("Enter allowed letter(s), unseparated: ")

			word=raw_input("Enter word to check for allowed letter(s) : ")
			has_only_these.has_only_these(word,only_letters,True)#allow printing


		elif option=='4':
			fixed_letters = raw_input("Enter allowed letter(s), unseparated: ")

			word=raw_input("Enter word to check if all allowed letter(s) are present: ")
			has_only_these.has_only_these(fixed_letters,word,True)#allow printing


		elif option=='5':
			word = raw_input("Enter word to be checked for abecedarian : ")
			print is_abecedarian.is_abecedarian(word)		


		elif option=='6':
			substring = raw_input("Enter substring to check how many words have it : ")
			
			is_print = raw_input("Enter 1 to print , else nothing:")
			print_bool = False
			if is_print=='1':
				print_bool=True

			#if len(char)==1:
			count = words_with_e.words_with_e(substring,print_bool)
			#disable printing words without char

			time.sleep(2)#externally called to save time for allstars
			print '\nwords containing',substring,':',count

			#else:
			#	print 'char needs to be a single letter!'


		elif option=='7':
			#extend later to rhyming words - sky , bye
			substring=raw_input("Enter substring to check words which end with it : ")
			#printing mandatory
			ends_with.ends_with(substring)


		elif option=='8':
			print 'Crunching numbers ... displaying count of words containing each letter'
			allstar_words.allstar_words()


		elif option=='9':
			search_this = raw_input("Enter word to search for , in database : ")
			
			#	dict method faster upto 50% - for word boy - 0.06 and 0.04 resp
			#										map for worst case
			# check speed , uncomment time prints in these files v

			#print 'Method 1 : list and append'
			#is_there.is_there(search_this)
			#print 'Method 2 : dict()'
			is_there_dict.is_there_dict(search_this)


		elif option=='10':
			print 'Displaying all reverse pairs:'
			char = raw_input("Begin with what letter? (* for complete) : ")
			reverse_pairs.reverse_pairs(char)


		elif option=='11':
			interlocked.interlocked()


		elif option=='12':
			inp_str = raw_input("Enter string to obtain histogram : ")
			hist = histogram.histogram(inp_str)

			print hist,'\n'
			histogram.print_hist(hist)


		elif option=='13':
			substr = raw_input("Enter substring from which words are to be rotated : ")
			rotate_pairs.iterate_rotors(substr)


		elif option=='14':
			word = raw_input("Enter word to pronounce :")

			pron = pronounce.print_pronounce(word)
			if pron!='0':
				print 'Pronounce as : ',pron

				show_guide = raw_input("Enter y to see pronounciation guide : ")
				if show_guide=='y':
					pronounce.guide()
					
			else:
				print 'Pronunciation not found! Did you enter a valid word ? Check using option 9'


		elif option=='15':
			word = raw_input("Enter word for which rhyming words are needed : ")
			substr = raw_input("start with any substr ? enter * for all : ")
			rhyming.rhyming(word,substr)

		elif option=='16':
			print 'Do you wonder what is 6 letter word with y as 2nd letter and ends with n ?'
			time.sleep(1)
			print 'i.e, a word _y___n ?\nThis is perfect for you !'
			time.sleep(1)
			print 'just type _y__n or -y--n and voila , all possibilities are given!'
			print 'Psst : it\'s python'
			time.sleep(1)
			mystery_word = raw_input("\nEnter your mystery word in the above format : ")
			crossword.crossword(mystery_word)



		elif option=='17':
			booker.initialise()


		elif option=='18':
			word = raw_input("Enter word to check all its anagrams : ")
			anagrams.print_anagrams(word)


#generate anagrams of word


#Total number of words = 113809 - now updated ! - has some 540233 words
		else :
			print 'Incorrect choice :(\n'