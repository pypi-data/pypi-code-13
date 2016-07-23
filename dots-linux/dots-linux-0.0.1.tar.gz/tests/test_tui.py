"""Tests for TUI utilities."""

from dots.tui import Message

paragraph = """
 xLorem ipsum dolor sit amet, consectetur adipiscing elit. Cras nec lacus lacus.
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
    """Test that messages exceeding the terminal-width are formatted across
    multiple lines represented as a list, and that messages which do not exceed
    the terminal-width are maintained."""

    # 1. Long-messages.
    long_message = Message(contents=paragraph)
    columns = 80

    assert isinstance(long_message.contents, list)

    for line in long_message.contents:
        assert line.__len__() <= columns

    # 2. Short-messages.
    short_message = Message(contents='foo')
    assert isinstance(short_message.contents, str)


def test_message_replacements():
    """Test the 'replacements' option.

    Expected output is the same as supplying **kwargs to `str.replace`."""

    d = {'contents': '{foo}', 'replacements': {'foo': 'bar'}}
    message = Message(**d)

    assert message.contents == 'bar'


def test_message_new_line():
    """Test that a new-line character is appended to the end of the string."""

    d = {'contents': 'foo', 'new_line': True}
    message = Message(**d)

    assert '\n' in message.contents


def test_message_echo():
    """Test that the `echo` function is callable."""

    Message(contents=paragraph).echo()    # Multi-line
    Message(contents='foo').echo()    # Single-line
