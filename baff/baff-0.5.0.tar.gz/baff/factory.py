import tornado.web
from tornado.ioloop import IOLoop
from Queue import Queue
import argparse
from ConfigParser import ConfigParser
from api import Type
import api
from loop import SyncLoop


def load_tabs(config=None):

    assert config is not None

    tabs = {}

    for section in config.sections():
        if section.startswith('process:'):
            section_name = section[8:]
            tab_type = config.get(section, 'type')

            if tab_type == Type.CLI:
                tab = {'command': config.get(section, 'command'),
                       'type': Type.CLI}
                if config.has_option(section, 'user'):
                    tab['user'] = config.get(section, 'user')

            elif tab_type == Type.REQUEST:
                tab = {'uri': config.get(section, 'uri'),
                       'type': Type.REQUEST}
            
            tabs[section_name] = tab

    return tabs

def make_api_application(queue=None, tabs=None):
    urls = [
        (r'^/enqueue$', api.EnqueueHandler),
    ]
    app = tornado.web.Application(urls)
    app.queue = queue
    app.tabs = tabs

    return app

def parse_config(file=None):
    config = ConfigParser()
    confile = file if file \
              else '../tests/default.ini'
    config.readfp(open(confile))
    return config

def parse_args():
    aparser = argparse.ArgumentParser()
    aparser.add_argument('-c', type=str)
    parsed = aparser.parse_args()
    return parsed


def main_loop(tabs={}, port=4545, queue=Queue(),
              processing=[]):
    app = make_api_application(queue=queue,
                               tabs=tabs
                               )
    app.listen(port)
    SyncLoop(queue=queue, tabs=tabs).start()
    IOLoop.current().start()