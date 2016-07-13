#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# jp: a SAT command line tool
# Copyright (C) 2009-2016 Jérôme Poisson (goffi@goffi.org)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from sat.core.i18n import _

### logging ###
import logging as log
log.basicConfig(level=log.DEBUG,
                    format='%(message)s')
###

import sys
import locale
import os.path
import argparse
from gi.repository import GLib
from glob import iglob
from importlib import import_module
from sat_frontends.tools.jid import JID
from sat_frontends.bridge.DBus import DBusBridgeFrontend
from sat.core import exceptions
import sat_frontends.jp
from sat_frontends.jp.constants import Const as C
import xml.etree.ElementTree as ET  # FIXME: used temporarily to manage XMLUI
import shlex
from collections import OrderedDict

if sys.version_info < (2, 7, 3):
    # XXX: shlex.split only handle unicode since python 2.7.3
    # this is a workaround for older versions
    old_split = shlex.split
    new_split = (lambda s, *a, **kw: [t.decode('utf-8') for t in old_split(s.encode('utf-8'), *a, **kw)]
        if isinstance(s, unicode) else old_split(s, *a, **kw))
    shlex.split = new_split

try:
    import progressbar
except ImportError:
    log.info (_('ProgressBar not available, please download it at http://pypi.python.org/pypi/progressbar'))
    log.info (_('Progress bar deactivated\n--\n'))
    progressbar=None

#consts
PROG_NAME = u"jp"
DESCRIPTION = """This software is a command line tool for XMPP.
Get the latest version at """ + C.APP_URL

COPYLEFT = u"""Copyright (C) 2009-2016 Jérôme Poisson, Adrien Cossa
This program comes with ABSOLUTELY NO WARRANTY;
This is free software, and you are welcome to redistribute it under certain conditions.
"""

PROGRESS_DELAY = 10 # the progression will be checked every PROGRESS_DELAY ms


def unicode_decoder(arg):
    # Needed to have unicode strings from arguments
    return arg.decode(locale.getpreferredencoding())


class Jp(object):
    """
    This class can be use to establish a connection with the
    bridge. Moreover, it should manage a main loop.

    To use it, you mainly have to redefine the method run to perform
    specify what kind of operation you want to perform.

    """
    def __init__(self):
        """

        @attribute quit_on_progress_end (bool): set to False if you manage yourself exiting,
            or if you want the user to stop by himself
        @attribute progress_success(callable): method to call when progress just started
            by default display a message
        @attribute progress_success(callable): method to call when progress is successfully finished
            by default display a message
        @attribute progress_failure(callable): method to call when progress failed
            by default display a message
        """
        try:
            self.bridge = DBusBridgeFrontend()
        except exceptions.BridgeExceptionNoService:
            print(_(u"Can't connect to SàT backend, are you sure it's launched ?"))
            sys.exit(1)
        except exceptions.BridgeInitError:
            print(_(u"Can't init bridge"))
            sys.exit(1)

        self.parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                              description=DESCRIPTION)

        self._make_parents()
        self.add_parser_options()
        self.subparsers = self.parser.add_subparsers(title=_('Available commands'), dest='subparser_name')
        self._auto_loop = False # when loop is used for internal reasons
        self._need_loop = False

        # progress attributes
        self._progress_id = None # TODO: manage several progress ids
        self.quit_on_progress_end = True

        # outputs
        self._outputs = {}
        for type_ in C.OUTPUT_TYPES:
            self._outputs[type_] = OrderedDict()

    @property
    def version(self):
        return self.bridge.getVersion()

    @property
    def progress_id(self):
        return self._progress_id

    @progress_id.setter
    def progress_id(self, value):
        self._progress_id = value
        self.replayCache('progress_ids_cache')

    @property
    def watch_progress(self):
        try:
            self.pbar
        except AttributeError:
            return False
        else:
            return True

    @watch_progress.setter
    def watch_progress(self, watch_progress):
        if watch_progress:
            self.pbar = None

    @property
    def verbosity(self):
        try:
            return self.args.verbose
        except AttributeError:
            return 0

    def replayCache(self, cache_attribute):
        """Replay cached signals

        @param cache_attribute(str): name of the attribute containing the cache
            if the attribute doesn't exist, there is no cache and the call is ignored
            else the cache must be a list of tuples containing the replay callback as first item,
            then the arguments to use
        """
        try:
            cache = getattr(self, cache_attribute)
        except AttributeError:
            pass
        else:
            for cache_data in cache:
                cache_data[0](*cache_data[1:])

    def disp(self, msg, verbosity=0, error=False):
        """Print a message to user

        @param msg(unicode): message to print
        @param verbosity(int): minimal verbosity to display the message
        @param error(bool): if True, print to stderr instead of stdout
        """
        if self.verbosity >= verbosity:
            if error:
                print >>sys.stderr,msg
            else:
                print msg

    def output(self, type_, name, data):
        self._outputs[type_][name]['callback'](data)

    def addOnQuitCallback(self, callback, *args, **kwargs):
        """Add a callback which will be called on quit command

        @param callback(callback): method to call
        """
        try:
            callbacks_list = self._onQuitCallbacks
        except AttributeError:
            callbacks_list = self._onQuitCallbacks = []
        finally:
            callbacks_list.append((callback, args, kwargs))

    def getOutputChoices(self, output_type):
        """Return valid output filters for output_type

        @param output_type: True for default,
            else can be any registered type
        """
        return self._outputs[output_type].keys()

    def _make_parents(self):
        self.parents = {}

        # we have a special case here as the start-session option is present only if connection is not needed,
        # so we create two similar parents, one with the option, the other one without it
        for parent_name in ('profile', 'profile_session'):
            parent = self.parents[parent_name] = argparse.ArgumentParser(add_help=False)
            parent.add_argument("-p", "--profile", action="store", type=str, default='@DEFAULT@', help=_("Use PROFILE profile key (default: %(default)s)"))
            parent.add_argument("--pwd", action="store", type=unicode, default='', metavar='PASSWORD', help=_("Password used to connect profile, if necessary"))

        profile_parent, profile_session_parent = self.parents['profile'], self.parents['profile_session']

        connect_short, connect_long, connect_action, connect_help = "-c", "--connect", "store_true", _(u"Connect the profile before doing anything else")
        profile_parent.add_argument(connect_short, connect_long, action=connect_action, help=connect_help)

        profile_session_connect_group = profile_session_parent.add_mutually_exclusive_group()
        profile_session_connect_group.add_argument(connect_short, connect_long, action=connect_action, help=connect_help)
        profile_session_connect_group.add_argument("--start-session", action="store_true", help=_("Start a profile session without connecting"))

        progress_parent = self.parents['progress'] = argparse.ArgumentParser(add_help=False)
        if progressbar:
            progress_parent.add_argument("-P", "--progress", action="store_true", help=_("Show progress bar"))

        verbose_parent = self.parents['verbose'] = argparse.ArgumentParser(add_help=False)
        verbose_parent.add_argument('--verbose', '-v', action='count', default=0, help=_(u"Add a verbosity level (can be used multiple times)"))

    def add_parser_options(self):
        self.parser.add_argument('--version', action='version', version=("%(name)s %(version)s %(copyleft)s" % {'name': PROG_NAME, 'version': self.version, 'copyleft': COPYLEFT}))

    def register_output(self, type_, name, callback, description=""):
        if type_ not in C.OUTPUT_TYPES:
            log.error(u"Invalid output type {}".format(type_))
            return
        self._outputs[type_][name] = {'callback': callback,
                                      'description': description
                                     }

    def import_plugins(self):
        """Automaticaly import commands and outputs in jp

        looks from modules names cmd_*.py in jp path and import them
        """
        path = os.path.dirname(sat_frontends.jp.__file__)
        # XXX: outputs must be imported before commands as they are used for arguments
        for type_, pattern in ((C.PLUGIN_OUTPUT, 'output_*.py'), (C.PLUGIN_CMD, 'cmd_*.py')):
            modules = (os.path.splitext(module)[0] for module in map(os.path.basename, iglob(os.path.join(path, pattern))))
            for module_name in modules:
                module = import_module("sat_frontends.jp."+module_name)
                try:
                    self.import_plugin_module(module, type_)
                except ImportError:
                    continue

    def import_plugin_module(self, module, type_):
        """add commands or outpus from a module to jp

        @param module: module containing commands or outputs
        @param type_(str): one of C_PLUGIN_*
        """
        try:
            class_names =  getattr(module, '__{}__'.format(type_))
        except AttributeError:
            log.warning(_("Invalid plugin module [{type}] {module}").format(type=type_, module=module))
            raise ImportError
        else:
            for class_name in class_names:
                cls = getattr(module, class_name)
                cls(self)

    def run(self, args=None):
        self.args = self.parser.parse_args(args)
        try:
            self.args.func()
            if self._need_loop or self._auto_loop:
                self._start_loop()
        except KeyboardInterrupt:
            log.info(_("User interruption: good bye"))

    def _start_loop(self):
        self.loop = GLib.MainLoop()
        self.loop.run()

    def stop_loop(self):
        try:
            self.loop.quit()
        except AttributeError:
            pass

    def quitFromSignal(self, errcode=0):
        """Same as self.quit, but from a signal handler

        /!\: return must be used after calling this method !
        """
        assert self._need_loop
        # XXX: python-dbus will show a traceback if we exit in a signal handler
        # so we use this little timeout trick to avoid it
        GLib.timeout_add(0, self.quit, errcode)

    def quit(self, errcode=0):
        # first the onQuitCallbacks
        try:
            callbacks_list = self._onQuitCallbacks
        except AttributeError:
            pass
        else:
            for callback, args, kwargs in callbacks_list:
                callback(*args, **kwargs)

        self.stop_loop()
        sys.exit(errcode)

    def check_jids(self, jids):
        """Check jids validity, transform roster name to corresponding jids

        @param profile: profile name
        @param jids: list of jids
        @return: List of jids

        """
        names2jid = {}
        nodes2jid = {}

        for contact in self.bridge.getContacts(self.profile):
            jid_s, attr, groups = contact
            _jid = JID(jid_s)
            try:
                names2jid[attr["name"].lower()] = jid_s
            except KeyError:
                pass

            if _jid.node:
                nodes2jid[_jid.node.lower()] = jid_s

        def expand_jid(jid):
            _jid = jid.lower()
            if _jid in names2jid:
                expanded = names2jid[_jid]
            elif _jid in nodes2jid:
                expanded = nodes2jid[_jid]
            else:
                expanded = jid
            return expanded.decode('utf-8')

        def check(jid):
            if not jid.is_valid:
                log.error (_("%s is not a valid JID !"), jid)
                self.quit(1)

        dest_jids=[]
        try:
            for i in range(len(jids)):
                dest_jids.append(expand_jid(jids[i]))
                check(dest_jids[i])
        except AttributeError:
            pass

        return dest_jids

    def connect_profile(self, callback):
        """ Check if the profile is connected and do it if requested

        @param callback: method to call when profile is connected
        @exit: - 1 when profile is not connected and --connect is not set
               - 1 when the profile doesn't exists
               - 1 when there is a connection error
        """
        # FIXME: need better exit codes

        def cant_connect(failure):
            log.error(_(u"Can't connect profile: {reason}").format(reason=failure))
            self.quit(1)

        def cant_start_session(failure):
            log.error(_(u"Can't start {profile}'s session: {reason}").format(profile=self.profile, reason=failure))
            self.quit(1)

        self.profile = self.bridge.getProfileName(self.args.profile)

        if not self.profile:
            log.error(_("The profile [{profile}] doesn't exist").format(profile=self.args.profile))
            self.quit(1)

        try:
            start_session = self.args.start_session
        except AttributeError:
            pass
        else:
            if start_session:
                self.bridge.profileStartSession(self.args.pwd, self.profile, lambda dummy: callback(), cant_start_session)
                self._auto_loop = True
                return
            elif not self.bridge.profileIsSessionStarted(self.profile):
                if not self.args.connect:
                    log.error(_(u"Session for [{profile}] is not started, please start it before using jp, or use either --start-session or --connect option").format(profile=self.profile))
                    self.quit(1)
            else:
                callback()
                return


        if not hasattr(self.args, 'connect'):
            # a profile can be present without connect option (e.g. on profile creation/deletion)
            return
        elif self.args.connect is True:  # if connection is asked, we connect the profile
            self.bridge.asyncConnect(self.profile, self.args.pwd, lambda dummy: callback(), cant_connect)
            self._auto_loop = True
            return
        else:
            if not self.bridge.isConnected(self.profile):
                log.error(_(u"Profile [{profile}] is not connected, please connect it before using jp, or use --connect option").format(profile=self.profile))
                self.quit(1)

        callback()

    def get_full_jid(self, param_jid):
        """Return the full jid if possible (add main resource when find a bare jid)"""
        _jid = JID(param_jid)
        if not _jid.resource:
            #if the resource is not given, we try to add the main resource
            main_resource = self.bridge.getMainResource(param_jid, self.profile)
            if main_resource:
                return "%s/%s" % (_jid.bare, main_resource)
        return param_jid


class CommandBase(object):

    def __init__(self, host, name, use_profile=True, use_output=False,
                       need_connect=None, help=None, **kwargs):
        """ Initialise CommandBase
        @param host: Jp instance
        @param name(unicode): name of the new command
        @param use_profile(bool): if True, add profile selection/connection commands
        @param use_output(bool, dict): if not False, add --output option
        @param need_connect(bool, None): True if profile connection is needed
            False else (profile session must still be started)
            None to set auto value (i.e. True if use_profile is set)
            Can't be set if use_profile is False
        @param help(unicode): help message to display
        @param **kwargs: args passed to ArgumentParser
            use_* are handled directly, they can be:
            - use_progress(bool): if True, add progress bar activation option
                progress* signals will be handled
            - use_verbose(bool): if True, add verbosity option
        @attribute need_loop(bool): to set by commands when loop is needed

        """
        self.need_loop = False # to be set by commands when loop is needed
        try: # If we have subcommands, host is a CommandBase and we need to use host.host
            self.host = host.host
        except AttributeError:
            self.host = host

        # --profile option
        parents = kwargs.setdefault('parents', set())
        if use_profile:
            #self.host.parents['profile'] is an ArgumentParser with profile connection arguments
            if need_connect is None:
                need_connect = True
            parents.add(self.host.parents['profile' if need_connect else 'profile_session'])
        else:
            assert need_connect is None
        self.need_connect = need_connect
        # from this point, self.need_connect is None if connection is not needed at all
        # False if session starting is needed, and True if full connection is needed

        # --output option
        if use_output:
            if use_output == True:
                use_output = C.OUTPUT_TEXT
            assert use_output in C.OUTPUT_TYPES
            self._output_type = use_output
            output_parent = argparse.ArgumentParser(add_help=False)
            choices = self.host.getOutputChoices(use_output)
            if not choices:
                raise exceptions.InternalError("No choice found for {} output type".format(use_output))
            default = 'default' if 'default' in choices else choices[0]
            output_parent.add_argument('--output', '-O', choices=choices, default=default, help=_(u"Select output format"))
            parents.add(output_parent)

        # other common options
        use_opts = {k:v for k,v in kwargs.iteritems() if k.startswith('use_')}
        for param, do_use in use_opts.iteritems():
            opt=param[4:] # if param is use_verbose, opt is verbose
            if opt not in self.host.parents:
                raise exceptions.InternalError(u"Unknown parent option {}".format(opt))
            del kwargs[param]
            if do_use:
                parents.add(self.host.parents[opt])

        self.parser = host.subparsers.add_parser(name, help=help, **kwargs)
        if hasattr(self, "subcommands"):
            self.subparsers = self.parser.add_subparsers()
        else:
            self.parser.set_defaults(func=self.run)
        self.add_parser_options()

    @property
    def args(self):
        return self.host.args

    @property
    def profile(self):
        return self.host.profile

    @property
    def progress_id(self):
        return self.host.progress_id

    @progress_id.setter
    def progress_id(self, value):
        self.host.progress_id = value

    def progressStartedHandler(self, uid, metadata, profile):
        if profile != self.profile:
            return
        if self.progress_id is None:
            # the progress started message can be received before the id
            # so we keep progressStarted signals in cache to replay they
            # when the progress_id is received
            cache_data = (self.progressStartedHandler, uid, metadata, profile)
            try:
                self.host.progress_ids_cache.append(cache_data)
            except AttributeError:
                self.host.progress_ids_cache = [cache_data]
        else:
            if self.host.watch_progress and uid == self.progress_id:
                self.onProgressStarted(metadata)
                GLib.timeout_add(PROGRESS_DELAY, self.progressUpdate)

    def progressFinishedHandler(self, uid, metadata, profile):
        if profile != self.profile:
            return
        if uid == self.progress_id:
            try:
                self.host.pbar.finish()
            except AttributeError:
                pass
            self.onProgressFinished(metadata)
            if self.host.quit_on_progress_end:
                self.host.quitFromSignal()

    def progressErrorHandler(self, uid, message, profile):
        if profile != self.profile:
            return
        if uid == self.progress_id:
            if self.args.progress:
                self.disp('') # progress is not finished, so we skip a line
            if self.host.quit_on_progress_end:
                self.onProgressError(message)
                self.host.quitFromSignal(1)

    def progressUpdate(self):
        """This method is continualy called to update the progress bar"""
        data = self.host.bridge.progressGet(self.progress_id, self.profile)
        if data:
            try:
                size = data['size']
            except KeyError:
                self.disp(_(u"file size is not known, we can't show a progress bar"), 1, error=True)
                return False
            if self.host.pbar is None:
                #first answer, we must construct the bar
                self.host.pbar = progressbar.ProgressBar(int(size),
                                                    [_(u"Progress: "),progressbar.Percentage(),
                                                     " ",
                                                     progressbar.Bar(),
                                                     " ",
                                                     progressbar.FileTransferSpeed(),
                                                     " ",
                                                     progressbar.ETA()])
                self.host.pbar.start()

            self.host.pbar.update(int(data['position']))

        elif self.host.pbar is not None:
            return False

        self.onProgressUpdate(data)

        return True

    def onProgressStarted(self, metadata):
        """Called when progress has just started

        can be overidden by a command
        @param metadata(dict): metadata as sent by bridge.progressStarted
        """
        self.disp(_(u"Operation started"), 2)

    def onProgressUpdate(self, metadata):
        """Method called on each progress updata

        can be overidden by a command to handle progress metadata
        @para metadata(dict): metadata as returned by bridge.progressGet
        """
        pass

    def onProgressFinished(self, metadata):
        """Called when progress has just finished

        can be overidden by a command
        @param metadata(dict): metadata as sent by bridge.progressFinished
        """
        self.disp(_(u"Operation successfully finished"), 2)

    def onProgressError(self, error_msg):
        """Called when a progress failed

        @param error_msg(unicode): error message as sent by bridge.progressError
        """
        self.disp(_(u"Error while doing operation: {}").format(error_msg), error=True)

    def disp(self, msg, verbosity=0, error=False):
        return self.host.disp(msg, verbosity, error)

    def output(self, data):
        return self.host.output(self._output_type, self.args.output, data)

    def add_parser_options(self):
        try:
            subcommands = self.subcommands
        except AttributeError:
            # We don't have subcommands, the class need to implements add_parser_options
            raise NotImplementedError

        # now we add subcommands to ourself
        for cls in subcommands:
            cls(self)

    def run(self):
        """this method is called when a command is actually run

        It set stuff like progression callbacks and profile connection
        You should not overide this method: you should call self.start instead
        """
        # host._need_loop is set here from our current value and not before
        # as the need_loop decision must be taken only by then running command
        self.host._need_loop = self.need_loop

        try:
            show_progress = self.args.progress
        except AttributeError:
            # the command doesn't use progress bar
            pass
        else:
            if show_progress:
                self.host.watch_progress = True
            # we need to register the following signal even if we don't display the progress bar
            self.host.bridge.register("progressStarted", self.progressStartedHandler)
            self.host.bridge.register("progressFinished", self.progressFinishedHandler)
            self.host.bridge.register("progressError", self.progressErrorHandler)

        if self.need_connect is not None:
             self.host.connect_profile(self.connected)
        else:
            self.start()

    def connected(self):
        """this method is called when profile is connected (or session is started)

        this method is only called when use_profile is True
        most of time you should override self.start instead of this method, but if loop
        if not always needed depending on your arguments, you may override this method,
        but don't forget to call the parent one (i.e. this one) after self.need_loop is set
        """
        if not self.need_loop:
            self.host.stop_loop()
        self.start()

    def start(self):
        """This is the starting point of the command, this method should be overriden

        at this point, profile are connected if needed
        """
        pass


class CommandAnswering(CommandBase):
    """Specialised commands which answer to specific actions

    to manage action_types answer,
    """
    action_callbacks = {} # XXX: set managed action types in an dict here:
                          # key is the action_type, value is the callable
                          # which will manage the answer. profile filtering is
                          # already managed when callback is called

    def onActionNew(self, action_data, action_id, security_limit, profile):
        if profile != self.profile:
            return
        try:
            action_type = action_data['meta_type']
        except KeyError:
            try:
                xml_ui = action_data["xmlui"]
            except KeyError:
                pass
            else:
                self.onXMLUI(xml_ui)
        else:
            try:
                callback = self.action_callbacks[action_type]
            except KeyError:
                pass
            else:
                callback(action_data, action_id, security_limit, profile)

    def onXMLUI(self, xml_ui):
        """Display a dialog received from the backend.

        @param xml_ui (unicode): dialog XML representation
        """
        # FIXME: we temporarily use ElementTree, but a real XMLUI managing module
        #        should be available in the future
        # TODO: XMLUI module
        ui = ET.fromstring(xml_ui.encode('utf-8'))
        dialog = ui.find("dialog")
        if dialog is not None:
            self.disp(dialog.findtext("message"), error=dialog.get("level") == "error")

    def connected(self):
        """Auto reply to confirmations requests"""
        self.need_loop = True
        super(CommandAnswering, self).connected()
        self.host.bridge.register("actionNew", self.onActionNew)
        actions = self.host.bridge.actionsGet(self.profile)
        for action_data, action_id, security_limit in actions:
            self.onActionNew(action_data, action_id, security_limit, self.profile)
