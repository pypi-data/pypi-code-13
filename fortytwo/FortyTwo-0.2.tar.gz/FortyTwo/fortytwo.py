#     _____  ________
#    /  |  | \_____  \
#   /   |  |_ /  ____/
#  /    ^   //       \
#  \____   | \_______ \
#       |__|         \/
#
# This is the personal python module of 1m0r74l17y
# containing all the important stuff maybe needed.

###############################################################

# This is an email generator for buisness use.
# it will output either to the terminal, or
# a self generated file.
def emailgenerator(First,Last,Domain,Out):
    #first a list with all the email are generated.
    email_list = []
    email_list.append(First + Last + '@' + Domain)
    email_list.append(First + '.' + Last + '@' + Domain)
    email_list.append(First[0] + '.' + Last + '@' + Domain)
    email_list.append(First + '.' + Last[0] + '@' + Domain)
    email_list.append(First[0] + Last + '@' + Domain)
    email_list.append(First + Last[0] + '@' + Domain)
    email_list.append(Last + First + '@' + Domain)
    email_list.append(Last + '.' + First + '@' + Domain)
    email_list.append(Last[0] + '.' + First + '@' + Domain)
    email_list.append(Last + '.' + First[0] + '@' + Domain)
    email_list.append(Last[0] + First + '@' + Domain)
    email_list.append(Last + First[0] + '@' + Domain)
    #then it decides if it should print or write.
    if Out.lower() == "raw":
        for item in email_list:
            print(str(item) + "\n")

    else:
        fil = open(First + Last + '@' + Domain + ".txt", "w")

        for item in email_list:
            fil.write(str(item) + "\n")

        fil.close()

###############################################################

# This is a loading animation, that can be used for
# showing that the program is not dead yet
def loading(Animation,Loops,Delay):
    import time,sys
    run = True
    while run:
        for i in range(Loops):
            for l in range(len(Animation)):
                sys.stdout.write(Animation[l])
                sys.stdout.flush()
                sys.stdout.write('\b')
                time.sleep(Delay)
        run = False

###############################################################

# This is a quadratic equation solver, that can be
# used for solving quadratic equations fast, in
# school. I have used it plenty o' times myself.

def quadraticequation(A, B, C):
    import math
    D = B*B-(4*A*C)
    print "d : " + str(D)
    if D == 0.0 or 0:
        sqrtd = math.sqrt(D)
        x = -B/(2*A)
        print "x : " + str(x)
    if D < 0:
        print "there is no x."
    if D > 0:
        sqrtd = math.sqrt(D)
        x1 = (-B+sqrtd)/(2*A)
        print "x+ : " + str(x1)
        x2 = (-B-sqrtd)/(2*A)
        print "x- : " + str(x2)

###############################################################

# This is a likesystem for the website filmlinjen.dk
# It can be used for getting likes on your videos,
# and win competitions in your class.

def likefilmlinjen(productionId, likecount):
    import urllib2
    productionId = str(productionId)
    for i in range(likecount):
        urllib2.urlopen('http://filmlinjen.dk/umbraco/surface/ProductionsSurface/IncrementLikes?productionId=' + productionId +  '&timestamp=635962278782832032')

###############################################################

# This is a function for testing if a number is a prime.
# I think it is very clever and it works fine.
def isPrime(num):
    return num > 1 and not any(num % n == 0 for n in range(2,num))

###############################################################

# This section is to be overseen, dont look, just keep scrollin'
# Added this just because.

def add(a,b):
    return a+b

def subtract(a,b):
    return a-b

def multiply(a,b):
    return a*b

def divide(a,b):
    return a/b

###############################################################

# This is a function for finding... i dont even know how to
# explain this, but its here anyway.

def sumsquaredifference(Number):
    sumofsquares = 0
    for num in range(Number):
        sumofsquares = sumofsquares + num*num
    squareofsums = sum(range(Number)) ** 2
    return squareofsums - sumofsquares

###############################################################

# No need to explain this.
# (Opens cd drive. Just hide it in your code)
# WORKS ON LINUX ONLY, i think.
def nope():
    import os
    os.system("eject cdrom")

###############################################################

# This is just to return the n'th fibbonachi number.

def fib(Number):
    f1,f2 = 1,1
    run = 0
    while run<Number - 3:
        f1,f2 = f2,f1+f2
        print f2
        run += 1
    return f2

###############################################################
