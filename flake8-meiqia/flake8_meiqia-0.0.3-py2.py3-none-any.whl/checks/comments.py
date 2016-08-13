import re
import tokenize

from flake8_meiqia import core


_TODO_RE = re.compile(r'''
    (?P<leading>[@\W])?
    (?P<todo>TODO|ToDo|FIXME|FixMe|XXX)
    (?P<trailing>\()?''', re.VERBOSE)


@core.flake8ext
def meiqia_todo_format(physical_line, tokens):
    """Checks for 'TODO()' in comments.

    Okay: # TODO(timonwong)
    MQ101: # TODO
    MQ101: # TODO xxx
    MQ101: # TODO (timonwong)
    MQ101: # @ToDo
    """

    for token_type, text, start_index, _, _ in tokens:
        if token_type == tokenize.COMMENT:
            m = _TODO_RE.search(text)
            if not m:
                continue

            groups = m.groupdict()
            todo_name = groups['todo'].upper()
            if (groups['leading'] == '@' or groups['todo'] != todo_name or
                    groups['trailing'] != '('):
                if groups['leading'] == '@':
                    err_pos = m.start('leading') + start_index[1]
                else:
                    err_pos = m.start('todo') + start_index[1]

                return err_pos, "MQ101: Use %s(NAME)" % todo_name
