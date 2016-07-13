#! /usr/bin/env python3
"""SMTP proxy used to produce individual messages for each BCC: specified address
(c)2016 Vidmantas Balčytis <vidma@lema.lt>

Usage: %(program)s [options] [localhost[:localport] [remotehost[:remoteport]]]

Options:

    --version
    -V
        Print the version number and exit.

    --bcc2to
    -b
        Specify address to receive bcc expanded messages

    --size limit
    -s limit
        Restrict the total size of the incoming message to "limit" number of
        bytes via the RFC 1870 SIZE extension.  Defaults to 33554432 bytes.

    --debug level
    -d level
        0 - debugging off
        ...
        9 - pass debug flag to upper library

    --help
    -h
        Print this message and exit.

Version: %(__version__)s

If localhost is not not given 'localhost' is used.
If localport is not given, %(deflport)i is used.
If remotehost is not given 'localhost' is used.
If remoteport is not given, localport+1 is used.
"""

import  sys
import  os
import  getopt
import  logging
import  asyncore
import  re
import  email.utils


# <vidma@lema.lt>: this is excerpt from Mailman 3
# But realy smtplib is also broken - and in 3.5 as well.
# So we will not check for version, but always use "modified" one
# in smtpd - only one line (import is from modified smtplib) is changed
#
# In smtplib - we have replased encoding type from 'ascii' to 'utf8':
# Reson is simple - we are simply "proxying" - so failure to encode to 'ascii'
# is caused by decoder to utf on receive.
# On the other hand - if it's pure ASCII - both codecs do the same

# Python 3.4's smtpd module can't handle non-UTF-8 byte input.  Unfortunately
# we do get such emails in the wild.  Python 3.5's version of the module does
# handle it correctly.  We vendor a version to use in the Python 3.4 case.
#if sys.version_info < (3, 5):
#    from bcc2to.parts import smtpd
#else:
#    import smtpd

from bcc2to.parts import smtpd


__all__ = ["Bcc2To"]

program = sys.argv[0]
__version__ = '0.4.0rc1'
deflport = 10033

DEBUGSTREAM = smtpd.Devnull()
MAX_HEAD_LINE = 254
log = logging.getLogger("bcc2to.log")


class Bcc2To(smtpd.PureProxy):
    NEWLINE = b'\n'
    CHNEWLINE = 10
    EMPTY = b''
    CRLF = b"\r\n"
    
    def __init__(self, *args, **kwargs):
        super(Bcc2To, self).__init__(*args, **kwargs)
        if self._decode_data:
            self.NEWLINE = CHNEWLINE = '\n'
            self.EMPTY = ''
            sefl.CRLF = "\r\n"
            self.reTo = re.compile("to:",re.I)
            self.reCc = re.compile("cc:",re.I)
        else:
            self.reTo = re.compile(b"to:",re.I)
            self.reCc = re.compile(b"cc:",re.I)

    def retraddr(self, lines, b, e):
        """ Retrieve addresses from "To:" or "CC:" blocks
                lines - array af lines (str type if self._decode_data else bytes type)
                b - beginning line
                e - end line
            Returns: se, ad
                se - set of address
                ad - list of pairs (Full Name, address) in order, they where found in fields
        """
        if b is None:
            return set(), None
        if self._decode.data:
            ent = ''.join(lines[b:e])
        else:
            enb = b''.join(lines[b.e])
            try:
                ent = enb.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    ent = enb.decode('ascii')
                except UnicodeDecodeError:
                    log.exeption("Bcc2To.retraddr: ignoring undecodable letters")
                    ent = enb.decode('ascii', 'ignore')
        ad = [email.utils.parseaddr(t) for t in ent.split(',')]
        se = set({a[1] for a in ad})
        return se, ad

    def dec_line(l):
        try:
            r = l.decode('utf-8')
        except UnicodeDecodeError:
            try:
                r = l.decode('ascii')
            except UnicodeDecodeError:
                log.exeption("Bcc2To.dec_line: ignoring undecodable letters")
                r = l.decode('ascii', 'ignore')
        return r

    def mkheader(self, typ, memb, fmemb = None):
        """ mkheader(typ, memb, fmemb)
            typ - string containing header type
            memb - set of members
            fmemb - list of pairs ("full mane", "addr")
        """
        if len(memb) == 0:
            return []
        if fmemb is None:
            hd = [' ' + m + ',' for m in memb]
        else:
            hd = []
            for p in fmemb:
                if p[1] in memb:
                    if p[0] != '':
                        hd.append(' ' + p[0] + ' <' + p[1] + '>,')
                    else:
                        hd.append(' ' + p[1] + ',')
        hd[-1] = hd[-1].rstrip(',')
        hd[0] = typ + ':' + hd[0]
        s = 0
        while len(hd) - s > 1:
            l = hd[s] + hd[s + 1]
            if len(l) < MAX_HEAD_LINE:
                hd[s:s+2] = [l]
            else:
                s += 1
        if self._decode.data:
            return hd
        return [dec_line(l) for l in hd]


    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        if options.debug >= 1:
            print("===> Bcc2To receive: mailfrom '%s' rcptto '%s'" % (mailfrom, rcpttos), file=DEBUGSTREAM)
            if kwargs:
                print("  kwargs: %s", kwargs, file=DEBUGSTREAM)
        if options.debug >= 4: print(repr(data if isinstance(data, str) else str(data, 'utf-8', 'ignore')), file=DEBUGSTREAM)
        rcpt = set(rcpttos)
        havelist = haveinh = False
        if options.bcc2to in rcpt:
            rcpt.remove(options.bcc2to)
            havelist = True
        if options.alowedre.match(mailfrom):
            log.info("Processing message from <%s> to %s", mailfrom, rcpttos)
            lines = data.splitlines()
            if data[-1] == self.CHNEWLINE:
                lines += [self.EMPTY]
            # Inspect headers
            i = 0
            toBeg = toEnd = ccBeg = ccEnd = None
            for line in lines:
                if not line:
                    if toBeg is not None and toEnd is None:
                        toEnd = i
                    if ccBeg is not None and ccEnd is None:
                        ccEnd = i
                    break
                if toBeg is None:
                    if self.reTo.match(line):
                        toBeg = i
                elif toEnd is None and line[0] != ' ':
                    toEnd = i
                if ccBeg is None:
                    if self.reCc.match(line):
                        ccBeg = i
                elif ccEnd is None and line[0] != ' ':
                    ccEnd = i
                i += 1
            to, fto = self.retraddr(lines, toBeg, toEnd)
            cc, fcc = self.retraddr(lines, ccBeg, ccEnd)
            if options.bcc2to in to:
                to.remove(options.bcc2to)
                havelist = haveinh =True;
            if options.bcc2to in cc:
                cc.remove(ptions.bcc2to)
                havelist = haveinh = True;
            bcc = rcpt.difference(to, cc)
            if havelist and (len(bcc) != 0 or haveinh):
            # Remove lines from header
                if toBeg is None:
                    if ccBeg is not None:
                        i = ccBeg
                        lines[ccBeg:ccEnd] = []
                else:       # to is present
                    if ccBeg is None:
                        i = toBeg
                        lines[toBeg:toEnd] = []
                    else:   # both fields are present
                        if toBeg < ccBeg:
                            i = toBeg
                            lines[ccBeg:ccEnd] = []
                            lines[toBeg:toEnd] = []
                        else:
                            i = ccBeg
                            lines[toBeg:toEnd] = []
                            lines[ccBeg:ccEnd] = []
# To: and CC: headers removed. i = point to insert new headers
                for a in bcc:
                    hd = self.mkheader("To", [a])
                    l = len(hd)
                    lines[i:i] = hd
                    data = self.CRLF.join(lines)
                    self._deliver(mailfrom, list([a]), data, True)
                    lines[i:i+l] = []
                lines[i:i] = self.mkheader("To", list(to), fto) + self.mkheader("Cc", list(cc), fcc)
                data = self.CRLF.join(lines)
                rcpt = rcpt.difference(bcc)
        if len(rcpt):
            refused = self._deliver(mailfrom, list(rcpt), data, havelist | haveinh)
            if len(refused) != 0:
                log.warning("Refused delivery to %s", refused)
                if options.debug >= 1:
                    print('We got some refusals:', refused, file=DEBUGSTREAM)

    def _deliver(self, mailfrom, rcpttos, data, dolog):
        if dolog:
            log.info("Delivering message from <%s> to %s", mailfrom, rcpttos)
        if options.debug >= 1: print("===> Bcc2To deliver: mailfrom '%s' rcptto '%s'" % (mailfrom, rcpttos), file=DEBUGSTREAM)
        if options.debug >= 4: print(data if isinstance(data, str) else str(data, 'utf-8', 'ignore'), file=DEBUGSTREAM)
        return super()._deliver(mailfrom, rcpttos, data)


attrs = {"localhost":0, "localport":1, "remotehost":0, "remoteport":1, "bcc2to":0, "alowedre":2, "size_limit":1}
class Options:
    size_limit = None
    localhost = None
    localport = None
    remotehost = None
    remoteport = None
    bcc2to = None
    alowedre = None
    debug = 0

options = Options()

def logparams():
    """ Log all parameters we are starting job with
    """
    global options
    pn = [n for n in attrs]
    pn.sort()
    p = [getattr(options, a) for a in pn]
    for i in range(0,len(p)):
        if hasattr(p[i], 'pattern'):
            p[i] = getattr(p[i], 'pattern')
        if type(p[i]) is str:
            p[i] = "'" + p[i] + "'"
    pn += ['']
    l = "Sartup parameters: " + "=%s ".join(pn)
    log.info(l.rstrip(), *p)

def getdefault():
    """ Retrieve options from file /etc/default/bcc2to
    """
    global options
    w = re.compile("[ \t]*")
    df = "/etc/default/bcc2to"
    lin = 0
    try:
        with open(df) as f:
            while True:
                l = f.readline()
                lin += 1
                if not l:
                    break
                if l[0] in list(" \t#\n"):
                    continue
                v = w.split(l.strip(), maxsplit=1)
                if len(v) != 2:
                    log.warning("Invalid setting in '%s' at line %i: '%s'", df, lin, repr(l))
                    continue
                if v[0] in attrs:
                    try:
                        if attrs[v[0]] == 1:        # integer
                            val = int(v[1])
                        elif attrs[v[0]] == 2:      # re
                            val = re.compile(v[1])
                        else:
                            val = v[1]
                        setattr(options, v[0], val)
                    except:
                        log.warning("Invalid setting in '%s' at line %i: type error", df, lin)
                else:
                    log.warning("Invalid setting in '%s' at line %i: keyword unknown", df, lin)
    except:
        log.warning("Cannon find defaults file '%s'", df)



def usage(code, msg=''):
    print(__doc__ % globals(), file=sys.stderr)
    if msg:
        print(msg, file=sys.stderr)
    sys.exit(code)

def parseargs():
    global options, DEBUGSTREAM

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], 'Vhs:d:b:a:',
            ['version', 'help', 'size=', 'debug=', 'bcc2to=', 'allowed='])
    except getopt.error as e:
        usage(1, e)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage(0)
        elif opt in ('-V', '--version'):
            print(__version__)
            sys.exit(0)
        elif opt in ('-d', '--debug'):
            try:
                d = int(arg)
                options.debug = d
                if d < 0 or d > 9:
                    raise Exception
            except:
                usage(1, 'Invalid debug level: %s' % arg)
        elif opt in ('-b', '--bcc2to'):
            options.bcc2to = arg.lower()
        elif opt in ('-a', '--allowed'):
            try:
                options.alowedre = re.compile(arg)
            except:
                usage(1, 'Invalid regular expression in %s' % opt)
        elif opt in ('-s', '--size'):
            try:
                int_size = int(arg)
                options.size_limit = int_size
            except:
                usage(1, 'Invalid size: %s' % arg)

    # parse the rest of the arguments
    try:
        if len(args) >= 1:
            if ':' in args[0]:
                options.localhost, options.localport = args[0].split(':')
            else:
                options.localhost = args[0]
            options.localport = int(options.localport)
        if len(args) >= 2:
            if ':' in args[1]:
                options.remotehost, options.remoteport = args[1].split(':')
            else:
                options.remotehost = args[1]
            options.remoteport = int(options.remoteport)
        if len(args) >= 3:
            raise Exception
    except:
        usage(1, 'Invalid arguments: %s' % COMMASPACE.join(args))

    if options.localhost is None:
        options.localhost = 'localhost'
    if options.localport is None:
        options.localport = deflport
    if options.remotehost is None:
        options.remotehost = 'localhost'
    if options.remoteport is None:
        options.remoteport = options.localport + 1


def main():
    global options
    getdefault()
    parseargs()
    if options.debug > 0:
        DEBUGSTREAM = sys.stderr
    if options.debug >= 9:
        smtpd.DEBUGSTREAM = DEBUGSTREAM

    if options.bcc2to is None:
        usage(1, '-b option is mandatory')
    if options.alowedre is None:
        usage(1, '-a option is mandatory')
    logparams()

    Bcc2To((options.localhost, options.localport),
                   (options.remotehost, options.remoteport),
                   options.size_limit, decode_data = False)
    asyncore.loop()

