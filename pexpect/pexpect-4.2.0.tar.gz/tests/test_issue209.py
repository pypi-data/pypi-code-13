import asyncio
import sys
import pexpect

@asyncio.coroutine
def eof_coro():
    aout = pexpect.spawn('./tests/a.out')

    yield from aout.expect_exact('\r', async=True)
    yield from aout.expect_exact('\r', async=True)

#        except pexpect.EOF as e:
#            print("2. output: {:s}".format(repr(p.before)))
#            return
#        else:
#            print("1. output: {:s}".format(repr(p.before + p.after)))



def test_209():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(eof_coro())
    loop.close()
