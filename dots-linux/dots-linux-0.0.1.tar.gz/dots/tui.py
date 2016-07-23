"""Interface to interact with the user through the terminal."""

from shutil import get_terminal_size


def boolean_response(question, default=False):
    """Ask a yes-or-no question

    Args:
        question (str): message to the user
        default (bool): option if the input is None
    """

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


class Message():
    """One-way communication between the program and the user."""

    def __init__(self, contents, replacements=None, new_line=False):
        """Utility to format a message to display to the user.

        If the contents exceed the terminal-width then the message is truncated
        into multiple-lines represented by a list.

        Args:
            contents (str): message to relay to the user
            replacements (dict): **kwargs to pass to str.format
            new_line (bool): whether to append a new-line
        """

        self.contents = contents
        if replacements:
            # yapf: disable
            self.contents = self.contents.format(**replacements) # pylint: disable=no-member
            # yapf: enable
        if new_line:
            self.contents += '\n'
        self.fit_to_terminal()

    def echo(self):
        """Display the message to the user."""

        contents = self.contents
        if isinstance(contents, str):
            print(self.contents)
        else:
            for line in contents:
                print(line)

    def fit_to_terminal(self):
        """Break the message-contents into readable pieces."""

        t_columns, _ = get_terminal_size()
        if self.contents.__len__() > t_columns:
            words = self.contents.split(' ')    # pylint: disable=no-member

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
