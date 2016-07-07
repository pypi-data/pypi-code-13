
def is_abecedarian(word):
	"""
		check if given word is alphabetically arranged
	"""
	prev = word[0]
	for char in word:
		if char < prev:
			return False
		prev = char

	return True

#other implementations
# 1. use index based for loop - check for each index char


if __name__=='__main__':
	word = raw_input("Enter word to be checked for abecedarian : ")
	print is_abecedarian(word)