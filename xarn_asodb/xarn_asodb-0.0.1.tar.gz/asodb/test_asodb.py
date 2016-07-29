import random
import time
import sys
import query

from timeit import timeit
from collections import namedtuple
#from cnamedtuple import namedtuple

start = time.time()

def do(cmd, data=None, repeat=1):
	print('%dx %s' % (repeat, cmd))
	start = time.time()
	while repeat > 0:
		res = query.executePlain(cmd, data)
		repeat -= 1
	end = time.time()
	print('Took %.3f seconds' % (end-start))
	print(res[:200])
	print('-----------------------------------')

print(sys.version)
print('-----------------------------------')

cards = open('../test_data/mtg_cards.json', encoding='utf-8').read()
#do('GET	/')
do('SET	/cards', cards)
#do('GET	/')
do('GET	cards/Black Lotus', repeat=1000)
do('GET	cards/Black Lotus/name')
do('GET	cards/Black Lotus/types')
do('ADD	cards/Black Lotus/types', '"Cool Card!"')
do('GET	cards/Black Lotus/types')
do('GET	cards/Black Lotus/types/1')
do('FIND	cards/*/name')
do('FIND	cards/Black Lotus/types/*', repeat=1000)
do('FIND	cards/*/types/*')
do('COUNT	cards/*/*')

do('COUNT	cards/*')
do('SET	cards/*/types/0', '"Cool Card!"')
do('GET	cards/Black Lotus/types')

do('DELETE	cards/*/types/*	where=@value=="Cool Card!"')



print('Total elapsed time: %.3f seconds' % (time.time() - start))