# -*- coding: utf-8 -*-
from collections import Counter
import re
import string

from wordcloud import WordCloud


def clean_text(text):
    rm_punctuation_map = dict((ord(char), u' ') for char in string.punctuation)
    text = text.decode('utf-8').translate(rm_punctuation_map).lower()
    return re.sub(r'\s+', ' ', text)


def generate_wordcloud(text):
    frequencies = Counter(text.split(' '))
    return WordCloud(
        relative_scaling=.5, width=600, height=500, background_color='black',
        max_words=1000).generate_from_frequencies(frequencies.items())
