

import pymp4parse

filename = '/etc/resolv.conf'
myf = open(filename, 'rb')
my_bytes = myf.read()

print( pymp4parse.F4VParser.is_mp4_s(my_bytes) )