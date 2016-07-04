# -*- coding: utf-8 -*-
"""
    pygments.styles.lovelace
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lovelace by Miikka Salminen

    Pygments style by Miikka Salminen (https://github.com/miikkas)
    A desaturated, somewhat subdued style created for the Lovelace interactive
    learning environment.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
    Number, Operator, Punctuation, Generic, Whitespace


class LovelaceStyle(Style):
    """
    The style used in Lovelace interactive learning environment. Tries to avoid
    the "angry fruit salad" effect with desaturated and dim colours.
    """
    _KW_BLUE =       '#2838b0'
    _NAME_GREEN =    '#388038'
    _DOC_ORANGE =    '#b85820'
    _OW_PURPLE =     '#a848a8'
    _FUN_BROWN =     '#785840'
    _STR_RED =       '#b83838'
    _CLS_CYAN =      '#287088'
    _ESCAPE_LIME =   '#709030'
    _LABEL_CYAN =    '#289870'
    _EXCEPT_YELLOW = '#908828'

    default_style =  '#222222'

    styles = {
        Whitespace:          '#a89028',
        Comment:             'italic #888888',
        Comment.Hashbang:    _CLS_CYAN,
        Comment.Multiline:   '#888888',
        Comment.Preproc:     'noitalic '+_LABEL_CYAN,

        Keyword:             _KW_BLUE,
        Keyword.Constant:    'italic #444444',
        Keyword.Declaration: 'italic',
        Keyword.Type:        'italic',

        Operator:            '#666666',
        Operator.Word:       _OW_PURPLE,

        Punctuation:         '#888888',

        Name.Attribute:      _NAME_GREEN,
        Name.Builtin:        _NAME_GREEN,
        Name.Builtin.Pseudo: 'italic',
        Name.Class:          _CLS_CYAN,
        Name.Constant:       _DOC_ORANGE,
        Name.Decorator:      _CLS_CYAN,
        Name.Entity:         _ESCAPE_LIME,
        Name.Exception:      _EXCEPT_YELLOW,
        Name.Function:       _FUN_BROWN,
        Name.Label:          _LABEL_CYAN,
        Name.Namespace:      _LABEL_CYAN,
        Name.Tag:            _KW_BLUE,
        Name.Variable:       '#b04040',
        Name.Variable.Global:_EXCEPT_YELLOW,

        String:              _STR_RED,
        String.Char:         _OW_PURPLE,
        String.Doc:          'italic '+_DOC_ORANGE,
        String.Escape:       _ESCAPE_LIME,
        String.Interpol:     'underline',
        String.Other:        _OW_PURPLE,
        String.Regex:        _OW_PURPLE,

        Number:              '#444444',

        Generic.Deleted:     '#c02828',
        Generic.Emph:        'italic',
        Generic.Error:       '#c02828',
        Generic.Heading:     '#666666',
        Generic.Subheading:  '#444444',
        Generic.Inserted:    _NAME_GREEN,
        Generic.Output:      '#666666',
        Generic.Prompt:      '#444444',
        Generic.Strong:      'bold',
        Generic.Traceback:   _KW_BLUE,

        Error:               'bg:'+_OW_PURPLE,
    }
