from djondbconnection import *

host = "localhost"
port = 1243

# buffer = network.int_toendian(10)
# print(repr(buffer))
# val = network.int_fromendian(buffer, 0)
# print(val)

con = DjondbConnection(host, port)
con.open()

