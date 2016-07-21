import os
from shutil import get_terminal_size


def boolean_response(question, default=False):
    error = None
    while True:
        question_str_r = '{question} [{y}/{n}]{error}'.format(
            question=question,
            y='Y' if default else 'y',
            n='N' if not default else 'n',
            error=' ({})'.format(error) if error else '')
        question_message = Message(question_str_r)
        question_message.echo()
        answer = input()

        if answer is '':
            return default
        elif answer in ('y', 'Y'):
            return True
        elif answer in ('n', 'N'):
            return False
        error = 'Invalid Response'


class Table():
    pass


class Message():

    def __init__(self, contents, replacements=None, new_line=False):
        self.contents = contents
        if replacements:
            self.contents = self.contents.format(**replacements)
        if new_line:
            self.contents += '\n'
        self.fit_to_terminal()

    def echo(self):
        contents = self.contents
        if type(contents) is str:
            print(self.contents)
        else:
            for line in self.contents:
                print(line)

    def fit_to_terminal(self):
        t_columns, _ = get_terminal_size()
        if self.contents.__len__() > t_columns:
            words = self.contents.split(' ')

            lines = []
            line = []
            for word in words:
                new_line_r = ' '.join(line) + ' {}'.format(word)
                if new_line_r.__len__() < t_columns:
                    line.append(word)
                else:
                    lines.append(' '.join(line))
                    line = [word]
            # Prevents having an index to check for the last-item in words.
            lines.append(' '.join(line))
            self.contents = lines
