from djondbconnection import *

c = DjondbConnection('localhost', 1243)
c.open()

cur = c.find('ItsmDb', 'ORDERS', '*', '')
while cur.next():
	print(cur.current())

