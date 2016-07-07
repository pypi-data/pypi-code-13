from is_there import *
import time
#schooled is interlocked - s h o e + c o l d
# importing from is_there as it is heavily dependent

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


if __name__ == '__main__':
    interlocked()