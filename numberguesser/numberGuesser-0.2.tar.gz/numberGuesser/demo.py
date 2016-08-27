import random



#  Create a function for asking for a guessed number
def guessGen():
    randNum = random.randint(0, 101)
    guessRemain = 5
    while guessRemain > 0:
        numGuess = int(raw_input("Please Pick a number from 1-100 ==> "))
        if (numGuess > randNum):
            guessRemain -= 1
            print "You guessed %r the actual number is lower please try again you have %r remaining" % \
                  (numGuess, guessRemain)
            continue
        elif (numGuess < randNum):
            guessRemain -= 1
            print "Your guess is %r you must guess higher you have %r guesses remaining" % (numGuess, guessRemain)
            continue
        elif (numGuess == randNum):
            print "You guessed %r which is correct you win thanks for playing" % numGuess
            break
        else:
            print "Please select a number"
    print "The random number was %r" % randNum
guessGen()
#print "This is at the complete bottom of program and the random number is in fact %r" % randNum

