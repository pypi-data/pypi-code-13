#!/usr/bin/env python

from operator import itemgetter
import sys

word2count = {}
ctr = 1
word2 = "bar"
Str = ["bar 1","foo 1","foo 1","foo 1","labs 1","quxx 1","quxx 1"]
for each_item in Str:
    line = each_item
    line = line.strip()
    word,count = line.split(' ',1)
    #print (word,count)
    
    count = int(count)
    word2count[word] = word2count.get(word,0) + count
    #word2count[word] = word2count.get(word,0)
    #print(count)
    #print (word2count.get(word,0))
    
    if (word2 != word):
       ctr = ctr + 1
       print(word2,word2count[word2])
    word2 = word
print(word2,word2count[word2])
