from bisect import bisect_left
#Perfect example of hiding in plain sight
import time

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
    fin = open('reference/words.txt')

    for line in fin:
        word = line.strip()
        word_list.append(word)
    
    return word_list


def is_there(word):
    """

		search for given word with binary sort
		You'd think , you could just do 
		word in list , n00b
		Guess what,  it would take you ages !Go ahead , smarta$$
    """
    start_time = time.time()
    listed = word_list()
    print '\n',word, 'in list : ', in_bisect(listed,word)
    elapsed_time = time.time() - start_time
    #print 'elapsed_time :',elapsed_time,'seconds'


#main function removed as deprecated
#not in deprecated as essential for reverse_pairs in_bisect is used