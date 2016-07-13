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
import sys
from sat.core.i18n import _
from sat.tools.utils import clean_ustr

__commands__ = ["Message"]


class Send(base.CommandBase):

    def __init__(self, host):
        super(Send, self).__init__(host, 'send', help=_('send a message to a contact'))

    def add_parser_options(self):
        self.parser.add_argument("-s", "--separate", action="store_true", help=_("separate xmpp messages: send one message per line instead of one message alone."))
        self.parser.add_argument("-n", "--new-line", action="store_true", help=_("add a new line at the beginning of the input (usefull for ascii art ;))"))
        self.parser.add_argument("jid", type=str, help=_("the destination jid"))

    def start(self):
        jids = self.host.check_jids([self.args.jid])
        jid = jids[0]
        self.sendStdin(jid)

    def sendStdin(self, dest_jid):
        """Send incomming data on stdin to jabber contact

        @param dest_jid: destination jid
        """
        header = "\n" if self.args.new_line else ""

        if self.args.separate:  #we send stdin in several messages

            if header:
                self.host.bridge.sendMessage(dest_jid, header, profile_key=self.profile, callback=lambda: None, errback=lambda ignore: ignore)

            while (True):
                line = clean_ustr(sys.stdin.readline().decode('utf-8','ignore'))
                if not line:
                    break
                self.host.bridge.sendMessage(dest_jid, line.replace("\n",""), profile_key=self.host.profile, callback=lambda: None, errback=lambda ignore: ignore)

        else:
            msg = header + clean_ustr(u"".join([stream.decode('utf-8','ignore') for stream in sys.stdin.readlines()]))
            self.host.bridge.sendMessage(dest_jid, msg, profile_key=self.host.profile, callback=lambda: None, errback=lambda ignore: ignore)


class Message(base.CommandBase):
    subcommands = (Send, )

    def __init__(self, host):
        super(Message, self).__init__(host, 'message', use_profile=False, help=_('messages handling'))
