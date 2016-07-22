import random
def random_integer(min, max):
	return random.randrange(min, max + 1)
def random_letter_uppercase():
	rand = random_integer(1, 26)
	dec = ord('A')
	decl = dec - 1
	return chr(decl + rand)
def random_letter_lowercase():
	rand = random_integer(1, 26)
	dec = ord('a')
	decl = dec - 1
	return chr(decl + rand)
