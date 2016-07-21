import pytest
from shutil import get_terminal_size

from dots.tui import Message

paragraph = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras nec lacus lacus.
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus molestie
elementum erat, in fermentum nisi bibendum quis. Duis tincidunt sollicitudin
tortor, et feugiat ligula mattis ut. Sed vitae sagittis magna. Praesent ut leo
sit amet eros volutpat interdum ut sed odio. Suspendisse potenti. Integer
condimentum tincidunt felis quis efficitur. Donec posuere sem a augue maximus,
non molestie elit eleifend. Mauris porttitor, arcu in dignissim semper, nisl
nunc gravida lectus, in imperdiet magna ipsum sed velit. Sed malesuada tincidunt
turpis, sed facilisis eros commodo et. Vivamus ornare risus at lectus
sollicitudin dictum. Cras eu diam ut dolor consequat condimentum. In
hac habitasse platea dictumst. Cras hendrerit quam in leo dictum,
vitae egestas felis varius. Aenean rhoncus magna a sagittis porta.
"""


def test_message_fit_to_term():
    # 1. Long-messages.
    long_message = Message(contents=paragraph)
    columns, _ = get_terminal_size()

    assert type(long_message.contents) is list

    for line in long_message.contents:
        assert line.__len__() <= columns

    # 2. Short-messages.
    short_message = Message(contents='foo')
    assert type(short_message.contents) is str


def test_message_replacements():
    d = {'contents': '{foo}', 'replacements': {'foo': 'bar'}}
    message = Message(**d)

    assert message.contents == 'bar'


def test_message_new_line():
    d = {'contents': 'foo', 'new_line': True}
    message = Message(**d)

    assert '\n' in message.contents


def test_message_echo():
    Message(contents=paragraph).echo()    # Multi-line
    Message(contents='foo').echo()    # Single-line
