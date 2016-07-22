'''
Popcorn 1.3.1
https://github.com/InitializeSahib/Popcorn
'''
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
def random_sentence():
	dialogue = ["Does this seem normal to you?", "Please! I'm fading! And all I want is to know that I'm going to be okay!", "Relaaaaaax. It's not like we're gonna get caught.", "...Bond. James Bond.", "Of all the gin jos in all the towns in all the world, she walks o mine.", "Well, it's not the men in your life that counts, it's the life in your men.", "I'll be back.", "Would you be shocked if I put on something more comfortable?", "My Mama always said, 'Life was like a box of chocolates you never know what you're gonna get.'", "I could dance with you till the cows come home...On second thought, I'd rather dance with the cows when you came home."] 
	past_verbs = ["was", "had", "ate", "said", "went", "got", "made", "knew", "thought", "took", "saw", "came", "wanted", "used", "found"]
	articles = ["the", "a", "our", "their", "his", "her"]
	uppercase_articles = ["The", "A", "Our", "Their", "His", "Her"]
	names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Micheal", "Elizabeth", "William", "Linda", "David", "Barbara", "Richard", "Susan"]
	nouns = ["dog", "cat", "man", "woman", "human", "baby", "kid", "goat", "sheep", "cow", "teacher", "student", "professor", "wife", "husband"]
	adjectives = ["good", "new", "first", "last", "long", "great", "little", "own", "other", "old", "right", "big", "high", "different", "small"]
	dialogue_ind = random_integer(0, 9)
	past_verbs_ind = random_integer(0, 14)
	articles_ind = random_integer(0, 5)
	uppercase_articles_ind = random_integer(0, 5)
	names_ind = random_integer(0, 13)
	nouns_ind = random_integer(0, 14)
	nouns_ind_two = random_integer(0, 14)
	adjectives_ind = random_integer(0, 14)
	verb = past_verbs[past_verbs_ind]
	if verb is "went":
		verb = "went to"
	article = articles[articles_ind]
	uppercase_article = uppercase_articles[uppercase_articles_ind]
	lowercase_article = uppercase_article.lower()
	if lowercase_article is article:
		while True:
			articles_ind = random_integer(0, 5)
			article = articles[articles_ind]
			if article is not lowercase_article:
				break
	name = names[names_ind]
	noun = nouns[nouns_ind]
	noun_two = nouns[nouns_ind_two]
	if noun_two is noun:
		while True:
			nouns_ind = random_integer(0, 14)
			noun = nouns[nouns_ind]
			if noun is not noun_two:
				break
	adjective = adjectives[adjectives_ind]
	format = random_integer(0, 2)
	if format is 0:
		if verb is not "said":
			sentence = uppercase_article
			sentence += " "
			sentence += adjective
			sentence += " "
			sentence += noun
			sentence += " "
			sentence += verb
			sentence += " "
			sentence += article
			sentence += " "
			sentence += noun_two
			sentence += "."
			return sentence
		else:
			sentence = uppercase_article
			sentence += " "
			sentence += adjective
			sentence += " "
			sentence += noun
			sentence += " "
			sentence += "said, "
			sentence += "\""
			sentence += dialogue[dialogue_ind]
			sentence += "\""
			return sentence
	elif format is 1:
		if verb is said:
			sentence = name
			sentence += " "
			sentence += "said, "
			sentence += "\""
			sentence += dialogue[dialogue_ind]
			sentence += "\""
			return sentence
		else:
			sentence = name
			sentence += " "
			sentence += verb
			sentence += " "
			sentence += article
			sentence += " "
			sentence += noun_two
			sentence += "."
			return sentence
	elif format is 2:
		if verb is not said:
			sentence = name
			sentence += "'s"
			sentence += " "
			sentence += adjective
			sentence += " "
			sentence += noun
			sentence += " "
			sentence += verb
			sentence += " "
			sentence += article
			sentence += " "
			sentence += noun_two
			sentence += "."
			return sentence
		else:
			sentence = name
			sentence += "'s"
			sentence += " "
			sentence += adjective
			sentence += " "
			sentence += noun
			sentence += " "
			sentence += "said, "
			sentence += "\""
			sentence += dialogue[dialogue_ind]
			sentence += "\""
			return sentence
			
			
