import sys
import os
def printabc(a_list,ok=sys.stdout,indent=False,level=0):
    for a in a_list:
        if isinstance(a,list):
            printabc(a,ok,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end='',file=ok)
            print(a,file=ok)





