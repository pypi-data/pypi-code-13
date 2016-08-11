from word_creator import Word
from re import sub

class WordRenderer:

	@staticmethod
	def create_word(word):
		word_list = Word(word).get_word()
		result = ""
		for row in word_list:
			for item in row:
				result = "".join((result, str(item)))
			result = "\n".join((result, ""))
		return result

	def create_rendered_word(self, word, positive="1", negative="0"):
		result = self.create_word(word)
		result = sub(r"1", positive, result)
		result = sub(r"0", negative, result)
		return result

if __name__ == '__main__':
	renderer = WordRenderer()
	print renderer.create_word('HEY EVERYBODY')
	print renderer.create_rendered_word('HELLO FRIEND', "X", " ")
	print renderer.create_rendered_word('HEY EVERYBODY', "O", " ")
	print renderer.create_rendered_word('A B C D E F G', "O", " ")
	print renderer.create_rendered_word('H I J K L M N', "O", " ")
	print renderer.create_rendered_word('O P Q R S T U', "O", " ")
	print renderer.create_rendered_word('V W X Y Z', "O", " ")
	print renderer.create_rendered_word('da da da', "O", " ")
	print renderer.create_rendered_word('DANCE', ':boredparrot:', ':shuffleparrot:')