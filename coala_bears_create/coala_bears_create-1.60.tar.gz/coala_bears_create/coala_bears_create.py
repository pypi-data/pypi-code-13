import argparse
from functools import lru_cache
import os
import logging
import string
import sys

from coalib.settings.Section import Section
from coalib.misc.DictUtilities import inverse_dicts
from coalib.collecting.Collectors import collect_all_bears_from_sections
from coalib.output.printers.LogPrinter import LogPrinter

from coala_utils.Question import ask_question
from coala_utils.string_processing.StringConverter import StringConverter

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.validation import ValidationError, Validator

from pygments.style import Style
from pygments.styles.default import DefaultStyle
from pygments.token import Token

from pyprint.NullPrinter import NullPrinter


@lru_cache()
def get_all_bears():
    """
    Get a dict of bears with the bear class as key.
    The dict of bears is only created from the default bear directories
    with no additional configurations to coala.

    >>> [True for bear in get_all_bears() if 'RuboCopBear' in bear.name]
    [True]

    :return:
        A dict with bear classes as key and the list of sections
        as value.
    """
    log_printer = LogPrinter(NullPrinter())
    sections = {'default': Section('default')}
    local_bears, global_bears = collect_all_bears_from_sections(
        sections, log_printer)

    return inverse_dicts(local_bears, global_bears)


def get_languages():
    """
    Get a list of dict of languages with bear name.

    >>> "C++" in get_languages()
    True

    :return:
        A set with all languages present as value.
    """
    return {language for bear in get_all_bears() for language in bear.LANGUAGES}


def add_status_bar(cli):
    """
    Add a message to the status bar.

    :return:
        A status bar of class Token with custom message
    """
    return [(Token.Toolbar,
             "'regex' for parsing messages yielded by executable, 'corrected' "
             "for parsing a corrected version of the inputted file")]


def status_bar_languages(cli):
    """
    Instruction message for languages question.

    :return:
        A status bar of class Token with custom message
    """
    return [(Token.Toolbar,
             'Press Escape + Enter to move to next question')]


def get_continuation_tokens(cli, width):
    return [(Token, '.' * width)]


class BearTypeValidator(Validator):

    def validate(self, document):
        """
        Display error message if text not valid.

        return:
            A status bar with validation error message
        """
        text = document.text.lower()
        if text not in ("regex", "corrected"):
            raise ValidationError(message='Enter "regex" for regex bears and '
                                          '"corrected" for autocorrect bears.')


class DocumentStyle(Style):
    """
    Styles for dropdown list and status bar. Styles are populated using a
    dictionary with the key being Token subclasses and the value being a list.
    """
    styles = dict(DefaultStyle.styles)
    styles.update({
        # hex for background color of highlighted member of dropdown list.
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        # hex for background color of dropdown list.
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        # hex for background color of bottom status bar.
        Token.Toolbar: '#ffffff bg:#333333'
    })


def load_template(file):
    """
    Return lines from file as a string.

    :return:
        The content of the file as a string.
    """
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "scaffold-templates", "{}.in".format(file))
    with open(path) as temp:
        return temp.read()


# To be used when no default value is given
NoDefaultValue = object()


def create_setting(sdesc, stype, sdefault=NoDefaultValue):
    """
    Create a tuple ``(sdesc, stype)`` for non_optional settings and
    ``(sdesc, stype, sdefault)`` for optional settings.

    :param sdesc:
        Setting description.
    :param stype:
        Setting type.
    :param sdefault:
        Setting default value.
    :return:
        A tuple with the setting information.
    """
    return ((sdesc, stype) if sdefault is NoDefaultValue
            else (sdesc, stype, sdefault))


def main():
    # Default values if the user chooses to skip a question.
    conf = {
        'name': '',
        'testname': '',
        'description': '',
        'language': (),
        'bear_type': '',
        'executable': '',
        'settings': {},
        'arguments': (),
        'requirements': '',
        'authors': '',
        'authors_emails': '',
        'license': '',
    }

    parser = argparse.ArgumentParser(
        description="Generate a linter bear and test " +
                    "file using the command line",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--path', metavar="path",
                        help="Path where your files will be generated")
    parser.add_argument('-n', '--name', metavar="name",
                        help='Name of bear')
    parser.add_argument('-d', '--desc', metavar="description",
                        help='Description of bear')
    parser.add_argument('-e', '--executable', metavar="",
                        help='Name of linter executable')
    parser.add_argument('-l', '--lang', metavar="language",
                        help='Language that the bear will be used on')
    parser.add_argument('-t', '--type', metavar="type",
                        help='Type of bear')
    parser.add_argument('-ext', '--external', default=False,
                        action="store_true", help='Creates an external bear ' +
                        'instead of a regular one')
    args = parser.parse_args()

    print('''Welcome to coala-bears-create.

This command line tool will help you configure a coala bear and test file.
Please answer the following questions so this tool can help you automate
generating the files.
''')

    directory = args.path or os.path.abspath(
        os.path.expanduser(ask_question(
            'Where do you want to create your new bear? ', default=os.curdir)))

    conf['name'] = args.name or ask_question('Name of this bear: ')
    conf['description'] = args.desc or (ask_question(
        'Description of the bear: '))
    conf['executable'] = args.executable or (
        ask_question('Name of the the executable: '))
    if not args.external:
        conf['bear_type'] = args.type or (ask_question(
            'What is the type of output the external executable ' +
            'produces? (regex/corrected)',
                get_bottom_toolbar_tokens=add_status_bar,
                style=DocumentStyle,
                validator=BearTypeValidator()).lower())
    elif ask_question('Do you want to use settings? ', default="No",
                      typecast=bool):
        more_settings = True
        setting_strings = ""
        while more_settings:
            setting_strings += ask_question(
                'Give settings as name|desc|type[|default_value]: ',
                multiline=True,
                style=DocumentStyle,
                get_continuation_tokens=get_continuation_tokens,
                get_bottom_toolbar_tokens=status_bar_languages) + "\n"
            more_settings = ask_question('Are there more settings?',
                                         default="No", typecast=bool)
        setting_strings = setting_strings.split('\n')
        for setting_string in (setting_str for setting_str in setting_strings
                               if len(setting_str) != 0):
            setting_string = setting_string.split('|')
            sname = setting_string[0]
            sdesc = setting_string[1]
            stype = setting_string[2]
            # check if default value was provided
            if len(setting_string) == 4:
                sdefault = getattr(__builtins__, stype)(
                    StringConverter(setting_string[3]))
                conf['settings'][sname] = create_setting(sdesc, stype,
                                                         sdefault)
            else:
                conf['settings'][sname] = create_setting(sdesc, stype)

    conf['language'] = args.lang or ask_question(
        'Languages that bear will support: ', typecast=set,
        completer=WordCompleter(get_languages(), ignore_case=True),
        style=DocumentStyle,
        multiline=True,
        get_continuation_tokens=get_continuation_tokens,
        get_bottom_toolbar_tokens=status_bar_languages)
    conf['requirements'] = ask_question(
        'Add dependencies used by the executable: ', typecast=set)
    conf['authors'] = ask_question(
        'Add Author(s) name(s): ', typecast=set)
    conf['authors_emails'] = ask_question(
        'Add Author(s) email(s): ', typecast=set)
    conf['license'] = ask_question('Add License name for this code: ')

    if not conf['name'].lower().endswith('bear'):
        conf['name'] += 'Bear'

    conf['testname'] = conf['name'] + 'Test'
    bearfilename = conf['name'] + '.py'
    testfilename = conf['name'] + 'Test.py'
    template_file = 'bearconf' if not args.external else 'externalbearconf.py'
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as e:
        logging.exception('Cannot create directory: {}'.format(e))
        return

    try:
        processed_template = string.Template(load_template(template_file)
                                             ).safe_substitute(conf)
        with open(os.path.join(directory, bearfilename), 'w') as template:
            template.write(processed_template)

    except OSError as e:
        logging.exception('Cannot create bear file: {}'.format(e))
        return

    try:
        processed_template = string.Template(load_template('testconf')
                                             ).safe_substitute(conf)
        with open(os.path.join(directory, testfilename), 'w') as template:
            template.write(processed_template)
    except OSError as e:
        logging.exception('Cannot create test file: {}'.format(e))
        return

    print("Successfully completed generating your bear and test file"
          " at '{}'. You can now modify the files inside and implement your"
          " own bear."
          .format(directory))


if __name__ == "__main__":
    sys.exit(main())
