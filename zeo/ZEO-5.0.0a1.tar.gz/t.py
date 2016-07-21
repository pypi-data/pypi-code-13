import socket, struct
import sys

import ZEO.tests.testssl

sys.stdin.close()

addr, stop = ZEO.server(zeo_conf=ZEO.tests.testssl.server_config)

for i in range(55):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,
                 struct.pack('ii', 1, 0))
    s.connect(addr)
    s.close()

c = ZEO.DB(addr, ssl=ZEO.tests.testssl.client_ssl())

print("CONNECTED", c.storage.is_connected())

c.close()
stop()
