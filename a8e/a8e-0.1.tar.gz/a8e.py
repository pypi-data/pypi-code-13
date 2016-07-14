#!/usr/bin/env python

import sys
import urllib2

def a8e(text):
  text = text.split()
  retval = []
  for word in text:
    if len(word) < 4:
      retval.append(word)
    else:
      retval.append(word[0] + '%d' % (len(word) - 2) + word[-1])
  return ' '.join(retval)

def main(args=sys.argv[1:]):
  if len(args) == 1 and (args[0].startswith('http://')
                         or args[0].startswith('https://')):
    text = urllib2.urlopen(args[0]).read()
  else:
    text = ' '.join(args)
  # TODO: read from stdin if no args
  print a8e(text)

if __name__ == '__main__':
  main()
  
