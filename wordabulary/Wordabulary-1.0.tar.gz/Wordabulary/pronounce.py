from prettytable import PrettyTable


def guide():
    """

        print guide for pronunciation 
        needs file c06d_guide - available on below website
    """
    fin = open('reference/c06d_guide')
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


def pronounce_dict(filename='reference/c06d'):
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


if __name__=='__main__':
    word = raw_input("Enter word to pronounce :")

    pron = print_pronounce(word)
    if pron!='0':
        print 'Pronounce as : ',pron

        show_guide = raw_input("Enter y to see pronounciation guide : ")
        if show_guide=='y':
            guide()
                    
    else:
        print 'Pronunciation not found! Did you enter a valid word ? Check using option 9'    
