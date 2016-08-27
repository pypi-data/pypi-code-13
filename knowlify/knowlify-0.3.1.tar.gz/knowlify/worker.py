import os
import sys
import config
import time
import re
from lxml import html


def output_page(page, name=None):

    assert isinstance(page, html.HtmlElement)
    if name is None:
        #name = os.path.join(config.DATA_DIR, 'knowl_'+ page.text_content().lstrip('\r\n')[:11] + str(time.time()) + '.html')
        name = os.path.join(config.DATA_DIR, 'knowl_'+ page.text_content().lstrip('\r\n')[:11] + '.html')

    # if os.path.isfile(name):
    #     name += str(time.time())

    try:
        with open(name, 'w') as f:
            f.write(html.tostring(page))
    except OSError:
        sys.stderr('Unable to write output for filename: %s' % name)
        return 2




def output_dummy(page, len=100):
    assert isinstance(page, html.HtmlElement)
    name = 'knowl_'+ page.body.text_content().lstrip('\r\n')[:11] + '.html'
    path = os.path.join(config.DATA_DIR,name)

    # if os.path.isfile(name):
    #     name += str(time.time())

    try:
        with open(path, 'w') as f:
            f.write(html.tostring(page.body)[:len])
    except OSError:
        sys.stderr('Unable to write output for dummy file: %s' % name)
        return 2
    return name

if __name__ == "__main__":
    pass
