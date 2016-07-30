import os

print("The current working directory is")
print(os.getcwd())
print()
os.chdir('C:\\Users\\Harkit\\Documents\\Python\\HeadFirstPython\\Chapter3')
print("Current working directory changed to")
print(os.getcwd())
print()

man=[] # Creates array called man
otherMan=[] # Creates array called otherMan

try:
    data = open('sketch.txt')
    print("The Sketch")

    for each_line in data:
        try:
            (role,lineSpoken) = each_line.split(':',1)
            lineSpoken = lineSpoken.strip()
            # The if and elif statements append line spoken based on role
            # into respective arrays declared above
            if role == 'Man':
                man.append(lineSpoken)
            elif role == 'Other Man':
                otherMan.append(lineSpoken)
            # The three print statements print the role and line spoken
            # to the screen.
            """print(role, end='')
            print(':', end='')
            print(lineSpoken, end='')"""
        except ValueError:
            pass
        
    data.close()
except IOError:
    print("File does not exist")

# The two print commands and the two for loops print the contents
# of the arrays to the screen
"""
print(man)
print(otherMan)

for eachSentence in man:
    print(eachSentence)

for eachSentence in otherMan:
    print(eachSentence)
"""

# The try/except block will write the arrays to separate text files
try:
    manFile = open('manData.txt','w')
    otherManFile = open('otherManData.txt','w')
    for eachSentence in man:
        print(eachSentence, file=manFile)
    for eachSentence in otherMan:
        print(eachSentence, file=otherManFile)
except IOError:
    print("File error")
finally:
    manFile.close()
    otherManFile.close()    


    
