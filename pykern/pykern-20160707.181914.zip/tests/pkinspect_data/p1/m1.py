class C():
    pass

v = 1
c = C()

from pykern import pkinspect

def caller_module():
    return pkinspect.caller_module()

def is_caller_main():
    return pkinspect.is_caller_main()
