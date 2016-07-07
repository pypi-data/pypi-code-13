# check this out - https://en.wikipedia.org/wiki/Moby_Project
import time
from prettytable import PrettyTable
import string
import matplotlib.pyplot as plt
from math import pow
from bisect import bisect_left
import os.path

#All hand-made modules
"""
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
"""
#####
#####	install prettytable - pip install prettytable
#####

###
###	NOTE : This file is essential for pip module.If you want to read the code , 
### wordabulary.py is the file for you
### Also , since pip module didn't work well with data files,
### fool it with naming data files as words_txt.py instead of words.txt
###

#Option 1 - filter words above some length
def length_sorter(longword):
	"""
		print all words only beyond some length
	"""
	print ' '
	count = 0
	fin = open('words_txt.py')
	for line in fin:
		word = line.strip()#get rid of \r
	
		if len(word) >=longword:
			print word
			time.sleep(1)
			count = count + 1
	
	print '\nTotal words printed : ',count
	print ' '
	time.sleep(0.5)

#common
def has_no_e(word,substring):
	"""
		check if given word has that substring
		e is the most common char ~ 67 percent frequency
 	"""
	#for char in word:
	#	if char==letter:
	#		return False
	#return True
 	bool = substring in word
	return not bool		#allows flexibility for substring

#Option2
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


#option 3 & 4
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


#option 5
def is_abecedarian(word):
	"""
		check if given word is alphabetically arranged
	"""
	prev = word[0]
	for char in word:
		if char < prev:
			return False
		prev = char

	return True


#option 6 - find words containing a substring
def total_words(filename='words_txt.py'):

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
	fin = open('words_txt.py')
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


#option 7
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
	fin = open('words_txt.py')
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


#option 8 - how popular each char is
#plotter
def get_10s_power(num) : 
	"""
		get ceil(log num to base 10)
	"""
	duply = num
	power = 0
	while duply>1:
		power += 1
		duply /= 10

	return pow(10,power-1)

def plot_letters(letters,frequency):
	"""
		Takes 2 lists as input and prints graph
		x axis : letters
		y axis : frequency
	"""
	plt.plot(letters,frequency,'r')
	plt.title('Alphabet wise arrangement')
	plt.xlabel('Alphabets')
	plt.ylabel('Frequency')

	x_max = max(letters) + get_10s_power(max(letters))
	y_max = max(frequency) + get_10s_power(max(frequency))
	plt.axis([0, x_max, 0, y_max])#xmin , xmax , ymin , ymax
	#y max at e - 76168
	plt.show()

#Actual function for allstars
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
	
		book = booker_most_frequent.read_file('words_txt.py')
		result , tots = most_frequent(book)
		
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


#option 9 - find word in dict
def create_dict(filename='words_txt.py'):
	"""

		Add each string as key in a dict
	"""
	word_dict = dict()
	fin = open(filename)

	for line in fin:
		word = line.strip()
		word = word.lower()
		word_dict[word] = word

	return word_dict

def is_there_dict(word):
 	"""

 		Use your in method to find , because #tables were made for you
 	"""
	start_time = time.time()
	source = create_dict()
	print '\n',word,'in dict : ',word in source

	elapsed_time = time.time() - start_time
	#print 'elapsed_time :',elapsed_time,'seconds'
	# upto 50 % better - check where this backtracks to in wordabulary


#option 10 - check if reverse of word is a word as well
def in_bisect(word_list, word):
    """

    	Binary search for word in sorted word_list
    """
    i = bisect_left(word_list, word)
    if i != len(word_list) and word_list[i] == word:
        return True
    else:
        return False

def word_list():
    """
    	Prepare word list to search in
    """
    word_list = []
    fin = open('words_txt.py')

    for line in fin:
        word = line.strip()
        word_list.append(word)
    
    return word_list

def is_reverse_there(word_list, word):
    """

        Checks whether a reversed word appears in word_list.
    """
    rev_word = word[::-1]
    return in_bisect(word_list, rev_word)
        

def reverse_pairs(char):
    """
    
        print all reverse pair words
    """   
    listed = word_list()
    count = 0 

    for word in listed:

        if char!='*':
            if word[0]!=char:
                continue
                #continue if word doesn't begin with letter

        if is_reverse_there(listed, word):
            count += 1
            print word, word[::-1]
            time.sleep(0.01)
            if char!='*':
                time.sleep(0.04)#so le jara , so le jara

    print '\nTotal words : ',count,'\n'


#option 11 - interlocked words - alter chars make two dictionary words
def is_interlock(word_list, word):
    """

    	Checks whether a word can be split into two interlocked words.
    """
    evens = word[::2]
    odds = word[1::2]
    return in_bisect(word_list, evens) and in_bisect(word_list, odds) 
        

def interlock_general(word_list, word, n=2):
    """

    	Checks whether a word can be split into n interlocked words.

    	Extension of problem
    """
    for i in range(n):
        inter = word[i::n]
        if not in_bisect(word_list, inter):
            return False
    return True
        
def interlocked():
    """

    	iterator , nothing else
    """
    listed = word_list()
    count = 0
    for word in listed:
        if is_interlock(listed, word):
            print word, word[::2], word[1::2]
            count += 1
            time.sleep(0.04)

    print '\nTotal interlocked words : ',count,'\n'

    #May change to start from some letter , but not required

#    for word in word_list:
#        if interlock_general(listed, word, 3):
#            print word, word[0::3], word[1::3], word[2::3]


#option 12 - char dist of string
def histogram(string):
	"""

		provide a dict which returns char-wise distribution
	"""
	d = dict()
	for char in string:
		#check deprecated folder for naive
		d[char] = d.get(char,0) + 1
				#	get key , default_value

	return d

def print_hist(h):
	for char in h:
		print char , h[char]


#option 13 - rotate words for encoding / decoding
def rotate_letter(letter, n):
    """
        Rotate a letter by n places
    """
    if letter.isupper():
        start = ord('A')
    elif letter.islower():
        start = ord('a')
    else:
        return letter

    c = ord(letter) - start
    i = (c + n) % 26 + start
    return chr(i)


def rotate_word(word, n,encode_bool=True):
    """
        Rotate a word by n places.

        encode_bool = True =>encode
        else decode
    """

    out_str = ''
    if encode_bool==False:
        n = -1*n

    for letter in word:
        out_str += rotate_letter(letter, n)
    return out_str

def starts_with(substr,word):
    """

        return true if word starts with substr
    """
    l = len(substr)
    if len(word) < l:
        return False

    for i in range(l):
        if word[i]!=substr[i]:
            return False

    return True


def rotate_pairs(word, word_dict,table,count):
    """

    	Prints all words that can be generated by rotating word.
    """
    for i in range(1, 14):
        rotated = rotate_word(word, i)
        if rotated in word_dict:

            #global table
            table.add_row([word,i,rotated])
            #print word, i, rotated

            count += 1
            time.sleep(0.01)


def iterate_rotors(substr):
    """

		Function to work of main in case imported as module
        prints only words starting with substr
    """
    count = 0
    table = PrettyTable(['Word','rotate id','rotated word'])

    word_dict = create_dict()
    for word in word_dict:
        if starts_with(substr,word):
            rotate_pairs(word, word_dict,table,count)

    print table
    time.sleep(1)
    print '\nTotal rotated pairs :',count 


#option 14  pronounce
def guide():
    """

        print guide for pronunciation 
        needs file c06d_guide - available on below website
    """
    fin = open('c06d_guide.py')
    table = PrettyTable(['Phoneme','example','Translation'])

    for line in fin:

        #skip the comments
        if line[0] == "#":continue

        t = line.split()
        phoneme = t[0]
        example = ' '.join(t[1:2])
        translation = ' '.join(t[2:])
        table.add_row([phoneme,example,translation])
    print table


def pronounce_dict(filename='c06d.py'):
    """

        Build a dictionary from file 
        (c06d , courtesy of the CMU pronouncing dictionary)
        visit these guys at http://www.speech.cs.cmu.edu/cgi-bin/cmudict

        d[word] = pronunciation 
        words in alternate pronunciation ,have pronunciation described by (2)
    """
    d = dict()
    fin = open(filename)
    for line in fin:

        # skip over the comments
        if line[0] == '#': continue

        t = line.split()
        word = t[0].lower()
        pron = ' '.join(t[1:])
        d[word] = pron

    return d

def print_pronounce(word): 
    d = pronounce_dict()

    nada = '0'
    for k, v in d.items():
        if k==word:
            return v

    return nada

#option 15 - rhyme for a dime
def create_word_dict(filename='c06d.py'):
    """

        Build a dictionary from file only for keys
    """
    d = dict()
    fin = open(filename)
    for line in fin:

        # skip over the comments
        if line[0] == '#': continue

        t = line.split()
        word = t[0].lower()
        d[word] = word

    return d


def check_rhyme(singel,word,word_dict,phonetic):
    """

        check if word rhymes with singel 

        word: string
        #word_dict: dictionary with words as keys
        #phonetic: map from words to pronunciation codes
    """

    p_a = phonetic[singel]
    p_b = phonetic[word]

    a = p_a[::-1].split()
    b = p_b[::-1].split()

    if a[0]==b[0]:
        return True
    else:
        return False


def rhyming(singel,starts):
    """
        print rhyming words using the cmu dictionary
    """

    phonetic = pronounce_dict()
    word_dict = create_word_dict()
    
    if not singel in word_dict:
        print '\nNot a valid word\n returning ....'
        return


    #creating list for alphabetical order
    listed =[]
    count = 0
    for word in word_dict:

        #only need to filter if not all required to print
        if starts!= '*' :
            if starts_with(starts,word):
                if check_rhyme(singel,word, word_dict, phonetic):
                    listed.append(word)
                    count += 1
        else :
            if check_rhyme(singel,word, word_dict, phonetic):
                    listed.append(word)
                    count += 1

    listed.sort()
    for word in listed:
        print word
        time.sleep(0.1)

    print '\nTotal alternatives : ',count,'\n'


#option 16 - crossword aid
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


#option 17 - books and stuff

def total_freq(t):
    """

        Return total occurences of letters
    """
    count = 0
    for freq,x in t:
        count += freq
    return count


def read_file(filename):
    return open(filename).read()


def char_histogram(s):
    """

        Make a map from letters to number of times they appear in s.
        Returns: map from letter to frequency
    """
    hist = {}
    for x in s:
        x = x.lower()
        hist[x] = hist.get(x, 0) + 1
    return hist


#you might want to look at deprecated/ this file for naive implementation
def word_histogram(doc):
    hist = {}
    fp = file(doc)

    punctuation = string.punctuation
    for line in fp:
        # replace hyphens with spaces before splitting
        line = line.replace('-', ' ')
    
        for word in line.split():
            # remove punctuation and convert to lowercase
            word = word.strip(string.punctuation + string.whitespace)
            word = word.lower()

            # update the histogram
            hist[word] = hist.get(word, 0) + 1

    return hist


def most_frequent(doc,typef='char',to_limit=False):
    """

        Sorts the typef in doc in reverse order of frequency.
        return reverse sorted version along with num_words in doc.
    """
    if typef =='char':
        hist = char_histogram(doc)

    elif typef =='word':
        hist = word_histogram(doc)

    t = []
    for x, freq in hist.iteritems():
        t.append((freq, x))

    t.sort(reverse=True)
    result = []
    #list of tuples
    limit = 0# to limit only 20 most frequent words
    tots = total_freq(t)
    for freq, x in t:
        
        percentage = get_percent_in2points(freq,tots)
        result.append((x,freq,percentage))

        if typef=='word'and to_limit==True:
            limit += 1
            if limit==20:
                break

    return result,tots


def iterate_booker(filer,typef='char'):
    """
		main function module
    """
    if not os.path.isfile(filer):
        print '\tNot a valid file !Returning now...'
        return 

    to_limit = False#Limit table display size for large docs

    print '\tFile found!Working ...'
    if typef=='char':
        doc = read_file(filer)
        out,tots = most_frequent(doc,'char')
        table = PrettyTable(['Char','Freq','%'])
    
    elif typef=='word':   
        print '\tNOTE : If your file is too big , the analysis may take a long time'
        to_limit = raw_input("\tEnter y to limit display top 20 entities : ")
        if to_limit=='y':
            to_limit = True
        
        out,tots = most_frequent(filer,'word',to_limit)
        table = PrettyTable(['Word','Freq','%'])

    for x,freq,percent in out:
        table.add_row([x,freq,percent])

    print table
    time.sleep(1)
    print '\tTotal entities in document : ',tots
    print '\tTotal unique entities : ',len(out)


#you might want to look at deprecated/ this file for naive implementation
def check_data(transcript,reference_dict):
	"""

		return a dictionary of words in transcript not in reference_dict
		Effectively , these are percieved as misspelled words.
	"""
	incorrect_dict = dict()
	count = 0
	for key ,freq,percent in transcript:

		if key not in reference_dict:
			#print key,' not in dict'
			incorrect_dict[key] = 'suggest_correction_here'
			count += freq	# a word may be misspelled multiple times

	return incorrect_dict,count


def booker_correct(filer):
	
	if not os.path.isfile(filer):
		print '\tNot a valid file !Returning now...'
		return 

	out,tot_words_doc = most_frequent(filer,'word')
	reference_dict = create_dict()

	incorrect_dict,count = check_data(out,reference_dict)
	print '\n'	
	for key in incorrect_dict:
		print '\t',key

	time.sleep(2)
	print '\n\tTotal misspelled occurences : ',count


#booker submenu
def booker_initialise():
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
		print '\tTIP : start with / '
		if option=='0' or option=='clear':
			break


		elif option=='1':
			filer=raw_input("\tEnter your file for frequency distribution:\n\t")
			iterate_booker(filer,'char')	
		
		elif option=='2':
			filer=raw_input("\tEnter your file for word distribution:\n\t")
			iterate_booker(filer,'word')

		elif option=='3':
			filer = raw_input("\tEnter your file for typos:\n\t ")
			booker_correct(filer)	


		else :
			print '\tIncorrect choice :(\n'

		time.sleep(1)
		print '\n'


#option 18 - anagrams
def contents_of(word):
	"""

		return a string containing all letters in order
	"""
	c = list(word)
	c.sort()
	c = ''.join(c)
	return c


def find_anagrams(word,filename='words_txt.py'):
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


def print_anagrams(word,filename='words_txt.py'):
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
		print '13 for to find if the word can be rotated within dictionary'
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
			length_sorter(longword)


		elif option=='2':
			not_letters = raw_input("Enter forbidden letter(s) ,separated by , : ").split(",")
			#not_let = map(char,not_letters.split(","))

			word=raw_input("Enter word to check for forbidden letter(s) : ")
			has_no_these(word,not_letters,True)#allow printing


		elif option=='3':
			only_letters = raw_input("Enter allowed letter(s), unseparated: ")

			word=raw_input("Enter word to check for allowed letter(s) : ")
			has_only_these(word,only_letters,True)#allow printing


		elif option=='4':
			fixed_letters = raw_input("Enter allowed letter(s), unseparated: ")

			word=raw_input("Enter word to check if all allowed letter(s) are present: ")
			has_only_these(fixed_letters,word,True)#allow printing


		elif option=='5':
			word = raw_input("Enter word to be checked for abecedarian : ")
			print is_abecedarian(word)		


		elif option=='6':
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

			#else:
			#	print 'char needs to be a single letter!'


		elif option=='7':
			#extend later to rhyming words - sky , bye
			substring=raw_input("Enter substring to check words which end with it : ")
			#printing mandatory
			ends_with(substring)


		elif option=='8':
			print 'Crunching numbers ... displaying count of words containing each letter'
			allstar_words()


		elif option=='9':
			search_this = raw_input("Enter word to search for , in database : ")
			
			#	dict method faster upto 50% - for word boy - 0.06 and 0.04 resp
			#										map for worst case
			# check speed , uncomment time prints in these files v

			#print 'Method 1 : list and append'
			#is_there.is_there(search_this)
			#print 'Method 2 : dict()'
			is_there_dict(search_this)


		elif option=='10':
			print 'Displaying all reverse pairs:'
			char = raw_input("Begin with what letter? (* for complete) : ")
			reverse_pairs(char)


		elif option=='11':
			interlocked()


		elif option=='12':
			inp_str = raw_input("Enter string to obtain histogram : ")
			hist = histogram(inp_str)

			print hist,'\n'
			print_hist(hist)


		elif option=='13':
			substr = raw_input("Enter substring from which words are to be rotated : ")
			iterate_rotors(substr)


		elif option=='14':
			word = raw_input("Enter word to pronounce :")

			pron = print_pronounce(word)
			if pron!='0':
				print 'Pronounce as : ',pron

				show_guide = raw_input("Enter y to see pronounciation guide : ")
				if show_guide=='y':
					guide()
					
			else:
				print 'Pronunciation not found! Did you enter a valid word ? Check using option 9'


		elif option=='15':
			word = raw_input("Enter word for which rhyming words are needed : ")
			substr = raw_input("start with any substr ? enter * for all : ")
			rhyming(word,substr)

		elif option=='16':
			print 'Do you wonder what is 6 letter word with y as 2nd letter and ends with n ?'
			time.sleep(1)
			print 'i.e, a word _y___n ?\nThis is perfect for you !'
			time.sleep(1)
			print 'just type _y__n or -y--n and voila , all possibilities are given!'
			print 'Psst : it\'s python'
			time.sleep(1)
			mystery_word = raw_input("\nEnter your mystery word in the above format : ")
			crossword(mystery_word)



		elif option=='17':
			booker_initialise()


		elif option=='18':
			word = raw_input("Enter word to check all its anagrams : ")
			print_anagrams(word)


#Total number of words = 113809 - now updated ! - has some 380000+ords
		else :
			print 'Incorrect choice :(\n'