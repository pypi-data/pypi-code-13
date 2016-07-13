#! /usr/bin/env python3
"""It is a part fron bcc2to package
(c)2016 Vidmantas Balčytis <vidma@lema.lt>
"""

import  sys
import  logging
import  signal
from time import sleep

class SigExcept(Exception):
    def __init__(self, value):
        self.quit = value


def sig_handle(signum, frame):
    if signum == signal.SIGHUP:
        raise SigExcept(False)
    elif signum == signal.SIGTERM:
        raise SigExcept(True)

def worker():
    from bcc2to.parts import proxy
    proxy.main()

#**** Executable entry: run with command `python3 -m bcc2to <parameters>` ****
def main():
    signal.signal(signal.SIGTERM, sig_handle)
    signal.signal(signal.SIGHUP, sig_handle)
    log = logging.getLogger("bcc2to.log")
    log.setLevel(logging.DEBUG)
    try:
        fh = logging.FileHandler("/var/log/bcc2to.log")
    except:
        fh = logging.FileHandler("/tmp/bcc2to.log")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s\t%(levelname)s:\t%(message)s")
    fh.setFormatter(formatter)
    log.addHandler(fh)
    log.info("Starting with args %s", sys.argv[1:])
    sl = 0
    while True:
        try:
            if sl != 0:
                sleep(sl)
                sl = 0
            worker()
        except KeyboardInterrupt:
            log.info("Exiting on KeyboardInterrupt")
            break
        except SigExcept as e:
            if e.quit:
                log.info("Exiting on SIGTERM")
                break
            log.info("SIGHUP received: restarting")
        except Exception as e:
            log.exception("Exeption caught", exc_info=True)
            log.info("Restarting in 2 seconds")
            sl = 2

