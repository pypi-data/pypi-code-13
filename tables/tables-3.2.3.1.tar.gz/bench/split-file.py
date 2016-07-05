"""
Split out a monolithic file with many different runs of
indexed_search.py. The resulting files are meant for use in
get-figures.py.

Usage: python split-file.py prefix filename
"""

import sys

prefix = sys.argv[1]
filename = sys.argv[2]
f = open(filename)
sf = None
for line in f:
    if line.startswith('Processing database:'):
        if sf:
            sf.close()
        line2 = line.split(':')[1]
        # Check if entry is compressed and if has to be processed
        line2 = line2[:line2.rfind('.')]
        params = line2.split('-')
        optlevel = 0
        complib = None
        for param in params:
            if param[0] == 'O' and param[1].isdigit():
                optlevel = int(param[1])
            elif param[:-1] in ('zlib', 'lzo'):
                complib = param
        if 'PyTables' in prefix:
            if complib:
                sfilename = "%s-O%s-%s.out" % (prefix, optlevel, complib)
            else:
                sfilename = "%s-O%s.out" % (prefix, optlevel,)
        else:
            sfilename = "%s.out" % (prefix,)
        sf = file(sfilename, 'a')
    if sf:
        sf.write(line)
f.close()
