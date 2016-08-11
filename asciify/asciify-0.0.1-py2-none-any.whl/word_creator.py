from letter_profiles import Letter

SPACE_CHARACTER = Letter(' ')()

class Word:

	word_prime = {'word': []}

	def __init__(self, word_string):
		self.word_prime['word'] = [list(bit) for bit in SPACE_CHARACTER]
		for char in word_string:
			char = Letter(char)
			char_list = char()
			for idx, row in enumerate(char_list):
				self.word_prime.get('word')[idx].extend(row)
			for idx, row in enumerate(SPACE_CHARACTER):
				self.word_prime.get('word')[idx].extend(row)

	def get_word(self):
		return self.word_prime.get('word')

if __name__ == '__main__':
	w = Word('HELLO')
	print w.get_word()