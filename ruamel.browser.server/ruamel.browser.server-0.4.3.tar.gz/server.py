# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

"""
http://stackoverflow.com/questions/20832159/python-using-adblock-with-selenium-
http://stackoverflow.com/questions/27591787/python-selenium-firefox-adblock
Py3 problems?:
http://stackoverflow.com/questions/30071156/open-firefox-webdriver-with-adblock-

client to server communication:

init name typ subtype   # e.g. init sporcle selenium firefox initialises a new browser with
                        # name as point to return
all further references are prefixed with 'br name'

br name quit    # release browser
br name get url # gets a url, resets default element to full page
br name [elem el] css|id|class rest
br name [elem el]


Each Server can start multiple Virtual Browsers.
A Virtual Browser has some connection to e.g. selenium, knows its type,
what item was last selected (if not by name) etc

On pooh: new version of Firefox, update the adblock xpi (in /data1/DOWNLOAD/selenium/adblock
and then update selenium in the dev virtualenv (pip install --upgrade selenium)


"""

import sys
import os                 # NOQA
import traceback

from importlib import import_module

import zmq

from .vnc import VNC
from .browser import NoSuchElementException

import selenium.common
NSEE = selenium.common.exceptions.NoSuchElementException


class Server(object):
    def __init__(self, args, config):
        """
        unless a display is set, the browsers are on the desktop
        you create a display by vnc name and use that vnc name to create
        a browser
        """
        self._args = args
        self._config = config
        self._name = None
        self._displays = {}  # map from name to (VNC) display
        self._browsers = {}  # map from name to browser
        self._browser = None
        self._processes_to_kill = []
        self._kw = {}
        self.element = None
        self._browser_classes = {}  # imported Browser types
        self._browsers1 = {}

        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:{}".format(self._args.port))
        print('listening on:', self._args.port)
        # new version
        while True:
            res = None
            message = socket.recv_string()
            print(u'received:', message)
            if message == u'restart':
                socket.send_string(u'received ' + message)
                raise NotImplementedError
                # have to close all browsers here
                for br in self._browsers.values():
                    br.quit()
                os.execvp(sys.argv[0], sys.argv)
            try:
                res = self.process(message)
            except NoSuchElementException:
                res = u'NSEE'
            except NSEE:
                res = u'NSEE'
            except Exception as e:
                print(traceback.format_exc())
                print('e', type(e), e.message)
                res = str(type(e)) + u'|' + str(e)
            finally:
                if res is None:
                    res = 'not specified'
                try:
                    socket.send_string(res)
                except Exception as e:
                    print('ex', type(e), e.message)
                    print(repr(res))
                    socket.send_string(u'excepted')

    def process(self, message):
        msgw = message.split(None, 2)
        print('msgw', msgw)
        if msgw[0] == u'br':
            self._name = msgw[1]
            br = self._browsers[self._name]
            self._browser = br.br
            self._kw = self._browsers[self._name]._kw
            message = msgw[2]
            msgw = message.split()
        elif msgw[0] == u'display':
            return self.display(*message.split()[1:])
        elif msgw[0] == u'init':
            return self.init(*message.split()[1:])
        elif msgw[0] == u'init2':
            print('rbs: old init2 used')
            return self.init(*message.split()[1:])
        elif msgw[0] == u'check':
            # check if browser name is known
            return 'active' if msgw[1] in self._browsers else 'unknown'
        else:
            raise NotImplementedError('cmd ' + message)
        if br.verbose > 0:
            print('msgw', msgw)
            print('kw', self._kw.keys())
        elem = None
        try:
            cmd, message = message.split(None, 1)
        except ValueError:
            # message always contains a command, not necessarily a parameter
            cmd, message = message, ''
        if cmd == u'elem':
            try:
                elem, cmd, message = message.split(None, 2)
            except ValueError:
                # if you have an element to work on you still have a command,
                # but not necessarily a parameter
                elem, cmd = message.split(None, 2)
                message = ''
        if br.verbose > 0:
            print('cmd [{}], elem [{}], message [{}]'.format(cmd, elem, message))
        if not br.br:
            return 'not inited'
        if cmd == u'quit':
            br.quit()
            del self._browsers[self._name]
            return 'quit'
        elif cmd == u'verbose':
            br.verbose = message  # this sets a property, cannot have second (ignored) param
            return ''
        elif hasattr(br, cmd):
            func = getattr(br, cmd)
            print('attr calling', cmd, repr(message), repr(elem))
            return func(message, elem)
        print('did not find ' + repr(cmd))

    def init(self, *args):
        """args is optionally prefixed, peel those prefixes off"""
        del_tz = display = None
        while True:
            print('args', args)
            if args[0] == 'tz':
                del_tz = True
                if args[1] == '+':
                    os.environ['TZ'] = 'Pacific/Kiritimati'
                elif args[1] == '-':
                    os.environ['TZ'] = 'Pacific/Midway'
                else:
                    os.environ['TZ'] = args[1]
                args = args[2:]
                continue
            if args[0] == 'display':
                display = args[1]
                args = args[2:]
                continue
            break
        if display is not None:
            if not hasattr(self._displays[display], 'old_display_var'):
                self._displays[display].start()
            else:
                self._displays[display].redirect_display(True)
        print('starting with DISPLAY', os.environ['DISPLAY'])
        self.create_browser(*args)
        if display is not None:
            self._displays[display].redirect_display(False)
        if del_tz is not None:
            del os.environ['TZ']

    def display(self, *args):
        """setup a display (VNC) with name"""
        name, port, size_x, size_y = args[:4]
        if name in self._displays:
            return 'display with name "{}" already created'.format(name)
        self._displays[name] = VNC(backend='myxvnc',
                                   size=(int(size_x), int(size_y)),
                                   rfbport=port)
        print('display vnc {}x{} {}'.format(size_x, size_y, port))

    def create_browser(self, name, typ, subtype=None, proxy=None,
                       vnc=None):
        """
        name: identifier later passed as parameter to 'br'
        typ: type of browser loaded from ruamel.browser.server.{typ}

        """
        self._processes_to_kill = []
        br = self._browsers.get(name)
        if br:
            br.quit()
        typ = typ.lower()
        browser_class = self._browser_classes.get(typ)
        if browser_class is None:
            full_module_name = 'ruamel.browser.server.' + typ
            mod = import_module(full_module_name)
            browser_class = self._browser_classes[typ] = getattr(mod, 'Browser')
        if browser_class is None:
            print('rbs: cannot find browser class')
            raise NotImplementedError
        self._browsers[name] = browser_class(name)
        return

    # def close(self):
    #     self.browser.close()
