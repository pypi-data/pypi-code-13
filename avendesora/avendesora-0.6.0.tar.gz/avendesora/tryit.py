
from charsets import LOWERCASE, UPPERCASE, DIGITS, PUNCTUATION, ALPHANUMERIC
import re

ALPHABETS = {
    'l': LOWERCASE,
    'u': UPPERCASE,
    'd': DIGITS,
    's': PUNCTUATION,
    'S': None,
}

pattern = re.compile(r'(\d*)([%s])(.*)' % ''.join(ALPHABETS.keys()))


def parse(recipe):
    parts = recipe.split()
    requirements = []
    try:
        each = parts[0]
        length = int(each)
        print(length)
        print(ALPHANUMERIC)
        for each in parts[1:]:
            num, kind, alphabet = pattern.match(each).groups()
            alphabet = ALPHABETS[kind] if ALPHABETS[kind] else alphabet
            print(num, kind, alphabet)
        print()
    except (ValueError, AttributeError) as err:
        print('Invalid term in recipe: %s.' % each)

parse('12 2u 2d 2s')
parse('12 2u 2d 2S!@#$%^&*')
parse('12 u d l s')
parse('xx u d l s')
parse('12 x d l s')

