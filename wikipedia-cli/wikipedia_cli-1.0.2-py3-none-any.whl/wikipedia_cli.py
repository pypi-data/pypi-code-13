#!/usr/bin/env python
"""
A quick-and-dirty CLI for fetching summaries of Wikipedia pages.

The real work is donw by the wikipedia module:
https://github.com/goldsmith/Wikipedia
"""

from optparse import OptionParser
import textwrap
import warnings
import webbrowser

import wikipedia

from prompt_toolkit.token import Token
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.shortcuts import confirm, print_tokens

# wikipedia.BeautifulSoup sometimes throughs a UserWarning:
warnings.filterwarnings(action='ignore', category=UserWarning)

parser = OptionParser(usage="usage: %prog [-l, --lang] query",
                      version="%prog 1.0")

parser.add_option('-l', '--lang',
                  action='store',
                  dest='language',
                  default='en',
                  help='Choose language (default: en)')


color_style = style_from_dict({
    Token.Title: '#ff0066 bold',
    Token.URL: '#00ff66 bold',
    })


def main():
    (options, args) = parser.parse_args()
    if not args:
        parser.error('Must have at least one query word')
        return None
    query = ' '.join(args)
    lang = options.language
    if lang not in wikipedia.languages():
        print('Language {} is not supported'.format(lang))
        return None
    wikipedia.set_lang(lang)
    try:
        page = wikipedia.page(query, auto_suggest=True)
    except wikipedia.exceptions.DisambiguationError as e:
        print()
        print(e)
    except wikipedia.exceptions.PageError as e:
        print()
        print(e)
    else:
        print()
        print_tokens([(Token.Title, page.title)], style=color_style)
        print('\n')
        print(textwrap.fill(page.summary))
        print()
        print_tokens([(Token.URL, page.url)], style=color_style)
        print('\n')

        ans = confirm('Open URL (y/n)? ')
        if ans:
            webbrowser.open_new_tab(page.url)


if __name__ == '__main__':
    main()
