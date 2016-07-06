from random import randint

def fun():
    result = randint(0,100)
    return result

def more_fun():
    x = fun() - 100
    return x

more_fun()
