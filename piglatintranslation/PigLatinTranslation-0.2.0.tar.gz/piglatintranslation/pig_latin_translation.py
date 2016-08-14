"""
.. module:: pig_latin_translation
   :synopsis: translate english text to pig latin.

.. moduleauthor:: Jai Chaudhary <jai.chaudhary.iitd@gmail.com>

"""

import re
import string

VOWELS = ('a', 'e', 'i', 'o', 'u')
VOWEL_SND_SUFFIX = "yay"
CONSONANT_SND_SUFFIX = "ay"

def translate_text(input_text):
  text_translation = []

  for match in re.finditer("(?P<not_word>\W+)|(?P<word>[\w']+)", input_text):
    if match.group("word") == None:
      text_translation.append(match.group("not_word"))
    else:
      translated_word = translate_word(match.group("word"))
      translated_word = proper_case(match.group("word"), translated_word)
      text_translation.append(translated_word)
  return "".join(text_translation)

def translate_word(word):
  assert(len(word) > 0)

  word = word.lower()

  if word[0] in VOWELS or is_first_letter_silent(word):
    return word + VOWEL_SND_SUFFIX
  else:
    for idx, char in enumerate(word):
      if char in VOWELS:
        return word[idx:] + word[:idx] + CONSONANT_SND_SUFFIX
    return word + CONSONANT_SND_SUFFIX

def proper_case(word, translated_word):
  if word[0] in string.ascii_uppercase:
    return string.upper(translated_word[0]) + translated_word[1:]

  return translated_word

def is_first_letter_silent(word):
  top_freq_silent_prefixes_cmu_dict = ( "pf", "ph", "ps", "pn", "pt", "wr", "ts", "gn", "kn", "jo", "he")

  if word[:2] in top_freq_silent_prefixes_cmu_dict:
    return True;
  return False;