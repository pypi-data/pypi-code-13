""" This is the module that provides one function called 'list_di(list)',
    you can input the list and it will print the dict with serial number.
    """

def list_di(s):
    y=list(range(1,len(s)+1))
    x=0
    d={}
    while x < len(s):
        print(y[x],':',s[x])
        d[y[x]] = s[x]
        x = x+1
    print(d)
