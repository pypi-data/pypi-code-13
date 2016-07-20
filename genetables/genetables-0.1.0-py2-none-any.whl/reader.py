# reader.py


# Copyright (C) 2016 - Sven E. Templer <sven.templer@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT
# OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


### readline_rnafold

# i = open(path)
# s = logical (strip '>' from fasta id)

def readline_rnafold(i, s = False):
    v = []
    try:
        line = i.readline() # read header
        line = line.strip()
        if s:
            line = line[1:] # drop fasta header '>'
        v.append(line)
        line = i.readline() # skip sequence line
        line = i.readline() # read structure + energy
        line = line.strip()
        line = line[:-1] # drop bracket and newline
        line = line.split(' (') # split structure from energy
        line[1] = line[1].strip()
        #if line[1][0] == ' ':
        #    line[1] = line[1][1:] # drop space before energy value
        #if line[1][0] == ' ':
        #    line[1] = line[1][1:] # drop space before energy value
        v.extend(line)
        return v
    except:
        return None
    

### readline_bam

# i = pysam.AlignmentFile(path).fetch()

def readline_bam(i):
    v = []
    try:
        line = i.next()
        v.append(line.query_name)
        v.append(line.reference_name)
        v.append(str(line.pos))
        return v
    except:
        return None
    

