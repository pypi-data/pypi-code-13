# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

_package_data = dict(
    full_package_name="ruamel.browser.server.selenium",
    version_info=(0, 1, 2),
    author="Anthon van der Neut",
    author_email="a.van.der.neut@ruamel.eu",
    description="selenium firefox browser plugin",
    # keywords="",
    entry_points=None,
    license="MIT License",
    since=2016,
    status=u"β",  # the package status on PyPI
    install_requires=dict(
        any=["ruamel.appconfig", "ruamel.std.argparse", "selenium", "ruamel.browser.server", ],
    ),
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP",
    ],
)


def _convert_version(tup):
    """Create a PEP 386 pseudo-format conformant string from tuple tup."""
    ret_val = str(tup[0])  # first is always digit
    next_sep = "."  # separator for next extension, can be "" or "."
    for x in tup[1:]:
        if isinstance(x, int):
            ret_val += next_sep + str(x)
            next_sep = '.'
            continue
        first_letter = x[0].lower()
        next_sep = ''
        if first_letter in 'abcr':
            ret_val += 'rc' if first_letter == 'r' else first_letter
        elif first_letter in 'pd':
            ret_val += '.post' if first_letter == 'p' else '.dev'
    return ret_val

version_info = _package_data['version_info']
__version__ = _convert_version(version_info)

del _convert_version


import os                                                             # NOQA
import time                                                           # NOQA
from glob import glob                                                 # NOQA

import selenium.common                                                # NOQA
from selenium import webdriver                                        # NOQA
from selenium.webdriver.common.action_chains import ActionChains      # NOQA
from selenium.webdriver.support.ui import Select                      # NOQA
NSEE = selenium.common.exceptions.NoSuchElementException              # NOQA

from ..browser import Browser, NoSuchElementException                 # NOQA


class SeleniumBrowser(Browser):
    def __init__(self, name, **kw):
        self._selenium = None
        super(SeleniumBrowser, self).__init__(name, **kw)

    @property
    def br(self):
        return self._selenium

    def get(self, url, elem):
        print(u'getting [{}]'.format(url))
        self.br.get(url)
        return ''

    def keys(self, keys, elem, add=False):
        if elem is None:
            elem = '_'
        if not add:
            self._kw[elem].clear()   # get rid of any previous non-recognised stuff
        self._kw[elem].send_keys(keys)
        return 'ok'

    def find(self, msg, elem):
        """find [use top] [store key] id|class|css rest
        if "use top" not provided search whole page
        if "store key" not provided only store in _
        rest can have spaces
        """
        if elem is None:
            elem = self.br
        else:
            elem = self._kw[elem]
        try:
            store_key = None
            cmd, k, rest = msg.split(None, 2)
            if cmd == u'store':
                store_key = k
                msg = rest
        except ValueError:
            pass
        try:
            typ, msg = msg.split(None, 1)
            typ = typ.lower()
            if typ == 'id':
                res = elem.find_element_by_id(msg)
            elif typ == 'class':
                res = elem.find_element_by_class_name(msg)
            elif typ == 'css':
                res = elem.find_element_by_css_selector(msg)
            else:
                return "Not implemented: " + typ
            if store_key:
                self._kw[store_key] = res
            self._kw['_'] = res
            return 'ok'
        except NSEE:
            raise NoSuchElementException
        except:
            print('rbs.selenium general raising')
            raise

    def select(self, msg, elem):
        """select, first msg part is typ
        """
        if elem is None:
            elem = '_'
        sel = Select(self._kw[elem])
        typ, msg = msg.split(None, 1)
        typ = typ.lower()
        if typ == 'index':
            res = sel.select_by_index(msg)  # does this need an int or is str ok?
        elif typ == 'text':
            res = sel.select_by_visible_text(msg)
        elif typ == 'value':
            res = sel.select_by_visible_text(msg)
        else:
            return "Not implemented: " + typ
        res = res
        return 'ok'

    def click(self, message, elem):
        if elem is None:
            elem = '_'
        self._kw[elem].click()

    def inner(self, msg, elem):
        """normally used with element previously found
        msg part discarded
        """
        if msg:
            print('\nSeleniumBrowser.inner: unused {}\n'.format(msg))
        if elem is None:
            elem = '_'
        return self._kw[elem].get_attribute('innerHTML')

    def javascript(self, arg, elem):
        return self.br.execute_script(arg)

    def title(self, message, elem):
        return self.br.title

    def current_url(self, message, elem):
        return self.br.current_url

    def hover(self, message, elem):  # untested
        if elem is None:
            elem = '_'
        h = ActionChains(self._browser).move_to_element(self._kw[elem])
        h.perform()

    def mouse_down_up(self, elem):
        if elem is None:
            elem = '_'
        action = ActionChains(self.br)
        action.move_to_element(self._kw[elem])
        action.click_and_hold()
        try:
            action.perform()
        except:
            pass
        time.sleep(0.5)
        action = ActionChains(self.br)
        action.release()
        action.perform()

    down_up = mouse_down_up
    downup = mouse_down_up

    def findallid(self, message, elem):
        res = []
        if elem is None:
            top = self.br
        else:
            top = self._kw[elem]
        for elem in top.find_elements_by_css_selector(message):
            res.append(elem.get_attribute('id'))
        return ' '.join(res)

    def displayed(self, message, elem):
        if elem is None:
            elem = '_'
        return ('yes' if self._kw[elem].is_displayed() else 'no')

    def quit(self):
        self.br.quit()


# FirefoxSeleniumBrowser
class Browser(SeleniumBrowser):
    def __init__(self, name, **kw):
        super(SeleniumBrowser, self).__init__(name, **kw)
        adblock_xpi = self.load_selenium_files('adblock/adblock_plus*.xpi')
        if adblock_xpi:
            try:
                ffprofile = webdriver.FirefoxProfile(self.load_selenium_files('profile00'))
                ffprofile.add_extension(adblock_xpi)
                self._selenium = webdriver.Firefox(ffprofile)
                return
            except:
                print('exception in loading adblock', adblock_xpi)
                raise
        self._selenium = webdriver.Firefox()

    def load_selenium_files(self, pattern):

        base_dirs = [os.environ.get('RBSSELENIUM')]
        for base_dir in ['/data1', '/data0']:
            base_dirs.append(os.path.join(base_dir, 'DATA', 'selenium'))
        for base_dir in base_dirs:
            pat = os.path.join(pattern)
            # print('trying', pat)
            res = glob(pat)
            if res:
                break
        else:
            return
        return sorted(res)[-1]  # the newest one if multiple
