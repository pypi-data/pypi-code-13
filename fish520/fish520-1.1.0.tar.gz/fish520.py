"""csccsssss"""
def printabc(a_list):
    for a in a_list:
        if isinstance(a,list):
            printabc(a)
        else:
            print(a)



