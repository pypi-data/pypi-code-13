"""
A simple language-agnostic tokenizer based on Unicode character properties.

Copyright ® 2016, Luís Gomes <luismsgomes@gmail.com>

Simple language-independent tokenizer based on unicode character properties.
Only the following writting systems are supported:
    Latin (western Europe)
    Devanagari and Kannada (languages from India)
    Greek and Coptic
    Cyrillic (eastern Europe)
    Arabic (several languages from Africa and Asia)

As the name indicates, this tokenizer errs on the side of over-tokenization
(separating too much).
"""

import regex

__version__ = "0.1.0"


domain_regex = r"""(?:[a-z0-9\.\-_]+\.)+[a-z]{2,4}"""
user_regex = r"""[a-z0-9\.\-_]+"""
email_regex = r"""(?P<email>(?:mailto:)?{user}@{domain})"""
email_regex = email_regex.format(user=user_regex, domain=domain_regex)
url_regex = r"""(?P<url>(?:(?:ftp|http)s?://)?{domain}(?:/[^"'>\s]*)?)"""
url_regex = url_regex.format(domain=domain_regex)

ident_regex = r"""[a-z0-9]+(?:-[a-z0-9]+)?"""
ident_regex = r"""{ident}(?:\:{ident})?""".format(ident=ident_regex)
attr_regex = r"""{ident}(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^'">]*))?"""
attr_regex = attr_regex.format(ident=ident_regex)
tag_regex = r"""(?P<tag>(?:<{ident}(?:\s+{attr})*/?>|</{ident}>))"""
tag_regex = tag_regex.format(ident=ident_regex, attr=attr_regex)

num_regex = r"(?P<num>\p{N}+)"
word_regex = (
    r"""(?P<word>\p{Script=Hani}|"""  # Chinese
    r"""\p{Script=Latin}+|"""  # European languages (separate hyphenated words)
    r"""\p{Script=Devanagari}+|\p{Script=Kannada}+|"""  # languages from India
    r"""(?:\p{Script=Greek}|\p{Script=Coptic})+|"""
    r"""\p{Script=Cyrillic}+|"""  # Russian
    r"""\p{Script=Arabic}+)"""
)
repeat_regex = \
    r"""(?P<repeat>[\p{P}\p{S}](?:[\p{P}\p{S}\s]*[\p{P}\p{S}])*)\g<repeat>+"""
symb_regex = r"""(?P<symb>\p{S})"""
punct_regex = r"""(?P<punct>\p{P})"""

token_regex = '{email}|{url}|{tag}|{num}|{word}|{repeat}|{symb}|{punct}'
token_regex = token_regex.format(
    email=email_regex,
    url=url_regex,
    tag=tag_regex,
    num=num_regex,
    word=word_regex,
    repeat=repeat_regex,
    symb=symb_regex,
    punct=punct_regex
)


class Overtokenizer:
    """Simple language-agnostic tokenizer

    >>> tokenize = Overtokenizer('en')
    >>> tokenize('Hello World!')
    ['Hello', 'World', '!']
    """

    def __init__(self):
        self.compiled_token_regex = regex.compile(token_regex, regex.U)

    def __call__(self, sentence):
        """Tokenizes a single sentence.

        Newline characters are not allowed in the sentence to be tokenized.
        """
        assert isinstance(sentence, str)
        sentence = sentence.rstrip("\n")
        assert "\n" not in sentence
        tokens = []
        for m in self.compiled_token_regex.finditer(sentence):
            type_ = m.lastgroup
            token = m.group(0)
            if type_ == "repeat":
                token = {
                    "...": "…",  # tranform ... into ellipsis unicode character
                    "--": "–",   # transform -- into en-dash
                    "---": "—",  # transform --- into em-dash
                    }.get(token, m.group("repeat"))
            tokens.append(token)
        return tokens


CMDLINE_USAGE = """
Usage:
    overtokenizer [<inputfile> [<outputfile>]]
    overtokenizer --selftest
    overtokenizer --help

Options:
    --selftest, -t  Run selftests.
    --help, -h      Show this help screen.


2016, Luís Gomes <luismsgomes@gmail.com>
"""


def main():
    from docopt import docopt
    from openfile import openfile
    args = docopt(CMDLINE_USAGE)
    if args["--selftest"]:
        import doctest
        doctest.testmod()
    tokenize = Overtokenizer()
    inputfile = openfile(args["<inputfile>"])
    outputfile = openfile(args["<outputfile>"], "wt")
    with inputfile, outputfile:
        for line in inputfile:
            print(*tokenize(line), file=outputfile)


if __name__ == "__main__":
    main()


__all__ = ["Overtokenizer", "__version__"]
