from pronounce import pronounce_dict
from rotate_pairs import starts_with
import time

def create_word_dict(filename='reference/c06d'):
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



if __name__ == '__main__':
                
    word = raw_input("Enter word for which rhyming words are needed : ")
    substr = raw_input("start with any substr ? enter * for all : ")
    rhyming(word,substr)