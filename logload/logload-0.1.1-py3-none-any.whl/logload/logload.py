
### generator
import random

class Fragment:
    def expand(self):
        return ""

class RandomSelection(Fragment):
    def __init__(self, lis):
        self.lis = lis
        random.shuffle(self.lis)
        self.length = len(lis)
        self.ptr = 0

    def expand(self):
        self.ptr = self.ptr + 1
        if self.ptr >= self.length:
            self.ptr = 0
        return self.lis[self.ptr]

class RandomWord(Fragment):
    def __init__(self, name):
        self.name = name
        with open('logload/words.txt') as x: self.words = x.readlines()

    def expand(self):
        return random.choice(self.words)
    
class StaticSelection(Fragment):
    def __init__(self, s):
        self.s = s

    def expand(self):
        return self.s

from datetime import datetime

class Timestamp(Fragment):
    def expand(self):
        dt = datetime.now()
        return dt.isoformat()
    
### tokenizer

from re import VERBOSE

from funcparserlib.lexer import make_tokenizer, Token

regexps = {
    'escaped': r'''
        \\                                  # Escape
          ((?P<standard>["\\/bfnrt])        # Standard escapes
        | (u(?P<unicode>[0-9A-Fa-f]{4})))   # uXXXX
        ''',
    'unescaped': r'''
        [^"\\]                              # Unescaped: avoid ["\\]
        ''',
}

def tokenize(string):
    """ str -> Sequence(Token) """
    specs = [
        ('Space', (r'[ \t\r\n]+', )),
        ('String', (r'"(%(unescaped)s | %(escaped)s)*"' % regexps, VERBOSE)),
        ('Op', (r'[\[\],()]', )),
        ('Name', (r'[A-Za-z_][A-Za-z_0-9]*',)),
    ]
    empty = ['Space']
    t = make_tokenizer(specs)
    return [x for x in t(string) if x.type not in empty]

### parser

class FunctionNameError(Exception):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "Name not available: " + self.name

import re

re_esc = re.compile(regexps[u'escaped'], VERBOSE)

from funcparserlib.parser import (some, maybe, many, finished, skip, a)

def parse(seq):
    tokval = lambda x: x.value
    toktype = lambda t: some(lambda x: x.type == t) >> tokval
    op = lambda s: a(Token('Op', s)) >> tokval
    op_ = lambda s: skip(op(s))

    def make_group(n):
        if n is None:
            return RandomSelection([])
        else:
            return RandomSelection([n[0]] + n[1])

    def make_list(n):
        if n is None:
            return []
        else:
            return [n[0]] + n[1]
        
    def unescape(s):
        std = {
            u'"': u'"', u'\\': u'\\', u'/': u'/', u'b': u'\b', u'f': u'\f',
            u'n': u'\n', u'r': u'\r', u't': u'\t',
        }

        def sub(m):
            if m.group('standard') is not None:
                return std[m.group('standard')]
            else:
                return chr(int(m.group('unicode'), 16))

        return re_esc.sub(sub, s)

    def make_name(n):
        if n == "randword":
            return RandomWord(n)
        elif n == "timestamp":
            return Timestamp()
        else:
            raise FunctionNameError(n)
    
    def make_string(n):
        return unescape(n[1:-1])

    name = toktype('Name') >> make_name
    string = toktype('String') >> make_string
    atom = string | name
    
    group = (
        op_('[') +
        maybe(atom + many(op_(',') + atom)) +
        op_(']')
        >> make_group)

    value = atom | group
    
    lis = (
        op_('(') +
        maybe(value + many(op_(',') + value)) +
        op_(')')
        >> make_list)

    logload = lis | value
    logload_text = logload + skip(finished)

    return logload_text.parse(seq)

### main & options

class LogLineGenerator:

    def set_pattern(self, pat):
        self.spec = parse(tokenize(pat))

    def execute(self, spec):
        if type(spec) is list:
            return ''.join([ self.execute(sp) for sp in spec])
        if type(spec) is str:
            return spec
        if isinstance(spec, Fragment):
            return spec.expand()
        
        
    def lines(self, i):
        return [self.execute(self.spec) for x in range(i)]

import argparse
import socket
from time import clock, sleep, time

class ConnectFailedError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "Failed to connect: {}".format(self.msg)

def get_client_sock(host, port):
    sock = None
    addr = socket.getaddrinfo( host, port, proto=socket.IPPROTO_TCP )

    for res in addr:
        af, socktype, proto, dummy, sa = res
        try:
            sock = socket.socket(af, socktype, proto)
        except OSError:
            sock = None
            continue
        try:
            sock.connect(sa)
        except OSError:
            sock.close()
            sock = None
            continue
        break

    if not sock:
        raise ConnectFailedError("could not connect")

    return sock

def main():
    parser = argparse.ArgumentParser(description="Load-test syslog servers")
    parser.add_argument('-H', dest='host', help='target to log to', default='localhost')
    parser.add_argument('-p', dest='port', type=int, help='target port to log to', default=514)
    parser.add_argument('-l', dest='pattern', help='logging pattern', required=True)
    parser.add_argument('-r', dest='rate', help='log lines per second', type=int, default=1000)

    args = parser.parse_args()

    gen = LogLineGenerator()
    gen.set_pattern(args.pattern)

    sock = None
    try:
        sock = get_client_sock(args.host, args.port)
    except ConnectFailedError as e:
        print("{}\n".format(e))
        exit(1)

    tot_lines = 0
    start_time = time()
    try:
        nr_lines = args.rate
        while True:
            start = clock()
            lines = gen.lines( nr_lines )
            for line in lines:
                sock.send(line.encode('utf-8'))
                tot_lines = tot_lines + 1

            dif = clock() - start
            if dif < 1.0:
                sleep(1 - dif)

    except BrokenPipeError:
        sock.close()
        print("Peer closed connection! Exiting!")

    runtime = max(1, int(time() - start_time))
    fin_rate = tot_lines / runtime
    print("Total lines sent: {}, runtime {}s, at {} lines/second.".format(tot_lines, runtime, fin_rate))

if __name__ == "__main__":
    main()
    
