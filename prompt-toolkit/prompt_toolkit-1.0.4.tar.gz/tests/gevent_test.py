from gevent.monkey import patch_all
import os
import threading
import select
import time
import sys

r,w = os.pipe()


def wait():
#    time.sleep(4)
    select.select([sys.stdin.fileno()], [], [])
    os.write(w, b'x')
    pass


threading.Thread(target=wait).start()

ready = select.select([r], [], [])
print('ready')

