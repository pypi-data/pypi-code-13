#!/usr/bin/env python3

import pexpect

def main(airport_code):
    output = ''
    telnet = pexpect.spawn('telnet rainmaker.wunderground.com',
                           encoding='latin1')
    telnet.expect('Press Return to continue:')
    telnet.sendline('')
    telnet.expect('enter 3 letter forecast city code')
    telnet.sendline(airport_code)
    while telnet.expect(['X to exit:', 'Selection:']) == 0:
        output += telnet.before
        telnet.sendline('')
    output += telnet.before
    telnet.sendline('X')
    telnet.expect(pexpect.EOF)
    telnet.close()
    print(output.strip())


if __name__ == '__main__':
    import sys
    main(airport_code=sys.argv[1])
