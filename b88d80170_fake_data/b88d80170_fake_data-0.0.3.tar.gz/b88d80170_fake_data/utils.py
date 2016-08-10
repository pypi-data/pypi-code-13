import random


def pickone(l):
    return l[random.randint(0, len(l) - 1)]


# c is a float number between 0 and 1
def pickchance(c):
    return random.random() <= c


def random_int_list(numdigit):
    l = str()
    for i in range(numdigit):
        l += str(random.randint(0, 9))
    return l
