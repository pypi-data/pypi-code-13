from slackclient import SlackClient
from IPython.core.magic import (cell_magic, line_magic, Magics, magics_class)

from IPython.utils import io

def load_ipython_extension(ipython):
    ipython.register_magics(Slack)

@magics_class
class Slack(Magics):

    def __init__(self, shell):
        # You must call the parent constructor
        super(Slack, self).__init__(shell)
        self.channel = None
        self.token = None
        self.client = None

    def parse_line(self, line):
        return line.split()

    @line_magic
    def slack_setup(self, line, cell=None):
        self.channel, self.token = self.parse_line(line)
        self.client = SlackClient(self.token)

    @cell_magic
    def slack(self, line, cell):
        with io.capture_output() as captured:
            res = self.shell.run_cell(cell)
        print captured
        self.client.api_call(
            'chat.postMessage',
            channel=self.channel,
            text='{}\n```\n{}```'.format(
                str(line),
                str(captured)
            ),
            parse='full'
        )

