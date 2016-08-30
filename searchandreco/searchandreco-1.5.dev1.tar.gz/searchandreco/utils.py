__author__ = 'monica'

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):

    mls = MLStripper()

    mls.feed(html)

    stripped_text = mls.get_data()

    return stripped_text