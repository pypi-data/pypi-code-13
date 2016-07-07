
def has_no_e(word,substring):
	"""
		check if given word has that substring
		e is the most common char ~ 67 percent frequency
 	"""
	#for char in word:
	#	if char==letter:
	#		return False
	#return True
 	bool = substring in word
	return not bool		#allows flexibility for substring



if __name__=='__main__':

	word = raw_input("Enter word :")
	substring = raw_input("Enter substring to check if not present : ")
	print substring,' in ',word,':',has_no_e(word,substring)