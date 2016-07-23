#This is the “Summation.py" module, and it provides one function called
#sumUpNumber() which will sum up all the numbers you have input into it

def sumUpNumber(*args):
    #Your input will be any number, any length of parameters 
    #into this function and it will return the total
    total = 0
    for arg in args:
        total += arg
    return total
