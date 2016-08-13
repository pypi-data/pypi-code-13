# SMOP -- Simple Matlab/Octave to Python compiler
# Copyright 2011-2016 Victor Leikehman

import version
import sys,cPickle,glob,os
import getopt,re
import lexer,parse,resolve,backend,options,node,graphviz
import callgraph
import networkx as nx
import pickle
import readline
import graphviz

#from runtime import *
#from version import __version__
__version__ = version.__version__

def main():
    """
    !a="def f(): \\n\\treturn 123"
    !exec a
    !print f
    !print f()
    !reload(backend)
    =>> function t=foo(a) \\
    ... t=123
    !exec foo(3)
    """
    symtab = {}
    print "? for help"
    while 1:
            buf = raw_input("octave: ")
            if not buf:
                continue
            while buf[-1] == "\\":
                buf = buf[:-1] + "\n" + raw_input("... ")
            if buf[0] == '?':
                print main.__doc__
                continue
            if buf[0] == "!":
                try:
                    exec buf[1:]
                except Exception as ex:
                    print ex
                    continue
            t = parse.parse(buf if buf[-1]=='\n' else buf+'\n')
            if not t:
                continue
            #print "t=", repr(t)
            #print 60*"-"
            resolve.resolve(t,symtab)
            #print "t=", repr(t)
            #print 60*"-"
            print "symtab:",symtab
            s = backend.backend(t)
            print "python:",s.strip()
            try:
                #exec s
                pass
            except SyntaxError:
                print "smop: syntax error"
            except EOFError:
                return
            except Exception as ex:
                print ex

if __name__ == "__main__":
    main()
