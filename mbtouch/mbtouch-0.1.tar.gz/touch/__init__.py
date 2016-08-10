import os

def touch(fname):
    if os.path.exists(fname):
        os.utime(fname, None)
    elif not os.path.isdir(fname.rsplit('/',1)[0]):
        os.makedirs(fname.rsplit('/',1)[0])
        open(fname, 'a').close()
    else:
        open(fname, 'a').close()

