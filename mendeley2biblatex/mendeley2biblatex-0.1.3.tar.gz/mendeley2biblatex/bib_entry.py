class BibEntry:
    TEMPLATES = {
        'JournalArticle': '''
@article{{{entry[citationKey]},
    author    = "{entry[authors]}",
    title     = "{entry[title]}",
    journal   = "{entry[publication]}",
    number    = "{entry[issue]}",
    volume    = "{entry[volume]}",
    pages     = "{entry[pages]}",
    year      = "{entry[year]}",
    doi       = "{entry[doi]}",
}}''',
        'ConferenceProceedings': '''
@proceedings{{{entry[citationKey]},
    author    = "{entry[authors]}",
    title     = "{entry[title]}",
    publisher = "{entry[publisher]}",
    pages     = "{entry[pages]}",
    year      = "{entry[year]}",
    doi       = "{entry[doi]}",
}}''',
        'WebPage': '''
@online{{{entry[citationKey]},
    author    = "{entry[authors]}",
    title     = "{entry[title]}",
    year      = "{entry[year]}",
    url       = "{entry[url]}",
    urldate   = "{entry[urldate]}"
}}''',
        'Book': '''
@book{{{entry[citationKey]},
    author    = "{entry[authors]}",
    title     = "{entry[title]}",
    publisher = "{entry[publisher]}",
    year      = "{entry[year]}",
    pages     = "{entry[pages]}",
    volume    = "{entry[volume]}",
    doi       = "{entry[doi]}",
}}''',
        'BookSection': '''
@inbook{{{entry[citationKey]},
    author    = "{entry[authors]}",
    title     = "{entry[title]}",
    booktitle = "{entry[publication]}"
    publisher = "{entry[publisher]}",
    year      = "{entry[year]}",
    volume    = "{entry[volume]}",
    pages     = "{entry[pages]}",
    doi       = "{entry[doi]}",
    url       = "{entry[url]}",
    urldate   = "{entry[urldate]}"
}}''',
        'Patent': '''
@thesis{{{entry[citationKey]},
    author    = "{entry[authors]}",
    title     = "{entry[title]}",
    number    = "{entry[number]}",
    year      = "{entry[year]}",
    type      = "{entry[sourceType]}",
    doi       = "{entry[doi]}",
    url       = "{entry[url]}",
    urldate   = "{entry[urldate]}"
}}''',
        'Report': '''
@inbook{{{entry[citationKey]},
    author    = "{entry[authors]}",
    title     = "{entry[title]}",
    type = "{entry[publication]}"
    institution = "{entry[institution]}",
    year      = "{entry[year]}",
    type      = "{entry[sourceType]}",
    doi       = "{entry[doi]}",
    pages     = "{entry[pages]}",
    url       = "{entry[url]}",
    urldate   = "{entry[urldate]}"
}}''',
        'Thesis': '''
@thesis{{{entry[citationKey]},
    author    = "{entry[authors]}",
    title     = "{entry[title]}",
    institution = "{entry[institution]}",
    year      = "{entry[year]}",
    type      = "{entry[sourceType]}",
    doi       = "{entry[doi]}",
    pages     = "{entry[pages]}",
    url       = "{entry[url]}",
    urldate   = "{entry[urldate]}"
}}'''
    }

    @staticmethod
    def clean_characters(entry):
        """A helper function to convert special characters to LaTeX characters"""

        # List of char and replacement, add your own list below
        char_to_replace = {
            # LaTeX special char
            '&': '\&',
            # UTF8 not understood by inputenc
            '–': '--',  # utf8 2014, special dash
            '—': '--',  # utf8 2013, special dash
            '∕': '/',  # utf8 2215, math division
            'κ': 'k',  # Greek kappa
            '×': 'x',  # times
        }

        # Which field shall we check and convert
        entry_key = ['publisher', 'publication', 'title']

        for k in entry_key:
            for char, repl_char in char_to_replace.items():
                entry[k] = entry[k].replace(char, repl_char)
