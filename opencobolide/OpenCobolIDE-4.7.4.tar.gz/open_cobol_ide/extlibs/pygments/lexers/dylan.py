# -*- coding: utf-8 -*-
"""
    pygments.lexers.dylan
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for the Dylan language.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import Lexer, RegexLexer, bygroups, do_insertions, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Generic, Literal

__all__ = ['DylanLexer', 'DylanConsoleLexer', 'DylanLidLexer']


class DylanLexer(RegexLexer):
    """
    For the `Dylan <http://www.opendylan.org/>`_ language.

    .. versionadded:: 0.7
    """

    name = 'Dylan'
    aliases = ['dylan']
    filenames = ['*.dylan', '*.dyl', '*.intr']
    mimetypes = ['text/x-dylan']

    flags = re.IGNORECASE

    builtins = set((
        'subclass', 'abstract', 'block', 'concrete', 'constant', 'class',
        'compiler-open', 'compiler-sideways', 'domain', 'dynamic',
        'each-subclass', 'exception', 'exclude', 'function', 'generic',
        'handler', 'inherited', 'inline', 'inline-only', 'instance',
        'interface', 'import', 'keyword', 'library', 'macro', 'method',
        'module', 'open', 'primary', 'required', 'sealed', 'sideways',
        'singleton', 'slot', 'thread', 'variable', 'virtual'))

    keywords = set((
        'above', 'afterwards', 'begin', 'below', 'by', 'case', 'cleanup',
        'create', 'define', 'else', 'elseif', 'end', 'export', 'finally',
        'for', 'from', 'if', 'in', 'let', 'local', 'otherwise', 'rename',
        'select', 'signal', 'then', 'to', 'unless', 'until', 'use', 'when',
        'while'))

    operators = set((
        '~', '+', '-', '*', '|', '^', '=', '==', '~=', '~==', '<', '<=',
        '>', '>=', '&', '|'))

    functions = set((
        'abort', 'abs', 'add', 'add!', 'add-method', 'add-new', 'add-new!',
        'all-superclasses', 'always', 'any?', 'applicable-method?', 'apply',
        'aref', 'aref-setter', 'as', 'as-lowercase', 'as-lowercase!',
        'as-uppercase', 'as-uppercase!', 'ash', 'backward-iteration-protocol',
        'break', 'ceiling', 'ceiling/', 'cerror', 'check-type', 'choose',
        'choose-by', 'complement', 'compose', 'concatenate', 'concatenate-as',
        'condition-format-arguments', 'condition-format-string', 'conjoin',
        'copy-sequence', 'curry', 'default-handler', 'dimension', 'dimensions',
        'direct-subclasses', 'direct-superclasses', 'disjoin', 'do',
        'do-handlers', 'element', 'element-setter', 'empty?', 'error', 'even?',
        'every?', 'false-or', 'fill!', 'find-key', 'find-method', 'first',
        'first-setter', 'floor', 'floor/', 'forward-iteration-protocol',
        'function-arguments', 'function-return-values',
        'function-specializers', 'gcd', 'generic-function-mandatory-keywords',
        'generic-function-methods', 'head', 'head-setter', 'identity',
        'initialize', 'instance?', 'integral?', 'intersection',
        'key-sequence', 'key-test', 'last', 'last-setter', 'lcm', 'limited',
        'list', 'logand', 'logbit?', 'logior', 'lognot', 'logxor', 'make',
        'map', 'map-as', 'map-into', 'max', 'member?', 'merge-hash-codes',
        'min', 'modulo', 'negative', 'negative?', 'next-method',
        'object-class', 'object-hash', 'odd?', 'one-of', 'pair', 'pop',
        'pop-last', 'positive?', 'push', 'push-last', 'range', 'rank',
        'rcurry', 'reduce', 'reduce1', 'remainder', 'remove', 'remove!',
        'remove-duplicates', 'remove-duplicates!', 'remove-key!',
        'remove-method', 'replace-elements!', 'replace-subsequence!',
        'restart-query', 'return-allowed?', 'return-description',
        'return-query', 'reverse', 'reverse!', 'round', 'round/',
        'row-major-index', 'second', 'second-setter', 'shallow-copy',
        'signal', 'singleton', 'size', 'size-setter', 'slot-initialized?',
        'sort', 'sort!', 'sorted-applicable-methods', 'subsequence-position',
        'subtype?', 'table-protocol', 'tail', 'tail-setter', 'third',
        'third-setter', 'truncate', 'truncate/', 'type-error-expected-type',
        'type-error-value', 'type-for-copy', 'type-union', 'union', 'values',
        'vector', 'zero?'))

    valid_name = '\\\\?[\\w!&*<>|^$%@\\-+~?/=]+'

    def get_tokens_unprocessed(self, text):
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text):
            if token is Name:
                lowercase_value = value.lower()
                if lowercase_value in self.builtins:
                    yield index, Name.Builtin, value
                    continue
                if lowercase_value in self.keywords:
                    yield index, Keyword, value
                    continue
                if lowercase_value in self.functions:
                    yield index, Name.Builtin, value
                    continue
                if lowercase_value in self.operators:
                    yield index, Operator, value
                    continue
            yield index, token, value

    tokens = {
        'root': [
            # Whitespace
            (r'\s+', Text),

            # single line comment
            (r'//.*?\n', Comment.Single),

            # lid header
            (r'([a-z0-9-]+)(:)([ \t]*)(.*(?:\n[ \t].+)*)',
                bygroups(Name.Attribute, Operator, Text, String)),

            default('code')  # no header match, switch to code
        ],
        'code': [
            # Whitespace
            (r'\s+', Text),

            # single line comment
            (r'//.*?\n', Comment.Single),

            # multi-line comment
            (r'/\*', Comment.Multiline, 'comment'),

            # strings and characters
            (r'"', String, 'string'),
            (r"'(\\.|\\[0-7]{1,3}|\\x[a-f0-9]{1,2}|[^\\\'\n])'", String.Char),

            # binary integer
            (r'#b[01]+', Number.Bin),

            # octal integer
            (r'#o[0-7]+', Number.Oct),

            # floating point
            (r'[-+]?(\d*\.\d+(e[-+]?\d+)?|\d+(\.\d*)?e[-+]?\d+)', Number.Float),

            # decimal integer
            (r'[-+]?\d+', Number.Integer),

            # hex integer
            (r'#x[0-9a-f]+', Number.Hex),

            # Macro parameters
            (r'(\?' + valid_name + ')(:)'
             r'(token|name|variable|expression|body|case-body|\*)',
                bygroups(Name.Tag, Operator, Name.Builtin)),
            (r'(\?)(:)(token|name|variable|expression|body|case-body|\*)',
                bygroups(Name.Tag, Operator, Name.Builtin)),
            (r'\?' + valid_name, Name.Tag),

            # Punctuation
            (r'(=>|::|#\(|#\[|##|\?\?|\?=|\?|[(){}\[\],.;])', Punctuation),

            # Most operators are picked up as names and then re-flagged.
            # This one isn't valid in a name though, so we pick it up now.
            (r':=', Operator),

            # Pick up #t / #f before we match other stuff with #.
            (r'#[tf]', Literal),

            # #"foo" style keywords
            (r'#"', String.Symbol, 'keyword'),

            # #rest, #key, #all-keys, etc.
            (r'#[a-z0-9-]+', Keyword),

            # required-init-keyword: style keywords.
            (valid_name + ':', Keyword),

            # class names
            (r'<' + valid_name + '>', Name.Class),

            # define variable forms.
            (r'\*' + valid_name + '\*', Name.Variable.Global),

            # define constant forms.
            (r'\$' + valid_name, Name.Constant),

            # everything else. We re-flag some of these in the method above.
            (valid_name, Name),
        ],
        'comment': [
            (r'[^*/]', Comment.Multiline),
            (r'/\*', Comment.Multiline, '#push'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[*/]', Comment.Multiline)
        ],
        'keyword': [
            (r'"', String.Symbol, '#pop'),
            (r'[^\\"]+', String.Symbol),  # all other characters
        ],
        'string': [
            (r'"', String, '#pop'),
            (r'\\([\\abfnrtv"\']|x[a-f0-9]{2,4}|[0-7]{1,3})', String.Escape),
            (r'[^\\"\n]+', String),  # all other characters
            (r'\\\n', String),  # line continuation
            (r'\\', String),  # stray backslash
        ]
    }


class DylanLidLexer(RegexLexer):
    """
    For Dylan LID (Library Interchange Definition) files.

    .. versionadded:: 1.6
    """

    name = 'DylanLID'
    aliases = ['dylan-lid', 'lid']
    filenames = ['*.lid', '*.hdp']
    mimetypes = ['text/x-dylan-lid']

    flags = re.IGNORECASE

    tokens = {
        'root': [
            # Whitespace
            (r'\s+', Text),

            # single line comment
            (r'//.*?\n', Comment.Single),

            # lid header
            (r'(.*?)(:)([ \t]*)(.*(?:\n[ \t].+)*)',
             bygroups(Name.Attribute, Operator, Text, String)),
        ]
    }


class DylanConsoleLexer(Lexer):
    """
    For Dylan interactive console output like:

    .. sourcecode:: dylan-console

        ? let a = 1;
        => 1
        ? a
        => 1

    This is based on a copy of the RubyConsoleLexer.

    .. versionadded:: 1.6
    """
    name = 'Dylan session'
    aliases = ['dylan-console', 'dylan-repl']
    filenames = ['*.dylan-console']
    mimetypes = ['text/x-dylan-console']

    _line_re = re.compile('.*?\n')
    _prompt_re = re.compile('\?| ')

    def get_tokens_unprocessed(self, text):
        dylexer = DylanLexer(**self.options)

        curcode = ''
        insertions = []
        for match in self._line_re.finditer(text):
            line = match.group()
            m = self._prompt_re.match(line)
            if m is not None:
                end = m.end()
                insertions.append((len(curcode),
                                   [(0, Generic.Prompt, line[:end])]))
                curcode += line[end:]
            else:
                if curcode:
                    for item in do_insertions(insertions,
                                              dylexer.get_tokens_unprocessed(curcode)):
                        yield item
                    curcode = ''
                    insertions = []
                yield match.start(), Generic.Output, line
        if curcode:
            for item in do_insertions(insertions,
                                      dylexer.get_tokens_unprocessed(curcode)):
                yield item
