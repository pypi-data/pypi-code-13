import os.path
import time
from prettytable import PrettyTable
import string

## further - remove stop_words from importer


####
####    NOTE : booker_most_frequent counts all occurences while
####            allstar_words checks for number of words , they are different !
####
# this function pasted here as this file is imported in allstar for most_frequent
def get_percent_in2points(freq,total):
    """
        get percent of total from freq as xx.xx%
    """
    percent = 100.0*freq/total
    percent = int(100*percent)/100.0
    return percent


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

    to_limit = False#Limit table display sie fr large docs

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


if __name__ == '__main__':
    
    print '\t1 for finding most frequent chars in a book(txt file)'
    print '\t2 for finding most frequent words in a book(txt file)'
    print '\n\t and 0 to exit this submenu'
    
    option = raw_input("\tYour choice :")
    print '\tTIP : start with / if address for file is not local'

    if option=='0' or option=='clear':
        exit

    elif option=='1':
        filer=raw_input("\tEnter your file for frequency distribution:\n\t")
        iterate_booker(filer,'char')   
        
    elif option=='2':
        filer=raw_input("\tEnter your file for word distribution:\n\t")
        iterate_booker(filer,'word')

    else :
        print '\tIncorrect choice :(\n'
