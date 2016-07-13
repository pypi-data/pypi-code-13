#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# SAT plugin for managing pipes (experimental)
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

from sat.core.i18n import _, D_
from sat.core.constants import Const as C
from sat.core.log import getLogger
log = getLogger(__name__)
from sat.tools import xml_tools
from twisted.words.xish import domish
from twisted.words.protocols.jabber import jid
from twisted.internet import defer

NS_PIPE = 'http://salut-a-toi.org/protocol/pipe'
SECURITY_LIMIT=30

PLUGIN_INFO = {
    "name": "Pipe Plugin",
    "import_name": "EXP-PIPE",
    "type": "EXP",
    "protocols": ["EXP-PIPE"],
    "dependencies": ["XEP-0166"],
    "main": "Exp_Pipe",
    "handler": "no",
    "description": _("""Jingle Pipe Transfer experimental plugin""")
}

CONFIRM = D_(u"{peer} wants to send you a pipe stream, do you accept ?")
CONFIRM_TITLE = D_(u"Pipe stream")

class Exp_Pipe(object):
    """This non standard jingle application works with named pipes"""

    def __init__(self, host):
        log.info(_("Plugin Pipe initialization"))
        self.host = host
        self._j = host.plugins["XEP-0166"] # shortcut to access jingle
        self._j.registerApplication(NS_PIPE, self)
        host.bridge.addMethod("pipeOut", ".plugin", in_sign='sss', out_sign='', method=self._pipeOut)

    # jingle callbacks

    def _pipeOut(self, peer_jid_s, filepath, profile_key=C.PROF_KEY_NONE):
        profile = self.host.memory.getProfileName(profile_key)
        self.pipeOut(jid.JID(peer_jid_s), filepath, profile)

    def pipeOut(self, peer_jid, filepath, profile):
        """send a file using EXP-PIPE

        @param peer_jid(jid.JID): recipient
        @param filepath(unicode): absolute path to the named pipe to send
        @param profile_key: %(doc_profile_key)s
        @return: an unique id to identify the transfer
        """
        self._j.initiate(peer_jid,
                         [{'app_ns': NS_PIPE,
                           'senders': self._j.ROLE_INITIATOR,
                           'app_kwargs': {'filepath': filepath,
                                         },
                         }],
                         profile=profile)

    def jingleSessionInit(self, session, content_name, filepath, profile=C.PROF_KEY_NONE):
        content_data = session['contents'][content_name]
        application_data = content_data['application_data']
        assert 'file_path' not in application_data
        application_data['file_path'] = filepath
        desc_elt = domish.Element((NS_PIPE, 'description'))
        return desc_elt

    def jingleRequestConfirmation(self, action, session, content_name, desc_elt, profile):
        """This method request confirmation for a jingle session"""
        content_data = session['contents'][content_name]
        if content_data['senders'] not in (self._j.ROLE_INITIATOR, self._j.ROLE_RESPONDER):
            log.warning(u"Bad sender, assuming initiator")
            content_data['senders'] = self._j.ROLE_INITIATOR

        def gotConfirmation(data):
            if data.get('cancelled', False):
                return False
            application_data = content_data['application_data']
            dest_path = application_data['file_path'] = data['path']
            content_data['file_obj'] = open(dest_path, 'w+')
            finished_d = content_data['finished_d'] = defer.Deferred()
            args = [session, content_name, content_data, profile]
            finished_d.addCallbacks(self._finishedCb, self._finishedEb, args, None, args)
            return True

        d = xml_tools.deferDialog(self.host,
            _(CONFIRM).format(peer=session['peer_jid'].full()),
            _(CONFIRM_TITLE),
            type_=C.XMLUI_DIALOG_FILE,
            options={C.XMLUI_DATA_FILETYPE: C.XMLUI_DATA_FILETYPE_DIR},
            action_extra={'meta_from_jid': session['peer_jid'].full(),
                          'meta_type': "PIPE",
                         },
            security_limit=SECURITY_LIMIT,
            profile=profile)

        d.addCallback(gotConfirmation)
        return d

    def jingleHandler(self, action, session, content_name, desc_elt, profile):
        content_data = session['contents'][content_name]
        application_data = content_data['application_data']
        if action in (self._j.A_ACCEPTED_ACK, self._j.A_SESSION_INITIATE):
            pass
        elif action == self._j.A_SESSION_ACCEPT:
            assert not 'file_obj' in content_data
            filepath = application_data['file_path']
            content_data['file_obj'] = open(filepath, 'r')  # XXX: we have to be sure that filepath is well opened, as reading can block it
            finished_d = content_data['finished_d'] = defer.Deferred()
            args = [session, content_name, content_data, profile]
            finished_d.addCallbacks(self._finishedCb, self._finishedEb, args, None, args)
        else:
            log.warning(u"FIXME: unmanaged action {}".format(action))
        return desc_elt

    def _finishedCb(self, dummy, session, content_name, content_data, profile):
        log.info(u"Pipe transfer completed")
        self._j.contentTerminate(session, content_name, profile=profile)
        content_data['file_obj'].close()

    def _finishedEb(self, failure, session, content_name, content_data, profile):
        log.warning(u"Error while streaming pipe: {}".format(failure))
        content_data['file_obj'].close()
        self._j.contentTerminate(session, content_name, reason=self._j.REASON_FAILED_TRANSPORT, profile=profile)
