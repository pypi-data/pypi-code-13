# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://bitbucket.org/ned/coveragepy/src/default/NOTICE.txt

# A test case sent to me by Steve White

def f(self):
    if self==1:
        pass
    elif self.m('fred'):
        pass
    elif (g==1) and (b==2):
        pass
    elif self.m('fred')==True:
        pass
    elif ((g==1) and (b==2))==True:
        pass
    else:
        pass

def g(x):
    if x == 1:
        a = 1
    else:
        a = 2

g(1)

def h(x):
    if 0:   #pragma: no cover
        pass
    if x == 1:
        a = 1
    else:
        a = 2

h(2)
