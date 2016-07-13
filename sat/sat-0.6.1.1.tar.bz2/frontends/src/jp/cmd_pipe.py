#! /usr/bin/python
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

from sat_frontends.jp import base

import tempfile
import sys
import os
import os.path
import shutil
from sat.core.i18n import _
from sat_frontends.tools import jid
import xml.etree.ElementTree as ET # FIXME: used temporarily to manage XMLUI


__commands__ = ["Pipe"]


class PipeOut(base.CommandBase):

    def __init__(self, host):
        super(PipeOut, self).__init__(host, 'out', help=_('send a pipe a stream'))
        self.need_loop = True

    def add_parser_options(self):
        self.parser.add_argument("jid", type=base.unicode_decoder, help=_("the destination jid"))

    def start(self):
        """ Create named pipe, and send stdin to it """
        # TODO: check_jids
        tmp_dir = tempfile.mkdtemp()
        fifopath = os.path.join(tmp_dir,"pipe_out")
        os.mkfifo(fifopath)
        self.host.bridge.pipeOut(self.host.get_full_jid(self.args.jid), fifopath, self.profile)
        with open(fifopath, 'w') as f:
            shutil.copyfileobj(sys.stdin, f)
        shutil.rmtree(tmp_dir)
        self.host.quit()


class PipeIn(base.CommandAnswering):

    def __init__(self, host):
        super(PipeIn, self).__init__(host, 'in', help=_('receive a pipe stream'))
        self.action_callbacks = {"PIPE": self.onPipeAction}

    def add_parser_options(self):
        self.parser.add_argument("jids", type=base.unicode_decoder, nargs="*", help=_('Jids accepted (none means "accept everything")'))

    def getXmluiId(self, action_data):
        # FIXME: we temporarily use ElementTree, but a real XMLUI managing module
        #        should be available in the futur
        # TODO: XMLUI module
        try:
            xml_ui = action_data['xmlui']
        except KeyError:
            self.disp(_(u"Action has no XMLUI"), 1)
        else:
            ui = ET.fromstring(xml_ui.encode('utf-8'))
            xmlui_id = ui.get('submit')
            if not xmlui_id:
                self.disp(_(u"Invalid XMLUI received"), error=True)
            return xmlui_id

    def onPipeAction(self, action_data, action_id, security_limit, profile):
        xmlui_id = self.getXmluiId(action_data)
        if xmlui_id is None:
            return self.host.quitFromSignal(1)
        try:
            from_jid = jid.JID(action_data['meta_from_jid'])
        except KeyError:
            self.disp(_(u"Ignoring action without from_jid data"), 1)
            return

        if not self.bare_jids or from_jid.bare in self.bare_jids:
            tmp_dir = tempfile.mkdtemp()
            fifopath = os.path.join(tmp_dir,"pipe_in")
            os.mkfifo(fifopath)
            xmlui_data = {'path': fifopath}
            self.host.bridge.launchAction(xmlui_id, xmlui_data, profile_key=profile)

            with open(fifopath, 'r') as f:
                shutil.copyfileobj(f, sys.stdout)
            shutil.rmtree(tmp_dir)
            self.host.quit()

    def start(self):
        self.bare_jids = [jid.JID(jid_).bare for jid_ in self.args.jids]


class Pipe(base.CommandBase):
    subcommands = (PipeOut, PipeIn)

    def __init__(self, host):
        super(Pipe, self).__init__(host, 'pipe', use_profile=False, help=_('stream piping through XMPP'))
